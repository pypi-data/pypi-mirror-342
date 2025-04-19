from typing import Generator


def read(path: str, encoding: str = 'utf-8') -> str:
    """
    Opens the file and reads its contents with the given encoding.

    For compatibility with python 2.7, the file is opened in binary read mode (rb)
    and a decoded is made to the content with the encoding passed;
    if this gives an error, the content of the file will be returned only in read mode (r).

    :param path: The target file path.
    :param encoding: The content encoding.
    :return: The file content.
    """
    ...

def write(path: str, content: str, encoding: str = 'utf-8'):
    """
    Opens the file and writes the content with the given encoding.

    For compatibility with python 2.7, the file is opened in binary write mode (wb)
    and a encoded is made to the content with the encoding passed;
    if this gives an error, the content of the file will be written only in write mode (w).

    :param path: The target file path.
    :param content: The content to write.
    :param encoding: The content encoding.
    """
    ...


def mkdirs(path: str, exist_ok: bool = False):
    """
    Creates a directory and its parents if they do not exist.

    :param path: The path to creates.
    :param exist_ok: If True, no exception is raised if the directory already exists.
    """
    ...


def filename(filepath: str) -> str:
    """
    Extracts the name from the path, without extension or parent paths.

    :param filepath: The file path.
    :return: The filename.
    """
    ...


def listfiles(path: str, extensions: tuple[str, ...] = None,
              level: int = None, include_root: bool = False) -> Generator[str]:
    """
    Lists all files in the directory and its subdirectories according its level.

    :param path: The target directory path.
    :param extensions: The file extensions to filter.
    :param level: The depth level to search.
    :param include_root: If true, the path parameter will be included in the result path.
    """
    pass
