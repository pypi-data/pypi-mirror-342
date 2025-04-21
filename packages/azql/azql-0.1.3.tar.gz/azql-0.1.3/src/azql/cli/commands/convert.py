from ..formatter import CustomHelpFormatter

CONFIG = {
    "name": "convert",
    "help": "Convert data exports to SQL DDL scripts",
    "formatter_class": CustomHelpFormatter,
}

ARGUMENTS = [
    (
        "input_file",
        {"help": "Path to input data file / folder (csv, json)"},
    ),
    (
        "output_dir",
        {"help": "Path to output SQL file", "nargs": "?", "default": None},
    ),
    (
        "-d",
        "--dialect",
        {
            "help": "SQL dialect (default: tsql, [mysql, postgresql])",
            "default": "tsql",
        },
    ),
    (
        "-s",
        "--schema",
        {"help": "SQL schema name, default `dbo`", "default": "dbo"},
    ),
    (
        "-t",
        "--table-name",
        {"help": "Name of the SQL table to create", "default": None},
    ),
    (
        "-n",
        "--sample-size",
        {
            "help": "Number of rows to sample for type detection",
            "type": int,
            "default": 1000,
        },
    ),
    (
        "--skip-validation",
        {
            "help": "Skip data validation step.",
            "action": "store_true",
            "default": False,
        },
    ),
    (
        "--style",
        {
            "help": "Column style (default: input, [camel, pascal, snake])",
            "default": "input",
        },
    ),
    (
        "--drop-table",
        {
            "help": "Include DROP TABLE statement, force drop",
            "action": "store_true",
            "default": False,
        },
    ),
]
