import functools
import typing

import joblib as _joblib
import pydantic
import xarray as xr
import xcollection as xc

from .registry import registry


class Serializer(pydantic.BaseModel):
    """Pydantic model for defining a serializer."""

    name: str
    load: typing.Callable
    dump: typing.Callable


@registry.serializers.register('xarray.zarr')
def xarray_zarr() -> Serializer:
    return Serializer(name='xarray.zarr', load=xr.open_zarr, dump=xr.backends.api.to_zarr)


@registry.serializers.register('xarray.netcdf')
def xarray_netcdf() -> Serializer:
    return Serializer(name='xarray.netcdf', load=xr.open_dataset, dump=xr.backends.api.to_netcdf)


@registry.serializers.register('xcollection')
def xcollection() -> Serializer:
    return Serializer(name='xcollection', load=xc.open_collection, dump=xc.Collection.to_zarr)


@registry.serializers.register('joblib')
def joblib() -> Serializer:
    return Serializer(name='joblib', load=_joblib.load, dump=_joblib.dump)


@functools.singledispatch
def pick_serializer(obj) -> str:
    """Returns the id of the appropriate serializer

    Parameters
    ----------
    obj: any Python object

    Returns
    -------
    id : str
       Id of the serializer
    """

    return registry.serializers.get('joblib')().name


@pick_serializer.register(xr.Dataset)
def _(obj):
    return registry.serializers.get('xarray.netcdf')().name


@pick_serializer.register(xr.DataArray)
def _(obj):
    return registry.serializers.get('xarray.netcdf')().name


@pick_serializer.register(xc.Collection)
def _(obj):
    return registry.serializers.get('xcollection')().name
