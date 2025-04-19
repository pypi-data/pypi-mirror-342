from typing import TypeVar, Iterable, Callable, Generator

_T = TypeVar("_T")
_R = TypeVar("_R")


def itermap(fn: Callable[[_T], _R], iterable: Iterable[_T]) -> Generator[_R]:
    """
    Map a function over an iterable lazily.

    Compatibility function for python 2. In python 3.x, its equivalent to **map()**.

    :param fn: Function to apply to each element
    :param iterable: Input iterable
    """
    pass


def iterfilter(fn: Callable[[_T], bool], iterable: Iterable[_T]) -> Generator[_T]:
    """
    Filter an iterable lazily based on a predicate.

    Compatibility function for python 2. In python 3.x, its equivalent to **filter()**.

    :param fn: Predicate function returning true for elements to keep
    :param iterable: Input iterable
    """
    pass


def iterrange(start: int = None, stop: int = None, step: int = None) -> Generator[int]:
    """
    Create a lazy range generator with optional start, stop and step parameters.

    Compatibility function. In python 2 is equivalent to **xrange()**; and in 3, its equivalent to **range()**.

    :param start: Starting value (inclusive).
    :param stop: Ending value (exclusive).
    :param step: Step size between values.
    """
    pass


def first(iterable: Iterable[_T], default: _T = None, key: Callable[[_T], bool] = None) -> _T:
    """
    Get the first element from an iterable that matches an optional key function.

    :param iterable: Input iterable
    :param default: Value to return if no element is found
    :param key: Predicate function to filter the first element.
    :return: First matching element or default value
    """
    pass


def last(iterable: Iterable[_T], default: _T = None, key: Callable[[_T], bool] = None):
    """
    Get the last element from an iterable that matches an optional key function.

    :param iterable: Input iterable
    :param default: Value to return if no element is found
    :param key: Predicate function to filter the last element.
    :return: Last matching element or default value
    """
    pass
