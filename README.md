# xpersist

| CI          | [![GitHub Workflow Status][github-ci-badge]][github-ci-link] [![Code Coverage Status][codecov-badge]][codecov-link] |
| :---------- | :-----------------------------------------------------------------------------------------------------------------: |
| **Docs**    |                                   [![Documentation Status][rtd-badge]][rtd-link]                                    |
| **Package** |                        [![Conda][conda-badge]][conda-link] [![PyPI][pypi-badge]][pypi-link]                         |
| **License** |                                       [![License][license-badge]][repo-link]                                        |

xpersist provides custom caching utility functions in Python. It is designed to be used in conjunction with analysis packages such as xarray, pandas which provide convenient interfaces for saving and loading data to and from disk.

See [documentation](https://xpersist.readthedocs.io/en/latest/) for more information.

## Installation

xpersist can be installed from PyPI with pip:

```bash
python -m pip install xpersist
```

It is also available from `conda-forge` for conda installations:

```bash
conda install -c conda-forge xpersist
```

[github-ci-badge]: https://img.shields.io/github/workflow/status/ncar-xdev/xpersist/CI?label=CI&logo=github&style=for-the-badge
[github-ci-link]: https://github.com/ncar-xdev/xpersist/actions?query=workflow%3ACI
[codecov-badge]: https://img.shields.io/codecov/c/github/ncar-xdev/xpersist.svg?logo=codecov&style=for-the-badge
[codecov-link]: https://codecov.io/gh/ncar-xdev/xpersist
[rtd-badge]: https://img.shields.io/readthedocs/xpersist/latest.svg?style=for-the-badge
[rtd-link]: https://xpersist.readthedocs.io/en/latest/?badge=latest
[pypi-badge]: https://img.shields.io/pypi/v/xpersist?logo=pypi&style=for-the-badge
[pypi-link]: https://pypi.org/project/xpersist
[conda-badge]: https://img.shields.io/conda/vn/conda-forge/xpersist?logo=anaconda&style=for-the-badge
[conda-link]: https://anaconda.org/conda-forge/xpersist
[license-badge]: https://img.shields.io/github/license/ncar-xdev/xpersist?style=for-the-badge
[repo-link]: https://github.com/ncar-xdev/xpersist
