import typing

import joblib

from .vendor._provenance import (  # noqa: F401
    args_extractor,
    inner_function,
    is_curry_func,
    param_info,
    with_merged_defaults,
)


def get_partial_func_info(partial_fn: typing.Callable) -> typing.Dict[str, typing.Any]:
    """
    Return the partial function information namely module, name, source, etc.
    """
    fn = inner_function(partial_fn)
    varargs, kargs = args_extractor(fn)(partial_fn.args, partial_fn.keywords)
    return {
        'varargs': varargs,
        'kargs': kargs,
        'module': fn.__module__,
        'name': joblib.func_inspect.get_func_name(fn)[1],
        'source': joblib.func_inspect.get_func_code(fn)[0],
    }


def get_func_info(fn: typing.Callable) -> typing.Dict[str, typing.Any]:
    """
    Return the function information namely module, name, source, etc.
    """
    if is_curry_func(fn):  # This is a partial function
        return get_partial_func_info(fn)

    return {
        'module': fn.__module__,
        'name': joblib.func_inspect.get_func_name(fn)[1],
        'source': joblib.func_inspect.get_func_code(fn)[0],
        'varargs': (),
        'kargs': {},
    }
