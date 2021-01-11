"""
Vendored code snippets

from https://github.com/bmabey/provenance. Permalink: https://git.io/Jteub

"""

import collections
import inspect

import boltons.funcutils
import toolz

UNSPECIFIED_ARG = '::unspecified::'


def is_curry_func(f):
    """
    Checks if f is a toolz or cytoolz function by inspecting the available attributes.
    Avoids explicit type checking to accommodate all versions of the curry fn.
    """
    return hasattr(f, 'func') and hasattr(f, 'args') and hasattr(f, 'keywords')


def _func_param_info(argspec):
    params = argspec.args
    defaults = argspec.defaults or []
    start_default_ix = -max(len(defaults), 1) - 1
    values = [UNSPECIFIED_ARG] * (len(params) - len(defaults)) + list(defaults[start_default_ix:])
    return collections.OrderedDict(zip(params, values))


def param_info(f):
    if is_curry_func(f):
        argspec = inspect.getfullargspec(f.func)
        num_args = len(f.args)
        args_to_remove = argspec.args[0:num_args] + list(f.keywords.keys())
        base = _func_param_info(argspec)
        return toolz.dissoc(base, *args_to_remove)
    return _func_param_info(inspect.getfullargspec(f))


def args_extractor(f, merge_defaults=False):
    """
    Takes a function, inspects it's parameter lists, and returns a
    function that will return all of the named and key arguments
    back as a dictionary. The varargs are also returned which don't
    have a name.
    """
    spec = inspect.getfullargspec(f)
    if spec.defaults:
        param_defaults = dict(zip(spec.args[-len(spec.defaults) :], spec.defaults))
    else:
        param_defaults = {}
    named_param_defaults = spec.kwonlydefaults or {}
    default_dicts = {}
    num_named_args = len(spec.args)

    if merge_defaults is True and hasattr(f, '__merge_defaults__'):
        merge_defaults = f.__merge_defaults__

    if merge_defaults:
        default_dicts = toolz.pipe(
            toolz.merge(named_param_defaults, param_defaults),
            toolz.curried.valfilter(lambda v: isinstance(v, dict)),
        )

        if isinstance(merge_defaults, collections.abc.Sequence):
            default_dicts = {k: default_dicts[k] for k in merge_defaults}

        def _args_dict(args, kargs):
            unnamed_args = dict(zip(spec.args, args[0:num_named_args]))
            varargs = args[num_named_args:]
            kargs = toolz.merge(kargs, unnamed_args)
            for k, d in default_dicts.items():
                kargs[k] = toolz.merge(d, kargs.get(k) or {})
            return varargs, kargs

    else:

        def _args_dict(args, kargs):
            unnamed_args = dict(zip(spec.args, args[0:num_named_args]))
            varargs = args[num_named_args:]
            kargs = toolz.merge(kargs, unnamed_args)
            return varargs, kargs

    return _args_dict


def with_merged_defaults(*kwargs_to_default):
    """
    Introspects the argspec of the function being decorated to see what
    keyword arguments take dictionaries. If a dictionary is passed in when
    then function is called then it is merged with the dictionary defined
    in the parameter list.
    """
    merge_defaults = True
    if len(kwargs_to_default) > 0:
        merge_defaults = kwargs_to_default

    def _with_merged_defaults(f):
        extract_kargs = args_extractor(f, merge_defaults)

        @boltons.funcutils.wraps(f)
        def _merge_defaults(*args, **kargs):
            vargs, kargs = extract_kargs(args, kargs)
            return f(*vargs, **kargs)

        _merge_defaults.__merge_defaults__ = merge_defaults

        return _merge_defaults

    return _with_merged_defaults


def inner_function(partial_fn):
    """Returns the wrapped function of either a partial or curried function."""
    fn = partial_fn.func
    if '__module__' not in dir(fn):
        # for some reason the curry decorator nests the actual function
        # metadata one level deeper
        fn = fn.func
    return fn
