import ast
import re

from ast import ClassDef

__all__ = ('KNOWN_BASES', 'get_bases', 'replace', 'add_replacement', 'ClassDef', 'get_replacement')

from ..utils.iter import itermap

KNOWN_BASES = {name: "python_{}".format(name) for name in ("object", "list", "tuple", "dict")}


def _as_replacement_name(target, name, ):
    return ast.Name(id=KNOWN_BASES.get(name, name), ctx=target.ctx)


def get_bases(node, bases=None):
    if not bases or not isinstance(node, dict):
        bases = KNOWN_BASES

    if not isinstance(node, ClassDef):
        raise TypeError('Node must be a ClassDef.')

    for name in node.bases:
        if isinstance(name, ast.Name) and name.id in bases:
            yield name
        elif isinstance(name, ast.Call) and name.func.id in bases:
            yield name.func


def get_regex(node, bases=None):
    # ([,(\s]\b)(object|list|tl)(\b[,)\s])
    bases = "|".join(itermap(re.escape, (name.id for name in get_bases(node, bases))))
    return r"([,(\s]\b)({})(\b[,)\s])".format(bases) if bases else None


def replace(source, node, bases=None):
    pattern = get_regex(node, bases)

    def replacefn(match):
        base = match.group(2)
        return match.group(1) + (bases or KNOWN_BASES).get(base, base)  + match.group(3)

    return re.sub(pattern, replacefn, source) if pattern else source


def add_replacement(python_name, renpy_name):
    KNOWN_BASES.setdefault(python_name, renpy_name)


def get_replacement(python_name, ):
    return KNOWN_BASES.get(python_name, python_name)
