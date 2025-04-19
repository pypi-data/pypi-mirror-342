import sys

__all__ = ('iterfilter', 'last', 'first', 'iterrange', 'itermap')

if sys.version_info[0] < 3:
    def itermap(fn, iterable):
        return (fn(it) for it in iterable)


    def iterfilter(fn, iterable):
        return (it for it in iterable if fn(it))


    iterrange = xrange
else:
    itermap = map
    iterfilter = filter
    iterrange = range


def first(iterable, default=None, key=None):
    if key is None:
        def key(it):
            return it

    for item in iterable:
        if key(item):
            return item
    return default


def last(iterable, default=None, key=None):
    try:
        iterable = reversed(iterable)
    except TypeError:
        return last(tuple(iterable), key, default)
    return first(iterable, key, default)
