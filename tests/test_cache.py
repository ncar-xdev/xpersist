import fsspec
import pandas as pd
import pytest
import xarray as xr

from xpersist import CacheStore
from xpersist.cache import Artifact


@pytest.mark.parametrize('readonly', [True, False])
def test_initialization(tmp_path, readonly):
    store = CacheStore(str(tmp_path), readonly=readonly)
    assert isinstance(store.mapper, fsspec.mapping.FSMap)
    assert isinstance(store.raw_path, str)
    assert store.raw_path == str(tmp_path)
    assert store.readonly == readonly


@pytest.mark.parametrize(
    'key, data, serializer',
    [
        ('bar', 'my_data', 'joblib'),
        ('foo', [1, 3, 4], 'auto'),
        ('test.nc', xr.DataArray([1, 2]).to_dataset(name='sst'), 'xarray.netcdf'),
        ('my_dataset.zarr', xr.DataArray([1, 2]).to_dataset(name='sst'), 'xarray.zarr'),
        ('foo.parquet', pd.DataFrame({'foo': [1, 2]}), 'pandas.parquet'),
    ],
)
def test_put_and_get(tmp_path, key, data, serializer):
    store = CacheStore(str(tmp_path))
    store.put(key=key, value=data, serializer=serializer)
    assert key in store.keys()
    assert isinstance(store.get_artifact(key), Artifact)
    results = store[key]
    if isinstance(data, (xr.Dataset, xr.DataArray)):
        xr.testing.assert_equal(results, data)
    elif isinstance(data, pd.DataFrame):
        pd.testing.assert_frame_equal(results, data)
    else:
        assert results == data


@pytest.mark.parametrize(
    'key, data, serializer',
    [
        ('bar', 'my_data', 'joblib'),
        ('foo', [1, 3, 4], 'auto'),
        ('test.nc', xr.DataArray([1, 2]).to_dataset(name='sst'), 'xarray.netcdf'),
        ('test.zarr', xr.DataArray([1, 2]).to_dataset(name='sst'), 'xarray.zarr'),
        ('foo.parquet', pd.DataFrame({'foo': [1, 2]}), 'pandas.parquet'),
    ],
)
def test_delete(tmp_path, key, data, serializer):
    store = CacheStore(str(tmp_path))
    store.put(key=key, value=data, serializer=serializer)
    assert key in store.keys()
    store.delete(key=key, dry_run=True)
    del store[key]
    assert key not in store.keys()


def test_delete_error(tmp_path):
    store = CacheStore(str(tmp_path))
    with pytest.raises(KeyError):
        store.delete(key='foo', dry_run=False)
