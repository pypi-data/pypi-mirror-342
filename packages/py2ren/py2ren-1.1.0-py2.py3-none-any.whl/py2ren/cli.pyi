from typing import Union

from py2ren.config import ModuleConfig, FileConfig


class Args:
    """
    The cli args class.
    """

    path: str
    config: Union[str, ModuleConfig, FileConfig]
    out: str
    init_level: int
    name: str
    no_keep_structure: bool
    force_config: bool
    analyze_dependencies: bool

    def __init__(self, path: str, out: str = None, config: Union[str, ModuleConfig, FileConfig] = None,
                 init_level: int = None, name: str = None,
                 no_keep_structure: bool = False, force_config: bool = False, analyze_dependencies: bool = False):
        """
        :param path: The target path.
        :param out: The output folder.
        :param config: The config path or instance.
        :param init_level: The init python level.
        :param name: The name of the target as store module.
        :param no_keep_structure: If true, no keeps the structure of the source folder.
        :param force_config: If true, creates and dumps a new configuration.
        :param analyze_dependencies: Indicates whether the module's internal dependencies are analyzed.
        """
        pass


def parse_args() -> Args:
    """
    Parses the cli args using argparse

    :return: The parsed args.
    """
    pass


def main(args: Args = None):
    """
    The main entry point for the cli program.

    :param args: The cli args.

    :see: :func:`.parse_args`, :func:`.helpers.convert`
    """
    pass
