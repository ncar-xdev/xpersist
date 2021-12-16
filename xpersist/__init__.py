#!/usr/bin/env python3
# flake8: noqa
""" Top-level module for xpersist. """
from pkg_resources import DistributionNotFound, get_distribution

from .cache import CacheStore
from .prefect.result import XpersistResult
from .registry import registry
from .serializers import pick_serializer

try:
    __version__ = get_distribution('xpersist').version
except DistributionNotFound:  # pragma: no cover
    __version__ = 'unknown'  # pragma: no cover
