from math import ceil

from .config import COMMON_DELIMITERS, ENCODING
from .core.models import DefaultArgs


def dict_to_args(args_dict: dict | DefaultArgs = None) -> object:
    """
    Convert a dictionary to an object with properties matching DefaultArgs.

    Args:
        args_dict: Dictionary containing argument values

    Returns:
        An object with properties from the input dictionary
    """

    if args_dict is None:
        return DefaultArgs()

    if isinstance(args_dict, DefaultArgs):
        return args_dict

    args = DefaultArgs()
    # Override with provided values from the dictionary
    if args_dict:
        for key, value in args_dict.items():
            setattr(args, key, value)

    return args


def round_up_to_nearest_multiple(n: int, multiple: int = 5) -> int:
    """
    Round up a number to the nearest multiple.

    Args:
        n: The number to round up
        multiple: The multiple to round up to (default: 5)

    Returns:
        The rounded up number
    """
    return multiple * ceil(n / multiple)


def guess_csv_delimiter(file_path: str, num_lines: int = 10) -> str:
    """
    Guess the delimiter used in a CSV file by counting occurrences of common delimiters.

    Args:
        file_path: Path to the CSV file
        num_lines: Number of lines to check for delimiter detection

    Returns:
        The most likely delimiter character
    """
    delimiter_counts = dict.fromkeys(COMMON_DELIMITERS, 0)
    try:
        with open(file_path, encoding=ENCODING) as file:
            # read file content
            for _ in range(num_lines):
                try:
                    line = next(file)
                    for delimiter in COMMON_DELIMITERS:
                        delimiter_counts[delimiter] += line.count(delimiter)
                except StopIteration:
                    break
            # Find the delimiter with the highest count
            if any(delimiter_counts.values()):
                return max(delimiter_counts.items(), key=lambda x: x[1])[0]
            # Default to comma if no delimiter has a significant count
            return ","
    except Exception as e:
        raise e
