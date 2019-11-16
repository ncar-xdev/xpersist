
# xpersist

Simple utility for wrapping functions that generate an `xarray.Dataset` and cache the result to file. If the cache file exists, don't recompute, but read back in from file.
