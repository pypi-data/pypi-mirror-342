import ast
import os
from ast import ImportFrom, Import

from ..utils import self
from ..utils.filepath import read
from ..utils.iter import itermap


def _alias_as_expression(alias):
    if not alias.asname:
        return alias.name
    return "{} as {}".format(alias.name, alias.asname)


def path2import(path):
    path, _ = os.path.splitext(path)
    return path.replace(os.path.sep, '.')


def import2path(imp):
    return imp.replace(".", os.path.sep)

def i2import(iterable):
    return ".".join(itermap(self, iterable))


def get_internals(filepath, root, package=None):
    code = read(filepath)
    if not package:
        package = os.path.split(filepath)[0]

    imports = set()
    modules = os.path.relpath(filepath, root).split(os.path.sep)
    tree = ast.parse(code)
    pkg = i2import((package, ''))

    def add_full(module):
        if not module.startswith(pkg):
            return
        imp = module.replace(pkg, "")
        if os.path.isfile(os.path.join(root, import2path(imp), "__init__.py")):
            imp = i2import((imp, "__init__"))
        imports.add(imp)

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.col_offset:
                continue

            if not node.level:
                add_full(node.module)
                continue

            parent = i2import(modules[:-node.level])
            if node.module:
                imp = node.module
                if parent:
                    imp = i2import((parent, imp))
                elif os.path.isfile(os.path.join(root, import2path(imp), "__init__.py")):
                    imp = i2import((imp, "__init__"))
                imports.add(imp)
            elif parent:
                imports.update(i2import((parent, n.name)) for n in node.names)
            else:
                imports.add("__init__")
        elif isinstance(node, ast.Import) and not node.col_offset:
            for name in node.names:
                add_full(name.name)


    return tuple(imports)

def as_expression(node):
    offset = " " * node.col_offset
    source = "import {}".format(
        ", ".join(itermap(_alias_as_expression, node.names))
    )
    if isinstance(node, ImportFrom):
        return offset + "from {}{} {}".format(
            "." * node.level,
            node.module if node.module else "",
            source
        )

    return offset + source


def create_store_import(names, lineno, col_offset=0):
    return ImportFrom(
        module="store",
        names=names,
        lineno=lineno,
        col_offset=col_offset,
        level=0,
    )


def as_store_import(imp, parent_module=None):
    store = "store"
    if parent_module:
        store += ".{}".format(parent_module)
    if isinstance(imp, ImportFrom):
        imp = ImportFrom(
            module="{}.{}".format(store, imp.module) if imp.module else store,
            names=imp.names,
            lineno=imp.lineno,
            level=0,
            col_offset=imp.col_offset,
        )
        return imp
    elif isinstance(imp, Import):
        return ImportFrom(
            module=store,
            names=imp.names,
            lineno=imp.lineno,
            level=0,
            col_offset=imp.col_offset,
        )
    return imp
