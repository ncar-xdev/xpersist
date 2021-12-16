---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Tutorial: Using xpersist to Cache Data

xpersist is a Python package for caching data in Python. It is designed to be used in conjunction with analysis packages such as xarray, pandas which provide convenient interfaces for saving and loading data to and from disk.

This notebook provides an example of current usage of xpersist. It is not intended to be a complete tutorial on how to use xpersist. For more information, see the rest of [xpersist documentation](https://xpersist.readthedocs.io/en/latest/).

Let's import the packages we will use.

```{code-cell} ipython3
import xpersist
import xarray as xr
import tempfile
```

## Set Cache Location

To use xpersist, we must set the location of the cache. This is done by instatiating a {py:class}`xpersist.cache.CacheStore` class. The cache store points to a POSIX directory or a cloud storage bucket where all cached data will be stored. In this example, we will use a local directory.

```{code-cell} ipython3
store = xpersist.CacheStore(f'{tempfile.gettempdir()}/my-cache')
store
```

## Put Data in the Cache

Now we can use the `store` object to cache some data. The data can be any Python object.

```{code-cell} ipython3
ds = xr.tutorial.open_dataset('rasm').isel(time=slice(0, 2))
value = {'bar': 'baz'}
```

By default, xpersist will some heuristics to determine the right serializer to use. We can override this by specifying the serializer in the `serializer` argument.

```{code-cell} ipython3
_ = store.put('foo', value)
_ = store.put('my-dataset', ds, serializer='xarray.zarr', dump_kwargs={'mode': 'w'})
```

## Get Data from the Cache

To find the list of keys in the cache, use the {py:meth}`xpersist.cache.CacheStore.keys` method.

```{code-cell} ipython3
store.keys()
```

To retrieve the data from the cache, use the {py:meth}`xpersist.cache.CacheStore.get` method. The `get` method returns a deserialized object. Let's retrieve our dataset and the dictionary values we previously cached.

```{code-cell} ipython3
value_from_cache = store.get('foo')
print(value_from_cache)
```

```{code-cell} ipython3
ds_from_cache = store.get('my-dataset')
print(ds_from_cache)
```

To confirm that the data is the same, we can use the {py:keyword}`assert` statement and {py:func}`xarray.testing.assert_equal` function:

```{code-cell} ipython3
assert value == value_from_cache
xr.testing.assert_equal(ds, ds_from_cache)
```

## Inspect the Cache

There are a few other methods that can be used to inspect the cache. For example, the {py:meth}`xpersist.cache.CacheStore.get_artifact` method returns an {py:class}`xpersist.cache.Artifact` object. An artifact object is a Python object that contains metadata about the data stored in the cache.

```{code-cell} ipython3
artifact = store.get_artifact('my-dataset')
artifact
```

## Delete Data from the Cache

To delete data from the cache, use the {py:meth}`xpersist.cache.CacheStore.delete` method and pass the key of the data to delete.

```{code-cell} ipython3
store.delete('foo')
```

By default, the `delete` method will run in dry-run mode. This means that it will not actually delete the data from the cache. To actually delete the data, use the `dry_run=False` argument.

```{code-cell} ipython3
store.delete('foo', dry_run=False)
```

To confirm that the data was deleted, we can check the available keys in the cache:

```{code-cell} ipython3
store.keys()
```
