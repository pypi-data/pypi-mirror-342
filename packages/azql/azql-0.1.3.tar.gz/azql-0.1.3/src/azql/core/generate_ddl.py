"""
DDL Generator Module

This module generates SQL DDL (Data Definition Language) scripts
from column type information.
"""

from typing import TYPE_CHECKING

import azql.core.dialects as dialects

if TYPE_CHECKING:
    from azql.core.models import DDLParams


def generate_ddl_script(
    table_name: str,
    schema: str,
    column_types: dict[str, str],
    dialect: str = "tsql",
    style: str = "input",
    drop_table: bool = False,
) -> str:
    """Generate a SQL DDL script for creating a table.

    Args:
        table_name: Name of the SQL table to create.
        schema: SQL schema name.
        column_types: Dictionary mapping column names to SQL types.
        dialect: SQL dialect (default: tsql).
        style: Column name style (default: input).
        drop_table: Whether to include a DROP TABLE statement.

    Returns:
        A string containing the SQL DDL script.

    Raises:
        ValueError: If the specified dialect is not supported.
    """
    params: DDLParams = {
        "table_name": table_name,
        "schema": schema,
        "column_types": column_types,
        "drop_table": drop_table,
        "style": style,
    }
    dialect = dialect.lower()
    match dialect:
        case "tsql":
            return dialects.tsql.ddl(**params)
        case "mysql":
            return dialects.mysql.ddl(**params)
        case "postgresql":
            return dialects.postgresql.ddl(**params)
        case _:
            msg = f"Unsupported SQL dialect: {dialect}"
            raise ValueError(msg)
