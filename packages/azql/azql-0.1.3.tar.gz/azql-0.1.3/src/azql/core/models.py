from collections.abc import Callable
from typing import TypedDict

from ..config import DDL_DIR


class DefaultArgs:
    schema = "dbo"
    dialect = "tsql"
    style = "input"
    drop_table = False
    sample_size = 1000
    output_dir = DDL_DIR
    export = False
    skip_validation = False


class DDLParams(TypedDict):
    table_name: str
    schema: str
    column_types: dict[str, str]
    style: str
    drop_table: bool


# Type for DDL generation functions
DDLFunction = Callable[[DDLParams], str]
