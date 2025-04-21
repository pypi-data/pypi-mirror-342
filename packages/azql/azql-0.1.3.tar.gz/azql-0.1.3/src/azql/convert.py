"""
Module for converting data files to SQL DDL (Data Definition Language) scripts.

This module provides functionality to analyze data files (CSV, JSON),
detect data types, and generate appropriate SQL DDL scripts for table creation.
It supports various SQL dialects, validation of data integrity, and customization
of the generated SQL scripts.

The main entry point is the `convert` function, which processes individual files
or directories containing multiple data files.

Example:
    ```python
    from pathlib import Path
    import azql

    # Convert a single CSV file to a SQL DDL script
    ddl = azql.convert("data.csv", dialect="tsql", schema="dbo")

    # Process all supported files in a directory
    results = azql.convert(Path("data_directory"), export=True)
    ```
"""

from pathlib import Path

from .config import DDL_DIR, ENCODING, EXTENSIONS
from .core import (
    analyze_column_properties,
    convert_to_sql_types,
    detect_types,
    generate_ddl_script,
    validate_data_integrity,
)
from .io import read_file
from .utils import dict_to_args


def convert(
    file_path: Path | str,
    **kwargs,
) -> str | tuple[str] | None:
    """
    Convert data files to SQL DDL scripts.

    This function reads data from a file or directory, analyzes its structure,
    and generates appropriate SQL DDL scripts for table creation.

    Args:
        file_path: Path to a data file or directory containing data files.
                   Supported file extensions are defined in EXTENSIONS.
        validate: Whether to validate data integrity before conversion.
                  Default is True.
        **kwargs: Additional arguments for customization:
            - sample_size: Number of rows to sample for type detection.
            - dialect: SQL dialect to use for type conversion.
            - schema: Database schema name for the table.
            - drop_table: Whether to include DROP TABLE statement in DDL.
            - style: SQL formatting style.
            - export: Whether to write DDL to file.
            - output_dir: Custom output directory for DDL files.

    Returns:
        str: Generated DDL script if export=False.
        dict: Dictionary of DDL scripts if processing a directory.
        None: If export=True or if validation fails.

    Raises:
        None: But prints error messages if validation fails or no data found.
    """
    # check if dir, then run recursivly
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    if file_path.is_dir():
        return {
            str(fp): convert(fp, **kwargs)
            for fp in file_path.iterdir()
            if EXTENSIONS.search(fp.suffix)
        }

    # Read the data
    data = read_file(file_path)
    if not data:
        print("No data found in the input file.")
        return None

    args = dict_to_args(kwargs)

    # Detect and analyze column types
    sample_size = min(args.sample_size, len(data))
    column_types = detect_types(data, sample_size)

    # Validate data integrity
    if not args.skip_validation:
        validation_results = validate_data_integrity(data, column_types)
        if not validation_results["is_valid"]:
            print(f"\nData validation failed: {file_path.stem}")
            print(f"\n{data = }")
            print(f"\n{column_types = }")
            for issue in validation_results["issues"]:
                print(f"- {issue}")
            print("\n")
            return None

    # Convert to SQL types
    dialect = args.dialect
    column_properties = analyze_column_properties(data, column_types)
    sql_column_types = convert_to_sql_types(column_properties, dialect)

    schema = args.schema
    table_name = file_path.stem
    # Generate DDL script
    ddl_script = generate_ddl_script(
        table_name=table_name,
        schema=schema,
        column_types=sql_column_types,
        dialect=dialect,
        drop_table=args.drop_table,
        style=args.style,
    )

    # Write the script to the output file
    if args.export:
        ddl_dir = args.output_dir
        if ddl_dir is None:
            # Calculate the ddl directory at the same level as the input dir.
            ddl_dir = file_path.parent / DDL_DIR
        else:
            ddl_dir = Path(ddl_dir)

        # Create the ddl directory if it doesn't exist
        ddl_dir.mkdir(exist_ok=True)

        # Generate output filename with schema__tablename.sql format
        output_filename = f"{schema}__{table_name}.sql"
        output_dir = ddl_dir / output_filename

        output_dir.write_text(ddl_script, encoding=ENCODING)
        print(f"Script successfully written to {output_dir}")
        return None

    return ddl_script
