import os
from pathlib import Path
from typing import Final


PROJECT_HOME: Final[str] = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../.."))
PACKAGE_NAME: Final[str] = "{{ cookiecutter.package_name }}"


def get_project_home() -> Path:
    return Path(PROJECT_HOME)


def get_package_root() -> Path:
    return Path(PROJECT_HOME).joinpath("src").joinpath(PACKAGE_NAME)
