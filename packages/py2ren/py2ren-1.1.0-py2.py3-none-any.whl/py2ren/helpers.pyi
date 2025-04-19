from typing import Union, Iterable, Generator

from py2ren.config import FileConfig, ModuleConfig
from py2ren.converter.syntax import CodeConverter


def get_config(path: str, name: str = None, stored_modules: Iterable[str] = None,
               level: int = 0, temp_config: bool = False, analyze_dependencies: bool = False) -> Union[
    FileConfig, ModuleConfig]:
    """
    Gets a configuration for the given path.

    If the configuration does not exist, it will be created and dumped.

    :param path: The target path.
    :param name: The name of the target as store module.
    :param stored_modules: The modules used in renpy are store modules.
    :param level: The init python level.
    :param temp_config: If true, no dumps the configuration if it does not exist.
    :param analyze_dependencies: Indicates whether the module's internal dependencies are analyzed.

    :see: :func:`.config.load`, :func:`.config.dump`
    """
    pass


def convfilew(path: str, converter: CodeConverter, name: str = None, level: int = 0, module: str = None,
              class_bases: dict[str, str] = None, init_offset: int = 0, init_body_offset: int = 4, ) -> str:
    """
    Converts the content of the given file using a converter.
    :param path: The target path.
    :param converter: The code converter.
    :param name: The name of the target as store module.
    :param level: The init python level.
    :param module: The parent module name.
    :param class_bases: The base classes and their replacements.
    :param init_offset: If true, no dumps the configuration if it does not exist.
    :param init_body_offset: The times to add a space offset to the init body.
    :return: The converted code.
    """
    pass


def convfile(path: str, name: str = None, stored_modules: Iterable[str] = None,
             level: int = 0, module: str = None, class_bases: dict[str, str] = None,
             temp_config: bool = False, init_offset: int = 0, init_body_offset: int = 4) -> str:
    """
    Converts the content of the given file.

    The path is expected to be a python file.

    :param path: The target path.
    :param name: The name of the target as store module.
    :param stored_modules: The modules used in renpy are store modules.
    :param level: The init python level.
    :param module: The parent module name.
    :param class_bases: The base classes and their replacements.
    :param temp_config: If true, no dumps the configuration if it does not exist.
    :param init_offset: The times to add a space offset to the init expression.
    :param init_body_offset: The times to add a space offset to the init body.
    :return: The converted code.
    """
    pass


def convfolderw(path: str, converter: CodeConverter, class_bases: dict[str, str] = None,
                init_offset: int = 0, init_body_offset: int = 4) -> Generator[tuple[str, str]]:
    """
    Converts the content of the given folder.

    The path is expected to be a folder with python files.

    :param path: The target path.
    :param converter: The code converter.
    :param class_bases: The base classes and their replacements.
    :param init_offset: The times to add a space offset to the init expression.
    :param init_body_offset: The times to add a space offset to the init body.
    :return: An iterator with the rpy filepath and the converted content.
    """
    pass


def convfolder(path: str, name: str = None, stored_modules: Iterable[str] = None,
               level: int = 0, class_bases: dict[str, str] = None, temp_config: bool = False,
               init_offset: int = 0, init_body_offset: int = 4, analyze_dependencies: bool = False) \
        -> Generator[tuple[str, str]]:
    """
    Converts the content of the given folder.

    The path is expected to be a folder with python files.

    :param path: The target path.
    :param name: The name of the target as store module.
    :param stored_modules: The modules used in renpy are store modules.
    :param level: The init python level.
    :param class_bases: The base classes and their replacements.
    :param temp_config: If true, no dumps the configuration if it does not exist.
    :param init_offset: The times to add a space offset to the init expression.
    :param init_body_offset: The times to add a space offset to the init body.
    :param analyze_dependencies: Indicates whether the module's internal dependencies are analyzed.
    :return: An iterator with the rpy filepath and the converted content.
    """
    pass


def convertw(path: str, out: str, converter: CodeConverter, name: str = None,
             level: int = 0, module: str = None, class_bases: dict[str, str] = None,
             init_offset: int = 0, init_body_offset: int = 4, keep_structure: bool = True):
    """
    Converts the content of the given path using a converter.

    :param path: The target path.
    :param out: The output folder.
    :param converter: The code converter.
    :param name: The name of the target as store module.
    :param level: The init python level.
    :param module: The parent module name.
    :param class_bases: The base classes and their replacements.
    :param init_offset: The times to add a space offset to the init expression.
    :param init_body_offset: The times to add a space offset to the init body.
    :param keep_structure: If true, keeps the structure of the source folder.
    """
    pass


def convert(path: str, out: str, name: str = None, stored_modules: Iterable[str] = None,
            level: int = 0, temp_config: bool = False, module: str = None, class_bases: dict[str, str] = None,
            init_offset: int = 0, init_body_offset: int = 4, keep_structure: bool = True,
            analyze_dependencies: bool = False):
    """
    Converts the content of the given path.

    The path is expected to be for some python module (either file or folder).

    :param path: The target path.
    :param out: The output folder.
    :param name: The name of the target as store module.
    :param stored_modules: The modules used in renpy are store modules.
    :param level: The init python level.
    :param temp_config: If true, no dumps the configuration if it does not exist.
    :param module: The parent module name.
    :param class_bases: The base classes and their replacements.
    :param init_offset: The times to add a space offset to the init expression.
    :param init_body_offset: The times to add a space offset to the init body.
    :param keep_structure: If true, keeps the structure of the source folder.
    :param analyze_dependencies: Indicates whether the module's internal dependencies are analyzed.
    """
    pass
