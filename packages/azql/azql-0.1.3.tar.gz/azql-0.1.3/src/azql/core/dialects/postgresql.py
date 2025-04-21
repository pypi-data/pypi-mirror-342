"""
DDL Generator Module

This module generates SQL DDL (Data Definition Language) scripts
from column type information.
"""

from typing import Any

from ...core.styles import Styles
from ...utils import round_up_to_nearest_multiple


def ddl(
    table_name: str,
    schema: str,
    column_types: dict[str, dict[str, Any]],
    drop_table: bool = False,
    style: str = "input",
) -> str:
    """
    Generate PostgreSQL DDL script.

    Args:
        table_name: Name of the table to create
        schema: Schema name
        column_types: Dictionary with SQL type information for each column
        drop_table: Whether to include a DROP TABLE statement

    Returns:
        PostgreSQL DDL script as a string
    """
    # Format the CREATE TABLE statement
    ddl_lines = [
        "-- Auto-generated PostgreSQL DDL script",
        "",
    ]

    if drop_table:
        ddl_lines.append(f'DROP TABLE IF EXISTS "{schema}"."{table_name}";')
        ddl_lines.append("")

    # Use CREATE TABLE IF NOT EXISTS for PostgreSQL
    ddl_lines.append(f'CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}" (')

    styler = None
    if style and style in ["camel", "pascal", "snake"]:
        styler = Styles.get(style)

    # Add column definitions
    column_defs = []
    for i, (column, info) in enumerate(column_types.items()):
        nullable_str = "NULL" if info["nullable"] else "NOT NULL"
        col_name = styler(column) if styler else column
        if i == 0:
            column_def = f'    "{col_name}" {info["sql_type"]} {nullable_str}'
        else:
            column_def = f'  "{col_name}" {info["sql_type"]} {nullable_str}'
        column_defs.append(column_def)

    # Format column definitions with comma-first style
    if column_defs:
        ddl_lines.append(column_defs[0])
        for col_def in column_defs[1:]:
            ddl_lines.append(f"  , {col_def.strip()}")

    # Close CREATE TABLE statement
    ddl_lines.append(");")

    # Convert SQL keywords to UPPERCASE
    final_ddl = "\n".join(ddl_lines)
    sql_keywords = [
        "CREATE TABLE",
        "DROP TABLE",
        "IF",
        "EXISTS",
        "NOT",
        "NULL",
    ]
    for keyword in sql_keywords:
        final_ddl = final_ddl.replace(keyword, keyword.upper())

    return final_ddl


def convert_types(
    column_properties: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Convert Python types to PostgreSQL types.

    Args:
        column_properties: Dictionary of column properties

    Returns:
        Dictionary with SQL type information for each column
    """
    sql_column_types = {}

    for column, properties in column_properties.items():
        python_type = properties["type"]
        has_null = properties["has_null"]

        sql_type_info = {
            "name": column,
            "nullable": has_null,
            "sql_type": "",
        }

        if python_type == "int":
            sql_type_info["sql_type"] = "INTEGER"

        elif python_type == "float":
            precision = properties["precision"]
            scale = properties["scale"]

            precision = max(precision, scale + 1, 1)
            scale = max(scale, 0)

            sql_type_info["sql_type"] = f"NUMERIC({precision}, {scale})"

        elif python_type == "bool":
            sql_type_info["sql_type"] = "BOOLEAN"

        elif python_type == "date":
            sql_type_info["sql_type"] = "TIMESTAMP"

        else:  # Default to string
            max_length = properties["max_length"]

            # Round up to the nearest multiple of 5
            if max_length > 0:
                max_length = round_up_to_nearest_multiple(max_length, 5)

            if max_length > 10485760:  # Approx limit for VARCHAR
                sql_type_info["sql_type"] = "TEXT"
            else:
                max_length = max(max_length, 1)
                sql_type_info["sql_type"] = f"VARCHAR({max_length})"

        sql_column_types[column] = sql_type_info

    return sql_column_types
