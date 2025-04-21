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
    Generate TSQL DDL script for Microsoft SQL Server.

    Args:
        table_name: Name of the table to create
        schema: Schema name
        column_types: Dictionary with SQL type information for each column
        drop_table: Whether to include a DROP TABLE statement

    Returns:
        TSQL DDL script as a string
    """
    # Format the CREATE TABLE statement
    ddl_lines = [
        "-- Auto-generated TSQL DDL script",
        "",
    ]

    if drop_table:
        ddl_lines.extend(
            [
                f"IF OBJECT_ID(N'{schema}.{table_name}', N'U') IS NOT NULL",
                f"    DROP TABLE [{schema}].[{table_name}];",
                "",
            ],
        )
    else:
        # If not dropping, add IF NOT EXISTS check
        ddl_lines.extend(
            [
                f"IF OBJECT_ID(N'{schema}.{table_name}', N'U') IS NULL",
                "BEGIN",
                "",
            ],
        )

    ddl_lines.append(f"CREATE TABLE [{schema}].[{table_name}] (")

    styler = None
    if style and style in ["camel", "pascal", "snake"]:
        styler = Styles.get(style)

    # Add column definitions with comma-first style
    # first line has no comma, changing whitespace afterwards
    whitespace = "    "
    for column, info in column_types.items():
        col_name = styler(column) if styler else column
        nullable_str = "NULL" if info["nullable"] else "NOT NULL"
        col_definition = f"[{col_name}] {info['sql_type']} {nullable_str}"
        ddl_lines.append(f"{whitespace}{col_definition}")
        whitespace = "  , "

    # Close CREATE TABLE statement
    ddl_lines.append(");")

    # Close the IF block if not dropping
    if not drop_table:
        ddl_lines.append("END;")

    # Convert SQL keywords to UPPERCASE
    final_ddl = "\n".join(ddl_lines)
    sql_keywords = [
        "CREATE TABLE",
        "DROP TABLE",
        "IF",
        "OBJECT_ID",
        "IS",
        "NOT",
        "NULL",
        "BEGIN",
        "END",
    ]
    for keyword in sql_keywords:
        final_ddl = final_ddl.replace(keyword, keyword.upper())

    return final_ddl


def convert_types(
    column_properties: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Convert Python types to TSQL (Microsoft SQL Server) types.

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
            # Choose appropriate integer type based on potential range
            sql_type_info["sql_type"] = "INT"

        elif python_type == "float":
            # For floats, use DECIMAL with appropriate precision and scale
            precision = properties["precision"]
            scale = properties["scale"]

            # Ensure minimum values and handle edge cases
            precision = max(precision, scale + 1, 1)
            scale = max(scale, 0)

            # SQL Server limits
            precision = min(precision, 38)

            sql_type_info["sql_type"] = f"DECIMAL({precision}, {scale})"

        elif python_type == "bool":
            sql_type_info["sql_type"] = "BIT"

        elif python_type == "date":
            sql_type_info["sql_type"] = "DATETIME2"

        else:  # Default to string (NVARCHAR)
            max_length = properties["max_length"]

            # Round up to the nearest multiple of 5
            if max_length > 0:
                max_length = round_up_to_nearest_multiple(max_length, 5)

            # Handle very long strings
            if max_length > 4000:
                sql_type_info["sql_type"] = "NVARCHAR(MAX)"
            else:
                # Ensure a minimum size of 5
                max_length = max(max_length, 5)
                sql_type_info["sql_type"] = f"NVARCHAR({max_length})"

        sql_column_types[column] = sql_type_info

    return sql_column_types
