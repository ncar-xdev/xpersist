# flake8: noqa
settings = {'cache_dir': 'xpersist_cache'}

from pkg_resources import DistributionNotFound, get_distribution

from .core import *
from .env_info import Environment

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = '9.9.9'  # pragma: no cover
