"""
This module provides functions for reading data from JSON and CSV files.
"""

import csv
import json
from pathlib import Path
from typing import Any

from ..config import ENCODING
from ..utils import guess_csv_delimiter


def get_options(defaults: dict, **kwargs):
    """
    Update default options with provided keyword arguments.

    Args:
        defaults: A dictionary of default options.
        **kwargs: Keyword arguments to override defaults.

    Returns:
        The updated dictionary of options.
    """
    for key in set(defaults).intersection(kwargs):
        defaults[key] = kwargs.pop(key)
    return defaults


def read_json(path: Path, **kwargs) -> list[dict[str, Any]]:
    """
    Read data from a JSON file.

    Args:
        path: The path to the JSON file.
        **kwargs: Additional keyword arguments passed to json.load.

    Returns:
        A list of dictionaries representing the JSON data.
    """

    defaults = {
        "cls": None,
        "object_hook": None,
        "parse_float": None,
        "parse_int": None,
        "parse_constant": None,
        "object_pairs_hook": None,
    }

    options = get_options(defaults, **kwargs)

    with open(path, encoding=ENCODING) as file:
        return json.load(file, **options)


def read_csv(path: Path, **kwargs) -> list[dict[str, Any]]:
    """
    Read data from a CSV file.

    Args:
        path: The path to the CSV file.
        **kwargs: Additional keyword arguments passed to csv.DictReader.

    Returns:
        A list of dictionaries representing the CSV data.
    """

    delimiter = guess_csv_delimiter(path)

    # defaults from csv.DictReader
    defaults = {
        "restkey": None,
        "restval": None,
        "dialect": "excel",
        "delimiter": delimiter,
        "quotechar": '"',
        "escapechar": None,
        "doublequote": True,
        "skipinitialspace": False,
        "lineterminator": "\r\n",
        "quoting": 0,
        "strict": False,
    }

    # extract the valid parameters from kwargs
    options = get_options(defaults, **kwargs)
    with open(path, encoding=ENCODING, newline="") as file:
        return list(csv.DictReader(file, **options))


def read_file(file_path: str | Path, **kwargs) -> list[dict[str, Any]]:
    """
    Read data from a file based on its extension (JSON or CSV).

    Args:
        file_path: The path to the data file (string or Path object).
        **kwargs: Additional keyword arguments passed to the specific reader
                  (read_json or read_csv).

    Returns:
        A list of dictionaries representing the data read from the file.

    Raises:
        ValueError: If the file format is unsupported.
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path
    ext = path.suffix.lower()
    match ext:
        case ".json":
            reader = read_json
        case ".csv":
            reader = read_csv
        case ".tsv":
            reader = read_csv
        case _:
            msg = f"Unsupported file format: {ext}"
            raise ValueError(msg)
    return reader(path, **kwargs)
