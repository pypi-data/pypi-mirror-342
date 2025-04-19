import ast
from collections import Iterable
from typing import Union, AnyStr


class Import(ast.Import):
    """
    The ast.Import class.
    """
    pass


class ImportFrom(ast.ImportFrom):
    """
    The ast.ImportFrom class.
    """
    pass


def path2import(path: AnyStr) -> AnyStr: ...

def import2path(imp: AnyStr) -> AnyStr: ...

def i2import(iterable: Iterable[AnyStr]) -> AnyStr: ...

def get_internals(filepath: AnyStr, root: AnyStr, package: AnyStr = None) -> tuple[str, ...]: ...

def as_expression(node: Union[Import, ImportFrom]) -> str:
    """
    Converts the node to an expression.

    :param node: The import or import from node.
    :return: An import expression.
    """
    pass


def create_store_import(names: list[ast.alias], lineno: int, col_offset: int = 0) -> ImportFrom:
    """
    Creates an import from node for the store module.

    :param names: The names to imports.
    :param lineno: The line number.
    :param col_offset: The column offset.
    :return: An import from node.
    """
    pass


def as_store_import(imp: Union[Import, ImportFrom], parent_module: str = None) -> ImportFrom:
    """
    Converts an import node to an import from node for the store module.

    :param imp: The import node.
    :param parent_module: The parent module name for the import node.
    :return: An import from node.
    """
    pass
