import os
import shutil

import dask
import xarray as xr
from toolz import curry

from . import settings

__all__ = ['PersistedDataset', 'persist_ds']

_actions = {'read_cache_trusted', 'read_cache_verified', 'overwrite_cache', 'create_cache'}
_formats = {'nc', 'zarr'}


class PersistedDataset:
    """
    Generate an `xarray.Dataset` from a function and cache the result to file.
    If the cache file exists, don't recompute, but read back in from file.

    Attempt to detect changes in the function and arguments used to generate the dataset,
    to ensure that the cache file is correct (i.e., it was produced by the same function
    called with the same arguments).

    On the first call, however, assume the cache file is correct.
    """

    # class property, dictionary: {cache_file: tokenized_name, ...}
    _tokens = {}

    # class property
    _actions = {}

    def __init__(
        self,
        func,
        name=None,
        path=None,
        trust_cache=False,
        clobber=False,
        format='nc',
        open_ds_kwargs={},
    ):
        """set instance attributes"""
        self._func = func
        self._name = name
        self._path = path
        self._trust_cache = trust_cache
        self._clobber = clobber

        if format not in _formats:
            raise ValueError(f'unknown format: {format}')
        self._format = format

        self._open_ds_kwargs = open_ds_kwargs

    def _check_token_assign_action(self, token):
        """check for matching token, if appropriate"""

        if self._cache_exists:

            # if we don't yet know about this file, assume it's the right one;
            # this enables usage on first call in a Python session, for instance
            known_cache = self._cache_file in PersistedDataset._tokens
            if not known_cache or self._trust_cache and not self._clobber:
                print('assuming cache is correct')
                PersistedDataset._tokens[self._cache_file] = token
                PersistedDataset._actions[self._cache_file] = 'read_cache_trusted'

            # if the cache file is present and we know about it,
            # check the token; if the token doesn't match, remove the file
            elif known_cache:
                if token != PersistedDataset._tokens[self._cache_file] or self._clobber:
                    print(f'name mismatch, removing: {self._cache_file}')
                    if self._format != 'zarr':
                        os.remove(self._cache_file)
                    else:
                        shutil.rmtree(self._cache_file, ignore_errors=True)
                    PersistedDataset._actions[self._cache_file] = 'overwrite_cache'
                else:
                    PersistedDataset._actions[self._cache_file] = 'read_cache_verified'

        else:
            PersistedDataset._tokens[self._cache_file] = token
            PersistedDataset._actions[self._cache_file] = 'create_cache'
            if os.path.dirname(self._cache_file) and not os.path.exists(self._path):
                print(f'making {self._path}')
                os.makedirs(self._path)

        assert PersistedDataset._actions[self._cache_file] in _actions

    @property
    def _basename(self):
        if self._name.endswith('.' + self._format):
            return self._name
        else:
            return f'{self._name}.{self._format}'

    @property
    def _cache_file(self):
        return os.path.join(self._path, self._basename)

    @property
    def _cache_exists(self):
        """does the cache exist?"""
        return os.path.exists(self._cache_file)

    def __call__(self, *args, **kwargs):
        """call function or read cache"""
        # Generate Deterministic token
        token = dask.base.tokenize(self._func, args, kwargs)
        if self._name is None:
            self._name = f'PersistedDataset-{token}'

        if self._path is None:
            self._path = settings['cache_dir']

        self._check_token_assign_action(token)

        if {'read_cache_trusted', 'read_cache_verified'}.intersection(
            {self._actions[self._cache_file]}
        ):
            print(f'reading cached file: {self._cache_file}')
            if self._format == 'nc':
                return xr.open_dataset(self._cache_file, **self._open_ds_kwargs)
            elif self._format == 'zarr':
                if 'consolidated' not in self._open_ds_kwargs:
                    zarr_kwargs = self._open_ds_kwargs.copy()
                    zarr_kwargs['consolidated'] = True
                return xr.open_zarr(self._cache_file, **zarr_kwargs)

        elif {'create_cache', 'overwrite_cache'}.intersection({self._actions[self._cache_file]}):
            # generate dataset
            ds = self._func(*args, **kwargs)

            # write dataset
            print(f'writing cache file: {self._cache_file}')

            if self._format == 'nc':
                ds.to_netcdf(self._cache_file)

            elif self._format == 'zarr':
                ds.to_zarr(self._cache_file, consolidated=True)

            return ds


@curry
def persist_ds(
    func, name=None, path=None, trust_cache=False, clobber=False, format='nc', open_ds_kwargs={}
):
    """Wraps a function to produce a ``PersistedDataset``.

    Parameters
    ----------

    func : callable
       The function to execute: ds = func(*args, **kwargs)
       Must return an `xarray.dataset`
    file_name : string, optional
       Name of the cache file.
    open_ds_kwargs : dict, optional
       Keyword arguments to `xarray.open_dataset`.

    Returns
    -------
    PersistedDataset
    """
    if not callable(func):
        raise ValueError('func must be callable')

    return PersistedDataset(func, name, path, trust_cache, clobber, format, open_ds_kwargs)
