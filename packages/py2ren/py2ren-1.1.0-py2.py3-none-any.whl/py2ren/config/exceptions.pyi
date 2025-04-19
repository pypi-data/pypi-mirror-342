from typing import Any


class NonLoadableSourceConfigurationPath(Exception):
    """
    Raised when the target path cannot be loaded.

    The path is expected to be for some python module (either file or folder)
    """

    def __init__(self: Any, filepath: str):
        """
        :param filepath: The target filepath.
        """
        ...


class NonLoadableConfigurationPath(Exception):
    """
    Raised when the path cannot be loaded.

    The path is expected to be a json file.
    """

    def __init__(self: Any, filepath: str):
        """
        :param filepath: the configuration filepath.
        """
        ...
