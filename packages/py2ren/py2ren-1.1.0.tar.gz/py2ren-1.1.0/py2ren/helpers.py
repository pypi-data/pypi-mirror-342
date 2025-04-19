import errno
import os

from .config import NonLoadableConfigurationPath, load, dump, create, Module, FileModule
from .converter.syntax import CodeConverter
from .utils.filepath import listfiles, filename, read, write, mkdirs

__all__ = (
    'get_config',
    'convfolder',
    'convfile',
    'convfilew',
    'convfolderw',
    'convert',
    'convertw',
)


def get_config(path, name=None, stored_modules=None, level=0, temp_config=False, analyze_dependencies=False):
    try:
        return load(path, creates=False)
    except NonLoadableConfigurationPath:
        creates = create if temp_config else dump
        return creates(path, name, stored_modules, level, analyze_dependencies=analyze_dependencies)


def convfilew(path, converter, name=None, level=0, module=None,
              class_bases=None, init_offset=0, init_body_offset=4, ):
    code = read(path)

    return converter.convert(code, name, level, module, class_bases, init_offset, init_body_offset)


def convfile(path, name=None, stored_modules=None, level=0, module=None,
             class_bases=None, temp_config=False, init_offset=0, init_body_offset=4):
    cfg = get_config(path, name, stored_modules, level, temp_config)
    converter = CodeConverter(cfg)
    return convfilew(path, converter, cfg.name, cfg.level, module, class_bases, init_offset, init_body_offset)


def convfolderw(path, converter, class_bases=None, init_offset=0, init_body_offset=4):
    cfg = converter.config
    for filepath in listfiles(path, extensions=(".py",)):
        module = cfg
        parent = cfg.name
        level = cfg.level

        parts = filepath.split(os.path.sep)
        for part in parts[:-1]:
            module = module.modules.get(part, None)
            if not isinstance(module, (Module, FileModule)):
                break
            level = level if module.level is None else module.level
            parent = "{}.{}".format(parent, filename(part))

        if not module:
            continue

        module = module.modules.get(parts[-1], None)
        if module is None or module.ignore:
            continue

        level = level if module.level is None else module.level

        if module.name:
            module_name = module.name
        else:
            module_name = filename(filepath)
            module_name = "" if module_name == "__init__" else module_name.strip("__")

        pt = os.path.join(path, filepath)
        yield filepath, convfilew(pt, converter, module_name, level, parent,
                                  class_bases, init_offset, init_body_offset)


def convfolder(path, name=None, stored_modules=None, level=0, class_bases=None,
               temp_config=False, init_offset=0, init_body_offset=4, analyze_dependencies=False):
    cfg = get_config(path, name, stored_modules, level, temp_config, analyze_dependencies)
    transformer = CodeConverter(cfg)
    return convfolderw(path, transformer, class_bases, init_offset, init_body_offset)


def _write(folder, path, code, keep_structure=True):
    path = os.path.basename(path) if not keep_structure else path
    path, _ = os.path.splitext(path)
    filepath = os.path.join(folder, path + ".rpy")
    if keep_structure:
        mkdirs(os.path.dirname(filepath), exist_ok=True)
    write(filepath, code, )


def convertw(path, out, converter, name=None, level=0, module=None,
             class_bases=None, init_offset=0, init_body_offset=4, keep_structure=True):
    if os.path.isfile(path):
        code = convfilew(path, converter, name, level, module, class_bases, init_offset, init_body_offset)
        mkdirs(out, exist_ok=True)
        _write(out, path, code, keep_structure)
    elif os.path.isdir(path):
        mkdirs(out, exist_ok=True)
        for path, code in convfolderw(path, converter, class_bases, init_offset, init_body_offset):
            _write(out, path, code, keep_structure)
    else:
        raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)


def convert(path, out, name=None, stored_modules=None, level=0, temp_config=False,
            module=None, class_bases=None, init_offset=0, init_body_offset=4, keep_structure=True,
            analyze_dependencies=False):
    config = get_config(path, name, stored_modules, level, temp_config, analyze_dependencies)
    converter = CodeConverter(config)
    convertw(path, out, converter, name, level, module, class_bases, init_offset, init_body_offset, keep_structure)
