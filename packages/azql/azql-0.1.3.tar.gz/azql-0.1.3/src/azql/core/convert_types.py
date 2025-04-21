"""
SQL Type Converter Module

This module converts Python types to SQL types for various SQL dialects,
with a focus on TSQL (Microsoft SQL Server).
"""

from typing import Any

import azql.core.dialects as dialects


def convert_to_sql_types(
    column_properties: dict[str, dict[str, Any]],
    dialect: str = "tsql",
) -> dict[str, dict[str, Any]]:
    """
    Convert Python types to SQL types based on the specified SQL dialect.

    Args:
        column_properties: Dictionary of column properties
        dialect: SQL dialect (tsql, mysql, postgresql)

    Returns:
        Dictionary with SQL type information for each column
    """
    dialect = dialect.lower()
    match dialect:
        case "tsql":
            return dialects.tsql.convert_types(column_properties)
        case "mysql":
            return dialects.mysql.convert_types(column_properties)
        case "postgresql":
            return dialects.postgresql.convert_types(column_properties)
        case _:
            msg = f"Unsupported SQL dialect: {dialect}"
            raise ValueError(msg)
