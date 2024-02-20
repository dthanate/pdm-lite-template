import os
import tomllib
from decimal import Decimal

from pyproject_metadata import StandardMetadata

from .path_helper import get_project_home


def get_pyproject_standard_metadata() -> StandardMetadata:
    cwd = os.getcwd()
    os.chdir(get_project_home())
    with open("pyproject.toml", "rb") as f:
        parsed_pyproject = tomllib.load(f, parse_float=Decimal)
    metadata = StandardMetadata.from_pyproject(parsed_pyproject)
    os.chdir(cwd)
    return metadata
