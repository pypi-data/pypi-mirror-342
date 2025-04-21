"""
Type Detector Module

This module detects and analyzes data types from input data.
It guesses Python types for columns and analyzes properties like
maximum length, precision, etc.
"""

import re
from typing import Any


def _is_int(value: Any) -> bool:
    """Check if value can be converted to an integer."""
    if isinstance(value, int):
        return True
    if isinstance(value, str):
        return value.isdigit() or (
            value.startswith("-") and value[1:].isdigit()
        )
    return False


def _is_float(value: Any) -> bool:
    """Check if value can be converted to a float."""
    if isinstance(value, int | float):
        return True
    if isinstance(value, str):
        try:
            float(value)
            return True
        except ValueError:
            return False
    return False


def _is_bool(value: Any) -> bool:
    """Check if value represents a boolean."""
    if isinstance(value, bool):
        return True
    if isinstance(value, str):
        lower_val = value.lower()
        return lower_val in ("true", "false", "yes", "no", "y", "n", "1", "0")
    return False


def _is_date(value: Any) -> bool:
    """Check if value represents a date."""
    if isinstance(value, str):
        # ISO date format: YYYY-MM-DD
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        # Simple datetime formats
        datetime_pattern = r"^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(:\d{2})?$"
        return bool(
            re.match(date_pattern, value) or re.match(datetime_pattern, value),
        )
    return False


def detect_column_type(values: list[Any]) -> str:
    """
    Detect the most appropriate Python type for a column.

    Args:
        values: List of values for a column

    Returns:
        String representing the Python type
    """
    non_none_values = [v for v in values if v is not None and v != ""]

    if not non_none_values:
        return "str"  # Default to string for empty columns

    # Check if all values are the same type
    if all(_is_bool(v) for v in non_none_values):
        return "bool"
    if all(_is_int(v) for v in non_none_values):
        return "int"
    if all(_is_float(v) for v in non_none_values):
        return "float"
    if all(_is_date(v) for v in non_none_values):
        return "date"

    # Default to string if mixed or no specific type detected
    return "str"


def detect_types(
    data: list[dict[str, Any]],
    sample_size: int = 1000,
) -> dict[str, str]:
    """
    Detect types for all columns in the data.

    Args:
        data: List of dictionaries representing rows of data
        sample_size: Number of rows to sample for type detection

    Returns:
        Dictionary mapping column names to detected Python types
    """
    if not data:
        return {}

    # Get all column names from the first row
    columns = list(data[0].keys())

    # Sample rows for type detection
    sample_data = data[:sample_size]

    # Detect types for each column
    column_types = {}
    for column in columns:
        values = [row.get(column) for row in sample_data]
        column_types[column] = detect_column_type(values)

    return column_types


def analyze_column_properties(
    data: list[dict[str, Any]],
    column_types: dict[str, str],
) -> dict[str, dict[str, Any]]:
    """
    Analyze properties of columns like max length, nullability, etc.

    Args:
        data: List of dictionaries representing rows of data
        column_types: Dictionary mapping column names to detected Python types

    Returns:
        Dictionary mapping column names to their properties
    """
    column_properties = {}

    for column, data_type in column_types.items():
        properties = {
            "type": data_type,
            "has_null": False,
            "max_length": 0,
            "precision": 0,
            "scale": 0,
        }

        for row in data:
            value = row.get(column)

            # Check for nulls
            if value is None or value == "":
                properties["has_null"] = True
                continue

            # Analyze string length
            if data_type == "str":
                value_str = str(value)
                properties["max_length"] = max(
                    properties["max_length"],
                    len(value_str),
                )

            # Analyze float precision and scale
            elif data_type == "float":
                try:
                    value_str = str(float(value))
                    if "." in value_str:
                        int_part, dec_part = value_str.split(".")
                        int_length = len(int_part.replace("-", ""))
                        dec_length = len(dec_part)
                        total_length = int_length + dec_length

                        properties["precision"] = max(
                            properties["precision"],
                            total_length,
                        )
                        properties["scale"] = max(
                            properties["scale"],
                            dec_length,
                        )
                except (ValueError, TypeError):
                    pass

        column_properties[column] = properties

    return column_properties
