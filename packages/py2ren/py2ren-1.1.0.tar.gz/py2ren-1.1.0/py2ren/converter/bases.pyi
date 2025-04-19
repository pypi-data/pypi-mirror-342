import ast
from ast import Name

from typing import Generator

KNOWN_BASES: dict[str, str]
"""
The python base classes and their replacements in ren'py.
"""


class ClassDef(ast.ClassDef):
    """
    The ast.ClassDef class.
    """
    pass


def get_bases(node: ClassDef, bases: dict[str, str] = None) -> Generator[Name]:
    """
    Gets the names of the base classes to be replaced.

    :param node: The class def node.
    :param bases: The base classes and their replacements.
    :return: An iterator with the base class names.
    """
    pass


def get_regex(node: ClassDef, bases: dict[str, str] = None) -> str:
    """
    Create a regex pattern to match the base classes to be replaced in the source code.

    :param node: The class def node to generate regex for.
    :param bases: The base classes and their replacements.
    :return: The created pattern.
    """
    pass


def replace(source: str, node: ClassDef, bases: dict[str, str] = None) -> str:
    """
    Replaces the base classes with their equivalents in source code.

    :param source: The source code string to modify.
    :param node: The class def node to process.
    :param bases: The base classes and their replacements.
    :return: Modified source code with replaced base classes.
    """
    pass


def add_replacement(python_name: str, renpy_name: str):
    """
    Adds a base class replacement.

    :param python_name: The base class name.
    :param renpy_name: The replacement class name.
    """
    pass


def get_replacement(python_name: str, ):
    """
    Gets the replacement for the base class.
    
    :param python_name: TThe base class name.
    :return: The replacement class name.
    """
    pass
