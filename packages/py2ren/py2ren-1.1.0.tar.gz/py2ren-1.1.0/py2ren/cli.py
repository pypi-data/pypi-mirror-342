import os

from . import config
from .converter.syntax import CodeConverter
from .helpers import get_config, convertw
from .utils.filepath import filename

__all__ = (
    'parse_args',
    'main',
    'Args'
)


class Args(object):
    __slots__ = (
        'path', 'config', 'out',
        'init_level', 'name', 'no_keep_structure',
        'force_config', 'analyze_dependencies',
    )

    def __init__(self, path, out=None, config=None, init_level=None,
                 name=None, no_keep_structure=False, force_config=False, analyze_dependencies=False):
        self.path = path
        self.config = config
        self.out = out
        self.init_level = init_level
        self.name = name
        self.no_keep_structure = no_keep_structure
        self.force_config = force_config
        self.analyze_dependencies = analyze_dependencies


def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Convert python files into ren'py format.")

    # Required positional argument
    parser.add_argument("path", type=str, help="target transformation path.")

    # Optional arguments
    parser.add_argument("-o", "--out", type=str, help="the output folder for the transformation result.")
    parser.add_argument("-n", "--name", type=str, help="the base module name, must not contain spaces.")
    parser.add_argument("-il", "--init-level", type=int, help="the init level for the init expression.")

    parser.add_argument("-c", "--config", type=str, help="path to the configuration file.")
    # Boolean flags
    parser.add_argument("-nks", "--no-keep-structure", action="store_true", default=False,
                        help="flag to disable keeping the module structure.")
    parser.add_argument("-fc", "--force-config", action="store_true", default=False,
                        help="flag to force the creation of the configuration file.")

    parser.add_argument('-ad', '--analyze-dependencies', action="store_true", default=False,
                        help="flag to analyze dependencies when the config is created.")
    return parser.parse_args()


def main(args=None):
    if args is None:
        args = parse_args()

    args.path = os.path.abspath(args.path)

    if args.out is None:
        args.out = args.path if os.path.isdir(args.path) else os.path.dirname(args.path)
    else:
        args.out = os.path.abspath(args.out)

    if not args.name:
        args.name = filename(args.path)

    if not args.force_config:
        if args.config is None:
            args.config = get_config(args.path, args.name, level=args.init_level, analyze_dependencies=args.analyze_dependencies)
        elif isinstance(args.config, str):
            args.config = config.load_file(args.config)
        elif not isinstance(args.config, config.FileConfig):
            args.config = config.load(args.path)
    else:
        args.config = config.dump(args.path, args.name, level=args.init_level, analyze_dependencies=args.analyze_dependencies)

    if args.init_level is None:
        args.init_level = args.config.level

    converter = CodeConverter(args.config)

    convertw(args.path, args.out, converter, args.name, args.init_level, keep_structure=not args.no_keep_structure)
