#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package initialization file for pylatinize string formatting library.

This file serves as the entry point for the pylatinize package. It exposes
the core functionality (PyLatinize class, Normalization enum) and the
predefined mapping dictionaries (default_mapping, emoji_mapping) directly
at the package level, allowing users to import them conveniently using
`from pylatinize import ...`. It also defines package-level metadata
like the list of public objects and the version number.
"""

from .core import PyLatinize, Normalization
from .mappings import default_mapping, emoji_mapping

__all__ = ["PyLatinize", "Normalization", "default_mapping", "emoji_mapping"]
__version__ = "0.0.1"
