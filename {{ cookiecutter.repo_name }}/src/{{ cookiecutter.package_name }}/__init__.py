from typing import Final

from .helpers.pyproject_helper import get_pyproject_standard_metadata

__version__: Final[str] = str(get_pyproject_standard_metadata().version)
