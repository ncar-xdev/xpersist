import os
import shutil
import stat
from contextlib import contextmanager
from glob import glob
from tempfile import TemporaryDirectory

import numpy as np
import pytest
import xarray as xr

import xpersist as xp

here = os.path.abspath(os.path.dirname(__file__))
xp.settings['cache_dir'] = os.path.join(here, 'cached_data')


def rm_tmpfile():
    for p in ['tmp-*.nc', 'PersistedDataset-*.nc']:
        for f in glob(os.path.join(here, 'cached_data', p)):
            os.remove(f)


@pytest.fixture(autouse=True)
def cleanup():
    rm_tmpfile()
    yield
    rm_tmpfile()


def func(scaleby):
    return xr.Dataset({'x': xr.DataArray(np.ones((50,)) * scaleby)})


# must be first test
def test_xpersist_actions():
    _ = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'read_cache_trusted'

    _ = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'read_cache_verified'

    _ = xp.persist_ds(func, name='test-dset')(11)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'overwrite_cache'

    _ = xp.persist_ds(func, name='tmp-test-dset')(11)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'create_cache'


def test_arg_check():
    with pytest.raises(ValueError, match='func must be callable'):
        xp.persist_ds('not a function')


def test_make_cache_dir():
    old = xp.settings['cache_dir'] = os.path.join(here, 'cached_data')
    new = os.path.join(here, 'tmp_cached_data')

    if os.path.exists(new):
        shutil.rmtree(new)
    xp.settings['cache_dir'] = new

    _ = xp.persist_ds(func, name='test-dset')(10)

    assert os.path.exists(new)

    shutil.rmtree(new)
    xp.settings['cache_dir'] = old


def test_xpersist_noname():
    _ = xp.persist_ds(func)(10)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'create_cache'


def test_clobber():
    _ = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'read_cache_verified'

    _ = xp.persist_ds(func, name='test-dset', clobber=True)(11)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'overwrite_cache'


def test_trusted():
    _ = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'read_cache_verified'

    _ = xp.persist_ds(func, name='test-dset', trust_cache=True)(11)
    file, action = xp.PersistedDataset._actions.popitem()
    assert action == 'read_cache_trusted'


def test_validate_dset():
    dsp = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.PersistedDataset._actions.popitem()
    ds = xr.open_dataset(file)
    xr.testing.assert_identical(dsp, ds)


def test_save_as_zarr():
    with TemporaryDirectory() as local_store:
        dsp = xp.persist_ds(func, name='test-dset', path=local_store, format='zarr')(10)
        zarr_store, action = xp.PersistedDataset._actions.popitem()
        ds = xr.open_zarr(zarr_store, consolidated=True)
        xr.testing.assert_identical(dsp, ds)


@contextmanager
def no_write_permissions(path):
    perm_orig = stat.S_IMODE(os.stat(path).st_mode)
    perm_new = perm_orig ^ stat.S_IWRITE
    try:
        os.chmod(path, perm_new)
        yield
    finally:
        os.chmod(path, perm_orig)


def test_write_permissionerror():
    with TemporaryDirectory() as local_store:
        zarr_store = os.path.join(local_store, 'mypath.zarr')

        # Zarr
        with no_write_permissions(local_store):
            with pytest.raises(PermissionError):
                _ = xp.persist_ds(func, name='test-dset', path=zarr_store, format='zarr')(10)
                assert not os.path.exists(zarr_store)

        # netCDF
        with no_write_permissions(local_store):
            with pytest.raises(PermissionError):
                _ = xp.persist_ds(func, name='test-dset', path=local_store)(10)
