"""
AZQL: Azure Query Language Utilities

# Copyright (c) Markus Feiks
# Licensed under the GNU GENERAL PUBLIC LICENSE Version 3.

AZQL is a tool for converting data files (CSV, JSON)
to SQL DDL (Data Definition Language) scripts. It analyzes data files,
detects data types, and generates appropriate SQL scripts for table creation.
"""

from .convert import convert
from .io import read_csv, read_file, read_json
from .utils import dict_to_args

__all__ = [
    "convert",
    "dict_to_args",
    "read_csv",
    "read_file",
    "read_json",
]
