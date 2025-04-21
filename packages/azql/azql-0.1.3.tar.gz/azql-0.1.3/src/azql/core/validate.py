"""
Data Validator Module

This module validates data integrity by ensuring that all values
in a column have consistent types or are None.
"""

from typing import Any


def validate_data_integrity(
    data: list[dict[str, Any]],
    column_types: dict[str, str],
) -> dict[str, Any]:
    """
    Validate data integrity across all columns.

    Checks that:
    - Every data point in a column has either the same data type or is None

    Args:
        data: List of dictionaries representing rows of data
        column_types: Dictionary mapping column names to detected Python types

    Returns:
        Dictionary with validation results
    """
    issues = []
    is_valid = True

    type_checkers = {
        "int": lambda v: v is None
        or v == ""
        or isinstance(v, int)
        or (
            isinstance(v, str)
            and (v.isdigit() or (v.startswith("-") and v[1:].isdigit()))
        ),
        "float": lambda v: v is None
        or v == ""
        or isinstance(v, int | float)
        or (isinstance(v, str) and _is_valid_float(v)),
        "bool": lambda v: v is None
        or v == ""
        or isinstance(v, bool)
        or (
            isinstance(v, str)
            and v.lower() in ("true", "false", "yes", "no", "y", "n", "1", "0")
        ),
        "str": lambda v: v is None or v == "" or isinstance(v, str),
        "date": lambda v: v is None or v == "" or isinstance(v, str),
    }

    for column, expected_type in column_types.items():
        type_checker = type_checkers.get(expected_type)
        if not type_checker:
            issues.append(
                f"Unknown column type '{expected_type}' for column '{column}'",
            )
            is_valid = False
            continue

        invalid_rows = []
        for i, row in enumerate(data):
            value = row.get(column)
            if not type_checker(value):
                invalid_rows.append(i + 1)  # +1 for human-readable row numbers
                if (
                    len(invalid_rows) > 5
                ):  # Limit the number of reported invalid rows
                    break

        if invalid_rows:
            if len(invalid_rows) > 5:
                issue_msg = (
                    f"Column '{column}' has inconsistent data types. "
                    f"First 5 invalid rows: {invalid_rows[:5]} and more."
                )
            else:
                issue_msg = (
                    f"Column '{column}' has inconsistent data types. "
                    f"Invalid rows: {invalid_rows}"
                )

            issues.append(issue_msg)
            is_valid = False

    return {
        "is_valid": is_valid,
        "issues": issues,
    }


def _is_valid_float(value: str) -> bool:
    """Check if a string can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False
