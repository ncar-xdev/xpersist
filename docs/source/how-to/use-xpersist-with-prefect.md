---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Use xpersist with Prefect

Let's begin by importing necessary packages and enabling checkpointing.

```{code-cell} ipython3
import os

os.environ["PREFECT__FLOWS__CHECKPOINTING"] = "True"

import tempfile
import time
from xpersist import XpersistResult, CacheStore
from prefect import Flow, task
import prefect
import xarray as xr
```

Ensure that checkpointing is enabled:

```{code-cell} ipython3
prefect.context.to_dict()['config']['flows']['checkpointing']
```

## Set Cache Location

```{code-cell} ipython3
store = CacheStore(f'{tempfile.gettempdir()}/my-cache')
```

## Set Prefect Flow

To enable persisting output of a task in xpersist's cache store, we need to define a {py:class}`xpersist.XpersistResult` object and pass it to the `result` argument of the `task` decorator.

```{code-cell} ipython3
@task(
    target="bar",
    result=XpersistResult(
        store, serializer="xarray.zarr", serializer_dump_kwargs={"mode": "w"}
    ),
)
def get_data():
    ds = xr.DataArray(range(10), dims="x", name="bar").to_dataset()
    time.sleep(5)
    return ds


@task
def total(ds):
    return ds.sum()


with Flow("my-flow") as flow:
    ds = get_data()
    total(ds)

```

```{code-cell} ipython3
flow.visualize()
```

## Run the Flow

Now we can run the flow. Notice that the flow runs for five seconds and the result for `get_data()` task is cached.

```{code-cell} ipython3
%%time
flow.run()
```

Confirm that the result is cached using the specified target name/key ('bar')

```{code-cell} ipython3
store.keys()
```

Running the flow again will retrieve the result from the cache instead of running the task again:

```{code-cell} ipython3
%%time
flow.run()
```

Notice that the flow takes milliseconds to run instead of the original five seconds.
