![Github Actions Status](https://github.com/matt-long/xpersist/workflows/CI/badge.svg)
[![codecov](https://codecov.io/gh/matt-long/xpersist/branch/master/graph/badge.svg)](https://codecov.io/gh/matt-long/xpersist)
[![PyPI](https://img.shields.io/pypi/v/xpersist.svg)](https://pypi.python.org/pypi/xpersist)

# xpersist

Simple utility for wrapping functions that generate an `xarray.Dataset` and cache the result to file. If the cache file exists, don't recompute, but read back in from file.


Attempt to detect changes in the function and arguments used to generate the dataset,
to ensure that the cache file is correct (i.e., it was produced by the same function
called with the same arguments).

On the first call, however, assume the cache file is correct.

# Examples

## Applied to function

```python
  import xarray as xr
  import xpersist as xp
  import numpy as np

  In [1]: def func(scaleby):
     ...:     return xr.Dataset({'x': xr.DataArray(np.ones((50,))*scaleby)})

  In [2]: func(10)
  Out[2]:
  <xarray.Dataset>
  Dimensions:  (dim_0: 50)
  Dimensions without coordinates: dim_0
  Data variables:
      x        (dim_0) float64 10.0 10.0 10.0 10.0 10.0 ... 10.0 10.0 10.0 10.0

  In [3]: ds = xp.persist_ds(func, name='func-output')(10)
  making xpersist_cache
  writing cache file: xpersist_cache/func-output.nc

  In [4]: ds
  Out[4]:
  <xarray.Dataset>
  Dimensions:  (dim_0: 50)
  Dimensions without coordinates: dim_0
  Data variables:
      x        (dim_0) float64 10.0 10.0 10.0 10.0 10.0 ... 10.0 10.0 10.0 10.0

  In [5]: ds = xp.persist_ds(func, name='func-output')(1000)
  name mismatch, removing: xpersist_cache/func-output.nc
  writing cache file: xpersist_cache/func-output.nc

  In [6]: ds = xp.persist_ds(func, name='func-output')(1000)
  reading cached file: xpersist_cache/func-output.nc
```

## Used as a decorator

```python
  import xarray as xr
  import xpersist as xp
  import numpy as np

  In [1]: @xp.persist_ds(name='func-output')
      ...: def func(scaleby):
      ...:     return xr.Dataset({'x': xr.DataArray(np.ones((50,))*scaleby)})

  In [2]: ds = func(10)
  writing cache file: xpersist_cache/func-output.nc

  In [3]: ds = func(10)
  reading cached file: xpersist_cache/func-output.nc
```
