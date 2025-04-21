"""Module for styling column names in DataFrames."""

import re
from collections.abc import Callable
from typing import Literal

# Compiled regex patterns
PASCAL_PATTERN = re.compile(r"(.)([A-Z][a-z]+)")
CAMEL_PATTERN = re.compile(r"([a-z0-9])([A-Z])")
NON_ALPHANUMERIC = re.compile(r"[^a-zA-Z0-9]")
UNDERSCORES = re.compile(r"_{2,}")


Style = Literal["camel", "pascal", "snake"]


class Styles:
    @classmethod
    def get(cls, style: Style) -> Callable:
        match style:
            case "camel":
                return cls.camel_case
            case "pascal":
                return cls.pascal_case
            case "snake":
                return cls.snake_case
            case _:
                err_msg = f"Style `{style}` not implemented."
                raise ValueError(err_msg)

    @classmethod
    def camel_case(cls, name: str) -> str:
        """Convert a string to camelCase."""
        # First convert to PascalCase
        pascal = cls.pascal_case(name)
        # Then make first character lowercase
        if pascal:
            return pascal[0].lower() + pascal[1:]
        return pascal

    @classmethod
    def pascal_case(cls, name: str) -> str:
        """Convert a string to PascalCase."""
        # Split by non-alphanumeric characters
        words = NON_ALPHANUMERIC.split(name)
        # Capitalize first letter of each word and join
        return "".join(word.capitalize() for word in words if word)

    @classmethod
    def snake_case(cls, name: str) -> str:
        """Convert a string to snake_case."""
        # Replace any non-alphanumeric characters with underscore
        s1 = PASCAL_PATTERN.sub(r"\1_\2", name)
        s2 = CAMEL_PATTERN.sub(r"\1_\2", s1)
        # Convert to lowercase and replace non-alphanumeric with underscore
        s3 = NON_ALPHANUMERIC.sub("_", s2).lower()
        return UNDERSCORES.sub("_", s3)
