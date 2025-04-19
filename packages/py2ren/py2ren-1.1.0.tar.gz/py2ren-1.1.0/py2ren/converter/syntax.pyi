from typing import Union, Any

from .imports import ImportFrom, Import
from py2ren.config import FileConfig, ModuleConfig


class CodeConverter(object):
    """
    The code converter class.
    """
    __slots__ = ()

    def __init__(self: Any, config: Union[FileConfig, ModuleConfig]):
        """
        :param config: The configuration for the conversion.
        """
        pass

    @property
    def config(self: Any) -> Union[FileConfig, ModuleConfig]:
        """
        The configuration for the conversion.

        :getter: Returns the configuration for the conversion.
        """
        pass

    # def _convert_import(self, node: Union[Import, ImportFrom]) -> \
    #         Union[tuple[Union[Import, ImportFrom]], tuple[Union[Import, ImportFrom], ImportFrom]]:
    #     """
    #     Converts an import node.
    #
    #     Separates or modifies the import if the base of it is part of the store modules.
    #
    #     :param node: The import node.
    #     :return: An iterable with the converted imports.
    #     """
    #     pass

    # def _convert_import_from(self, node: ImportFrom, module: str=None) -> tuple[ImportFrom]:
    #     """
    #     Converts an import from node.
    #
    #     :param node: The import from node.
    #     :param module: The parent module name.
    #     :return: An iterable with the converted import.
    #     """
    #     pass

    # def _get_init_expression(self, name: str = None, level: int = None, module: str = None):
    #     """
    #     Creates an init python expression for a store module.
    #
    #     :param name: The name of the store module.
    #     :param level: The init python level.
    #     :param module: The parent module name.
    #     :return: The init python expression.
    #     """
    #     pass

    # def _convert_bases_expr(self, lines: list[str], node: ClassDef, remove_indexes: list[int],
    #                         class_bases: dict[str, str] = None, body_new_line: str = "\n"):
    #     """
    #     Replaces the class bases of the class def node in the source lines.
    #
    #     Keep in mind:
    #         * Do not add or remove any elements from the lines.
    #         * If you want a specific line to be removed, add its index to remove_indexes; it will then be removed.
    #
    #     :param lines: The source code lines.
    #     :param node: The class def node
    #     :param remove_indexes: A list of indexes from lines.
    #     :param class_bases: The base classes and their replacements.
    #     :param body_new_line: The text to join each code line.
    #     """
    #     pass

    # def _convert_imports_expr(self, lines: list[str], node: Union[Import, ImportFrom],
    #                           remove_indexes: list[int], module: str = None, body_new_line: str = "\n"):
    #     """
    #     Converts the import or import from node in the source lines.
    #
    #     Keep in mind:
    #         * Do not add or remove any elements from the lines.
    #         * If you want a specific line to be removed, add its index to remove_indexes; it will then be removed.
    #
    #     :param lines: The source code lines.
    #     :param node: The class def node
    #     :param remove_indexes: A list of indexes from lines.
    #     :param module: The parent module name.
    #     :param body_new_line: The text to join each code line.
    #     """
    #     pass

    # def _convert_node_expr(self, lines: list[str], node: ast.AST, remove_indexes: list[int], body_new_line: str = "\n"):
    #     """
    #     Generic call convert for a node.
    #
    #     Keep in mind:
    #         * Do not add or remove any elements from the lines.
    #         * If you want a specific line to be removed, add its index to remove_indexes; it will then be removed.
    #
    #     :param lines: The source code lines.
    #     :param node: An ast node.
    #     :param remove_indexes: A list of indexes from lines.
    #     :param body_new_line: The text to join each code line.
    #     """
    #     pass

    def convert_imports(self: Any, node: Union[Import, ImportFrom], module: str = None) -> \
            Union[tuple[Union[Import, ImportFrom]], tuple[Union[Import, ImportFrom], ImportFrom]]:
        """
        Converts an import or import from node.

        Separates or modifies the import if the base of it is part of the store modules.

        :param node: The import or import from node.
        :param module: The parent module name.
        :return: An iterable with the converted imports.
        :see: :attr:`.config.FileConfig.stored_modules`
        """
        pass

    def convert_simple(self: Any, code: str, module: str = None,
                       class_bases: dict[str, str] = None, body_new_line: str = "\n") -> str:
        """
        Converts the source code.

        Converts imports and replaces the base classes from which they inherit.

        :param code: The python source code
        :param module: The parent module name.
        :param class_bases: The base classes and their replacements.
        :param body_new_line: The text to join each code line.
        :return: The converted code.
        """
        pass

    def convert(self: Any, code: str, name: str = None, level: int = None, module: str = None,
                class_bases: dict[str, str] = None, init_offset: int = 0, init_body_offset: int = 4) -> str:
        """
        Convert the source code to a store module in ren'py.

        :param code: The python source code.
        :param name: The name of the store module.
        :param level: The init python level.
        :param module: The parent module name.
        :param class_bases: The base classes and their replacements.
        :param init_offset: The times to add a space offset to the init expression.
        :param init_body_offset: The times to add a space offset to the init body.
        :return: The code for a store module in ren'py
        """
        pass
