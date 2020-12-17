# xpersist

- [xpersist](#xpersist)
  - [Badges](#badges)
  - [Overview](#overview)
  - [Examples](#examples)
    - [Applied to function](#applied-to-function)
    - [Used as a decorator](#used-as-a-decorator)

## Badges

| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![GitHub Workflow Status][github-lint-badge]][github-lint-link] [![Code Coverage Status][codecov-badge]][codecov-link] |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| **Docs**    |                                                                    [![Documentation Status][rtd-badge]][rtd-link]                                                                    |
| **Package** |                                                         [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                                                         |
| **License** |                                                                        [![License][license-badge]][repo-link]                                                                        |

## Overview

Simple utility for wrapping functions that generate an `xarray.Dataset` and cache the result to file. If the cache file exists, don't recompute, but read back in from file.

Attempt to detect changes in the function and arguments used to generate the dataset,
to ensure that the cache file is correct (i.e., it was produced by the same function
called with the same arguments).

On the first call, however, assume the cache file is correct.

## Examples

### Applied to function

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

### Used as a decorator

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

[github-ci-badge]: https://img.shields.io/github/workflow/status/NCAR/xpersist/CI?label=CI&logo=github&style=for-the-badge
[github-lint-badge]: https://img.shields.io/github/workflow/status/NCAR/xpersist/linting?label=linting&logo=github&style=for-the-badge
[github-ci-link]: https://github.com/NCAR/xpersist/actions?query=workflow%3ACI
[github-lint-link]: https://github.com/NCAR/xpersist/actions?query=workflow%3Alinting
[codecov-badge]: https://img.shields.io/codecov/c/github/NCAR/xpersist.svg?logo=codecov&style=for-the-badge
[codecov-link]: https://codecov.io/gh/NCAR/xpersist
[rtd-badge]: https://img.shields.io/readthedocs/xpersist/latest.svg?style=for-the-badge
[rtd-link]: https://xpersist.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/xpersist?logo=pypi&style=for-the-badge
[pypi-link]: https://pypi.org/project/xpersist
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/xpersist?logo=anaconda&style=for-the-badge
[conda-link]: https://anaconda.org/conda-forge/xpersist
[license-badge]: https://img.shields.io/github/license/NCAR/xpersist?style=for-the-badge
[repo-link]: https://github.com/NCAR/xpersist
