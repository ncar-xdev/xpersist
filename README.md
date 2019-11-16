
# xpersist

Simple utility for wrapping functions that generate an `xarray.Dataset` and cache the result to file. If the cache file exists, don't recompute, but read back in from file.


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
