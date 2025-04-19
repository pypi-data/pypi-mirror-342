import ast
import re

from . import imports, bases
from ..utils import strip_indexes, trymap
from ..utils.iter import itermap, first

FORBIDDEN_INIT = (
    'image', 'python',
)


def _check_remove_indexes(lines, lineno, source, indexes):
    offset = source.count("\\")

    while offset:
        indexes.append(lineno)
        offset = lines[lineno].count("\\")
        lineno += 1


def _class_lineno(lines, node):
    lineno = node.lineno
    if not node.decorator_list:
        return lineno

    lineno += len(node.decorator_list)
    match = re.match(r"\bclass\s+?{}\b".format(node.name), lines[lineno - 1])
    return lineno if match else node.lineno


class CodeConverter(object):
    __slots__ = ('_config',)

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        return self._config

    def _convert_import(self, node):
        stores = tuple((i, name) for i, name in enumerate(node.names)
                       if name.name in self.config.stored_modules or
                       first(name.name.split('.')) in self.config.stored_modules)

        if stores and len(stores) == len(node.names):
            return [imports.as_store_import(node)]
        elif not stores:
            return [node]

        strip_indexes(node.names, (index for index, _ in stores))
        return (
            node,
            imports.create_store_import(
                names=[name for _, name in stores],
                lineno=node.lineno,
                col_offset=node.col_offset,
            )
        )

    def _convert_import_from(self, node, module=None):
        if node.module and node.module.split('.')[0] in self.config.stored_modules:
            return (imports.as_store_import(node),)
        elif node.level and module:
            if node.level > 1:
                parts = module.split('.')
                if len(parts) < node.level:
                    return (node,)
                module = ".".join(parts[:-(node.level - 1)])
            return (imports.as_store_import(node, module),)
        return (node,)

    def _get_init_expression(self, name=None, level=None, module=None):
        name = self.config.name if name is None else name
        level = self.config.level if level is None else level

        name = name.strip() if name else ''
        module = module.strip() if module else ''
        if not module and not name:
            raise TypeError("Cannot creates an init python expression without a module name or a name")

        level = trymap(int, level, )

        if name and module:
            name = "." + name

        names = name.split(".")
        for it in names:
            if it in FORBIDDEN_INIT:
                raise NameError("The keyword '{}' is forbidden in init python expression".format(it))
        return "init{} python in{}{}".format(
            " {}".format(level) if level else "",
            " {}".format(module),
            name
        )

    def _convert_bases_expr(self, lines, node, remove_indexes, class_bases=None, body_new_line="\n"):
        lineno = _class_lineno(lines, node)
        source = lines[lineno - 1]

        lines[lineno - 1] = bases.replace(source, node, class_bases or self.config.class_bases)

        _check_remove_indexes(lines, lineno, source, remove_indexes)

    def _convert_imports_expr(self, lines, node, remove_indexes, module=None, body_new_line="\n"):
        lineno = node.lineno
        source = lines[lineno - 1]
        lines[lineno - 1] = body_new_line.join(itermap(imports.as_expression, self.convert_imports(node, module)))

        _check_remove_indexes(lines, lineno, source, remove_indexes)

    def _convert_node_expr(self, lines, node, remove_indexes, body_new_line="\n"):
        pass

    def convert_imports(self, node, module=None):
        if isinstance(node, imports.ImportFrom):
            return self._convert_import_from(node, module)
        elif isinstance(node, imports.Import):
            return self._convert_import(node)

        return [node]

    def convert_simple(self, code, module=None, class_bases=None, body_new_line="\n"):
        lines = code.splitlines()
        remove_indexes = []

        three = ast.parse(code)
        for node in ast.walk(three):
            if isinstance(node, (imports.ImportFrom, imports.Import)):
                self._convert_imports_expr(lines, node, remove_indexes, module, body_new_line)
            elif isinstance(node, bases.ClassDef):
                self._convert_bases_expr(lines, node, remove_indexes, class_bases, body_new_line)
            else:
                self._convert_node_expr(lines, node, remove_indexes, body_new_line)

        strip_indexes(lines, remove_indexes)
        return body_new_line.join(lines)

    def convert(self, code, name=None, level=None, module=None,
                class_bases=None, init_offset=0, init_body_offset=4):

        body_new_line = "\n" + (" " * init_body_offset)

        code = self.convert_simple(code, module, class_bases, body_new_line)
        init_offset = " " * init_offset
        return "{}{}\n{}{}:{}{}".format(
            init_offset,
            "# transformation made by py2ren. https://github.com/yoimerdr/py2ren",
            init_offset,
            self._get_init_expression(name, level, module),
            body_new_line,
            code if code else "pass"
        )
