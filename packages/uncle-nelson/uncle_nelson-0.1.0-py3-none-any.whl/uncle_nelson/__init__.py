"""
uncle-nelson
=============
Library to calculate mixes for the game Schedule 1.

Copyright (c) 2025-present codeofandrin
MIT License. See LICENSE for details
"""

__version__ = "0.1.0"
__author__ = "codeofandrin"
__copyright__ = "Copyright (c) 2025-present codeofandrin"
__license__ = "MIT"

from typing import NamedTuple, Literal

from .mix import *
from .enums import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    patch: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info = VersionInfo(major=0, minor=1, patch=0, releaselevel="final", serial=0)

del VersionInfo, NamedTuple, Literal
