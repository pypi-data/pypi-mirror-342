from typing import TypeVar, Iterable, Callable, Type, MutableSequence, Generator

_T = TypeVar("_T")
_R = TypeVar("_R")

def self(it: _T) -> _T: ...

def toposort(data: dict[str, Iterable[_T]]) -> Generator[set[_T]]: ...

def rowchars(text: str, char: str, start: int = 0) -> int:
    """
    Counts the consecutive occurrences of a character.

    :param text: The input text to search in.
    :param char: The character to count occurrences of.
    :param start: The starting position in the text.
    :return: The number occurrences.
    """
    pass


def strip_indexes(source: MutableSequence, indexes: Iterable[int]):
    """
    Deletes the items of the source object at the specified indexes.

    :param source: An object that allows `__delitem__`.
    :param indexes: The indexes of elements to remove.
    """
    pass


def trymap(func: Callable[[_T], _R], value: _T, default: _R = None, allow: Iterable[Type[Exception]] = None) -> _R:
    """
    Safely apply a function to a value.

    If the `allow` param is None, all exceptions are allowed.

    :param func: The function to apply to the value.
    :param value:  The value to pass to the function.
    :param default: The value to return if an exception occurs.
    :param allow: Types of exceptions to catch and handle.
    :return: The result of func(value), or default if an allowed exception occurs.
    """
    pass
