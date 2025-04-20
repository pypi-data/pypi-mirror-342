"""Termis - iTerm2 automation package."""

from .core.termis_app import TermisApp
from .utils.constants import VERSION

__version__ = VERSION
__all__ = ['TermisApp', 'VERSION']
