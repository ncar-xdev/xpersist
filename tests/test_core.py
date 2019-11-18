import os
from glob import glob
import numpy as np
import xarray as xr

import xpersist as xp

import pytest

here = os.path.abspath(os.path.dirname(__file__))
xp.settings['cache_dir'] = os.path.join(here, 'cached_data')

def rm_tmpfile():
    for p in ['tmp-*.nc', 'persisted_Dataset-*.nc']:
        for f in glob(os.path.join(here, 'cached_data', p)):
            os.remove(f)


@pytest.fixture(autouse=True)
def cleanup():
    rm_tmpfile()
    yield
    rm_tmpfile()

def func(scaleby):
    return xr.Dataset({'x': xr.DataArray(np.ones((50,))*scaleby)})


# must be first test
def test_xpersist_actions():
    ds = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.persisted_Dataset._actions.popitem()
    assert action == 'read_cache_trusted'

    ds = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.persisted_Dataset._actions.popitem()
    assert action == 'read_cache_verified'

    ds = xp.persist_ds(func, name='test-dset')(11)
    file, action = xp.persisted_Dataset._actions.popitem()
    assert action == 'overwrite_cache'

    #new_cache_file = os.path.join(here, 'cached_data', 'tmp-test-dset.nc')
    #if os.path.exists(new_cache_file):
#        os.remove(new_cache_file)
    ds = xp.persist_ds(func, name='tmp-test-dset')(11)
    file, action = xp.persisted_Dataset._actions.popitem()
    assert action == 'create_cache'


def test_arg_check():
    with pytest.raises(ValueError, match='func must be callable'):
        xp.persist_ds('not a function')


def test_xpersist_noname():
    ds = xp.persist_ds(func)(10)


def test_validate_dset():
    dsp = xp.persist_ds(func, name='test-dset')(10)
    file, action = xp.persisted_Dataset._actions.popitem()
    ds = xr.open_dataset(file)
    xr.testing.assert_identical(dsp, ds)
