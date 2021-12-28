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

## Set cache location

To use xpersist, we must set the location of the cache. This is done by instatiating a {py:class}`xpersist.cache.CacheStore` class. The cache store points to a POSIX directory or a cloud storage bucket where all cached data will be stored. In this example, we will use a local directory.

```{code-cell} ipython3
store = xpersist.CacheStore(f'{tempfile.gettempdir()}/my-cache')
store
```

## Put data in the Cache

Now we can use the `store` object to cache some data. The data can be any Python object.

```{code-cell} ipython3
ds = xr.tutorial.open_dataset('rasm').isel(time=slice(0, 2))
value = {'bar': 'baz'}
```

### Get the full list of available serializers

By default, xpersist uses some heuristics based on an object's type to determine the right serializer to use. Instead of relying on xpersist's heuristics, we can specify the name of the serializer in the `serializer` argument. To get the list of available serializers, we can use `xpersist.registry.serializers.get_all()`. This will return a dictionary of serializer names and their associated {py:class}`xpersist.serializers.Serializer` instances.

```{code-cell} ipython3
serializers = xpersist.registry.serializers.get_all().keys()
[serializer for serializer in serializers]
```

Once we know the name of the serializer we want to use, we can specify it in the `serializer` argument.

```{code-cell} ipython3
_ = store.put('foo', value)
_ = store.put('my-dataset.zarr', ds, serializer='xarray.zarr', dump_kwargs={'mode': 'w'})
```

## Get data from the Cache

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
ds_from_cache = store.get('my-dataset.zarr')
print(ds_from_cache)
```

To confirm that the data is the same, we can use the {py:keyword}`assert` statement and {py:func}`xarray.testing.assert_equal` function:

```{code-cell} ipython3
assert value == value_from_cache
xr.testing.assert_equal(ds, ds_from_cache)
```

## Inspect the cache

There are a few other methods that can be used to inspect the cache. For example, the {py:meth}`xpersist.cache.CacheStore.get_artifact` method returns an {py:class}`xpersist.cache.Artifact` object. An artifact object is a Python object that contains metadata about the data stored in the cache.

```{code-cell} ipython3
artifact = store.get_artifact('my-dataset.zarr')
artifact
```

## Delete data from the cache

To delete data from the cache, use the {py:meth}`xpersist.cache.CacheStore.delete` method and pass the key of the data to delete.

```{code-cell} ipython3
store.delete('my-dataset.zarr')
```

By default, the `delete` method will run in dry-run mode. This means that it will not actually delete the data from the cache. To actually delete the data, use the `dry_run=False` argument.

```{code-cell} ipython3
store.delete('my-dataset.zarr', dry_run=False)
```

To confirm that the data was deleted, we can check the available keys in the cache:

```{code-cell} ipython3
store.keys()
```

Trying to delete a key that does not exist in the cache will raise an error.

```{code-cell} ipython3
store.delete('my-dataset.zarr', dry_run=False)
```
