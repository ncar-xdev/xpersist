from typing import Callable

import catalogue
import pytest

import xpersist


@pytest.mark.parametrize(
    'registry_name,func_name,expected',
    [
        ('serializers', 'xarray.netcdf', True),
        ('serializers', 'my_func', False),
        ('my_registry', 'test', False),
    ],
)
def test_has(registry_name, func_name, expected):
    assert xpersist.registry.has(registry_name, func_name) == expected


@pytest.mark.parametrize(
    'registry_name,func_name',
    [
        ('serializers', 'xarray.netcdf'),
        ('serializers', 'xarray.zarr'),
        ('serializers', 'joblib'),
        ('serializers', 'xcollection'),
    ],
)
def test_get(registry_name, func_name):
    assert isinstance(xpersist.registry.get(registry_name, func_name), Callable)


def test_get_error():
    with pytest.raises(ValueError):
        xpersist.registry.get('my_registry', 'my_func')

    with pytest.raises(catalogue.RegistryError):
        xpersist.registry.get('serializers', 'my_func')


def test_create_error():
    with pytest.raises(ValueError):
        xpersist.registry.create('serializers')


def test_create():
    xpersist.registry.create('my_registry')

    @xpersist.registry.my_registry.register('test')
    def my_func():
        return

    assert xpersist.registry.has('my_registry', 'test')
