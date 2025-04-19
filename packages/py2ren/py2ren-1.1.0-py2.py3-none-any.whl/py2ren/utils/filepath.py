import errno
import os


def read(path, encoding='utf-8'):
    try:
        with open(path, 'rb') as f:
            return f.read().decode(encoding)
    except UnicodeEncodeError:
        with open(path, 'r') as f:
            return f.read()


def write(path, content, encoding='utf-8'):
    try:
        with open(path, 'wb') as f:
            f.write(content.encode(encoding))
    except UnicodeEncodeError:
        with open(path, 'w') as f:
            f.write(content)


def mkdirs(path, exist_ok=False):
    path = os.path.normpath(path)
    try:
        return os.makedirs(path, exist_ok=exist_ok)
    except TypeError:
        pass

    try:
        return os.makedirs(path)
    except OSError as e:
        if not exist_ok or e.errno != errno.EEXIST:
            raise


def filename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def listfiles(path, extensions=None, level=None, include_root=False):
    if not os.path.isdir(path):
        return

    def _check_name(_):
        return True

    def _check_level(_):
        return False

    if extensions:
        def _check_name(s): return s.endswith(extensions)

    if level is not None:
        def _check_level(s):
            return len(s.split(os.path.sep)) >= level

    _normpath = os.path.normpath(path)
    for (root, _, filenames) in os.walk(_normpath):
        _root = root.replace(_normpath, "")
        if _check_level(_root):
            continue
        for name in filenames:
            if _check_name(name):
                if include_root:
                    yield os.path.join(root, name)
                else:
                    yield name if root == _normpath else os.path.join(_root[1:], name)
