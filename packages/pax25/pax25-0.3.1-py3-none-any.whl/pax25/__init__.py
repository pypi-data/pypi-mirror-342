"""
Quick and common client imports for Pax25.
"""

import tomllib
from pathlib import Path

from . import interfaces
from .applications.application import Application
from .station import Station

with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as package_file:
    __version__ = tuple(tomllib.load(package_file)["project"]["version"].split("."))

__all__ = ["Station", "Application", "interfaces"]
