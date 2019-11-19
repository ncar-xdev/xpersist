settings = {'cache_dir': 'xpersist_cache'}

from pkg_resources import DistributionNotFound, get_distribution

from .core import *  # noqa: F403, F401

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass
