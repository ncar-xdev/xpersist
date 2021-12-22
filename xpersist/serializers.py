import functools
import typing

import joblib as _joblib
import pandas as pd
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


@registry.serializers.register('pandas.csv')
def pandas_csv() -> Serializer:
    return Serializer(name='pandas.csv', load=pd.read_csv, dump=pd.DataFrame.to_csv)


@registry.serializers.register('pandas.parquet')
def pandas_parquet() -> Serializer:
    return Serializer(name='pandas.parquet', load=pd.read_parquet, dump=pd.DataFrame.to_parquet)


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


@pick_serializer.register(pd.DataFrame)
def _(obj):
    return registry.serializers.get('pandas.csv')().name
