from argparse import ArgumentParser

from .commands import convert
from .formatter import CustomHelpFormatter

cli_parser = ArgumentParser(formatter_class=CustomHelpFormatter)
subparsers = cli_parser.add_subparsers(dest="command", help="Commands")

# ------------------- azql convert ... ------------------- #
convert_command = subparsers.add_parser(**convert.CONFIG)
for arguments in convert.ARGUMENTS:
    *args, kwargs = arguments
    convert_command.add_argument(*args, **kwargs)

# ------------------- azql validate ... ------------------ #
# Todo: Implement a data validation command
validate_command = subparsers.add_parser(
    name="validate",
    help="Validate Data",
)
