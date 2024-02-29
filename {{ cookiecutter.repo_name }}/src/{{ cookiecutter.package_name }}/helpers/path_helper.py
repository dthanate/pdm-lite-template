from os import path
from pathlib import Path
from typing import Final


__PACKAGE_ROOT: Final[str] = path.normpath(path.join(path.dirname(__file__), ".."))


def get_package_root() -> Path:
    """The top directory of the package.

    Returns:
        pathlib.Path object pointing to the correct directory.
    """
    return Path(__PACKAGE_ROOT)
