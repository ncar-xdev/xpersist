import toolz

from xpersist.func_inspect import get_func_info, with_merged_defaults


def test_func_info_lambda():
    add_one = lambda x: x + 1
    info = get_func_info(add_one)
    info.pop('source')
    assert info == {'name': '<lambda>', 'module': 'test_func_inspect', 'varargs': (), 'kargs': {}}


def test_func_info_with_partial():
    def mult(x, y):
        return x * y

    double = toolz.partial(mult, 2)
    info = get_func_info(double)
    info.pop('source')
    assert info == {'name': 'mult', 'module': 'test_func_inspect', 'varargs': (), 'kargs': {'x': 2}}


def test_func_info_with_partial_of_partial():
    def mult(*args):
        return toolz.reduce(lambda a, b: a * b, args)

    double = toolz.partial(mult, 2)
    quad = toolz.partial(double, 2)
    info = get_func_info(quad)
    info.pop('source')
    assert info == {'name': 'mult', 'module': 'test_func_inspect', 'varargs': (2, 2), 'kargs': {}}


def test_func_info_with_curry():
    @toolz.curry
    def mult(x, y):
        return x * y

    double = mult(2)
    assert double(3) == 6
    info = get_func_info(double)
    info.pop('source')
    assert info == {'name': 'mult', 'module': 'test_func_inspect', 'varargs': (), 'kargs': {'x': 2}}


def test_func_info_with_multiple_curries():
    @toolz.curry
    def mult(a, b, c):
        return a * b * c

    double = mult(2)
    quad = double(2)
    info = get_func_info(quad)
    info.pop('source')
    assert info == {
        'name': 'mult',
        'module': 'test_func_inspect',
        'varargs': (),
        'kargs': {'a': 2, 'b': 2},
    }


def test_with_merged_defaults_basic_merging():
    foo_defaults = {'a': 1, 'b': 2}

    @with_merged_defaults()
    def bar(foo=foo_defaults):
        return foo

    assert bar() == {'a': 1, 'b': 2}
    assert bar(foo={'c': 3}) == {'a': 1, 'b': 2, 'c': 3}
    assert bar(foo={'a': 10}) == {'a': 10, 'b': 2}


def test_with_merged_defaults_with_non_dict_args():
    foo_defaults = {'a': 1, 'b': 2}

    @with_merged_defaults()
    def bar(a, foo=foo_defaults, baz=None):
        return a, baz, foo

    assert bar(5) == (5, None, {'a': 1, 'b': 2})
    assert bar(5, baz='baz', foo={'c': 3}) == (5, 'baz', {'a': 1, 'b': 2, 'c': 3})


def test_with_merged_defaults_with_args_splat():
    foo_defaults = {'a': 1, 'b': 2}

    @with_merged_defaults()
    def bar(*args, foo=foo_defaults):
        return args, foo

    assert bar(5, 10) == ((5, 10), {'a': 1, 'b': 2})
    assert bar() == ((), {'a': 1, 'b': 2})
