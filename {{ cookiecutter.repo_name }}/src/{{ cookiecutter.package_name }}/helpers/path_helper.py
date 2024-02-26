from os import path
from pathlib import Path
from typing import Final


PACKAGE_ROOT: Final[str] = path.normpath(path.join(path.dirname(__file__), ".."))


def get_package_root() -> Path:
    return Path(PACKAGE_ROOT)
