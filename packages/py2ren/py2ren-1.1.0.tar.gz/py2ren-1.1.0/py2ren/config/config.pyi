from typing import Type, TypeVar, Any, Union, Iterable

_T = TypeVar('_T')


class Init(object):
    """
    The base class for the configurations.
    """
    __slots__ = ()

    def __init__(self: Any, name: str = None, level: int = 0, class_bases: dict[str, str] = None): pass

    # @classmethod
    # def _get_params(cls, dct) -> dict[str, Any]: pass

    @property
    def name(self: Any) -> str:
        """
        The name of the configuration.

        :getter: Returns the name of the configuration.
        """
        pass

    @property
    def level(self: Any) -> int:
        """
        The init level of the configuration.

        :getter: Returns the init level of the configuration.
        """
        pass

    @property
    def class_bases(self: Any) -> dict[str, str]:
        """
        The class bases of the configuration.

        :getter: Returns the class bases of the configuration.
        """
        pass

    @classmethod
    def from_dict(cls: Type[_T], dct: dict[str, Any]) -> _T:
        """
        Creates a new instance of the configuration.

        :param dct: The json source.
        """
        pass

    def to_dict(self: Any) -> dict[str, Any]:
        """
        Converts the configuration to a json.
        """
        pass


class FileModule(Init):
    """
    The configuration for a file module.
    """
    __slots__ = ()

    def __init__(self: Any, name: str = None, level: int = 0, class_bases: dict[str, str] = None,
                 ignore: bool = False):
        """
        :param name: The name of the file as store module.
        :param level: The init python level.
        :param class_bases: The base classes and their replacements.
        :param ignore: If true, the file will be ignored.
        """
        pass

    @property
    def ignore(self: Any) -> bool:
        """
        The ignore flag.
        """
        pass


class Module(FileModule):
    """
    The configuration for a module.
    """

    __slots__ = ()

    def __init__(self: Any, name: str = None, modules: dict[str, Union['Module', 'FileModule']] = None,
                 level: int = 0, class_bases: dict[str, str] = None, ignore: bool = False):
        """
        :param name: The name of the module as store module.
        :param modules: The modules configuration of the module.
        :param level: The init python level.
        :param class_bases: The base classes and their replacements.
        :param ignore: If true, the module will be ignored.
        """
        pass

    @property
    def modules(self: Any) -> dict[str, Union['Module', 'FileModule']]:
        """
        The module configurations of the module.

        :getter: Returns the module configurations of the module.
        """
        pass

    @staticmethod
    def map_modules(modules: dict[str, Any]) -> dict[str, Union['Module', 'FileModule']]:
        """
        Maps the source as module or file module configurations.

        :param modules: The object with the json configurations.
        """
        pass


class FileConfig(Init):
    """
    The root configuration for a file.
    """
    __slots__ = ()

    def __init__(self: Any, name: str = None, stored_modules: Iterable[str] = None,
                 level: int = 0, class_bases: dict[str, str] = None):
        """
        :param name: The name of the file as store module.
        :param stored_modules: The modules used in renpy are store modules.
        :param level: The init python level.
        :param class_bases: The base classes and their replacements.
        """
        pass

    @property
    def stored_modules(self: Any) -> tuple[str, ...]:
        """
        The stored modules of the file.

        :getter: Returns the stored modules of the file.
        """
        pass

    @classmethod
    def from_file(cls: Type[_T], path: str) -> _T:
        """
        Creates a new instance of the configuration from a json file.

        :param path: The path for the json file configuration.
        """
        pass


class ModuleConfig(FileConfig):
    """
    The root configuration for a module.
    """
    __slots__ = ()

    def __init__(self: Any, name: str = None, stored_modules: Iterable[str] = None,
                 modules: dict[str, Union[Module, FileModule]] = None, level: int = 0,
                 class_bases: dict[str, str] = None):
        """
        :param name: The name of the module as store module.
        :param stored_modules: The modules in renpy are store modules.
        :param modules: The modules configuration of the module.
        :param level: The init python level.
        :param class_bases: The base classes and their replacements.
        """
        pass

    @property
    def modules(self: Any) -> dict[str, Union[Module, FileModule]]:
        """
        The module configurations of the module.

        :getter: Returns the module configurations of the module.
        """
        pass


def load_dict(source: dict[str, Any]) -> Union[ModuleConfig, FileConfig]:
    """
    Loads the configuration for the given source.

    If the source does not contain “modules” or it is empty, it will be considered a file config.

    :example:
        >>> cfg = load_dict({"name": "sample", "classBases": {}}) # FileConfig
        >>> cfg = load_dict({"name": "sample", "modules": {}, "classBases": {}}) # FileConfig
        >>> cfg = load_dict({"name": "sample", "modules": {"module": {}}, "classBases": {}}) # ModuleConfig

    :param source: The json source.
    """
    pass


def load_file(path: str) -> Union[ModuleConfig, FileConfig]:
    """
    Loads the configuration for the given path source.

    Path is expected to be a json file.

    :param path: The path for the json file configuration.
    :see: :func:`.load_dict`
    """
    pass


def load(path: str, creates: bool = True) -> Union[ModuleConfig, FileConfig]:
    """
    Loads the configuration for the given path.

    The path is expected to be for some python module (either file or folder),
    since it will be joined with the name `py2ren.config.json`.

    :param path: The target path.
    :param creates: If true, creates a new configuration file if it does not exist.
    :raise NonLoadableSourceConfigurationPath: If the path is not loadable.
    """
    ...


def create(path: str, name: str = None, store_modules: Iterable[str] = None,
           level: int = 0, class_bases: dict[str, str] = None,
           analyze_dependencies: bool = False) -> Union[ModuleConfig, FileConfig]:
    """
    Creates a configuration for the given path.

    :param path: The target path.
    :param name: The name of the target as store module.
    :param store_modules: The modules used in renpy are store modules.
    :param level: The init python level.
    :param class_bases: The base classes and their replacements.
    :param analyze_dependencies: Indicates whether the module's internal dependencies are analyzed.

    Notes:
        * Analyzing internal dependencies creates a better structure for init levels.
        * Analyzing internal dependencies may delay the creation of the configuration, since all module files are parsed and analyzed.
    """
    ...


def dump_config(folder: str, config: Union[ModuleConfig, FileConfig]):
    """
    Dumps the configuration to the given folder.

    :param folder: The out folder.
    :param config: The configuration.
    """
    pass


def dump(path: str, name: str = None, store_modules: Iterable[str] = None,
         level: int = 0, class_bases: dict[str, str] = None,
         analyze_dependencies: bool = False) -> Union[ModuleConfig, FileConfig]:
    """
    Creates and dumps the configuration for the given path.

    :param path: The target path.
    :param name: The name of the target as store module.
    :param store_modules: The modules used in renpy are store modules.
    :param level: The init python level.
    :param class_bases: The base classes and their replacements.
    :param analyze_dependencies: Indicates whether the module's internal dependencies are analyzed.

    Notes:
        * Analyzing internal dependencies creates a better structure for init levels.
        * Analyzing internal dependencies may delay the creation of the configuration, since all module files are parsed and analyzed.

    :return: The created configuration.
    """
    pass
