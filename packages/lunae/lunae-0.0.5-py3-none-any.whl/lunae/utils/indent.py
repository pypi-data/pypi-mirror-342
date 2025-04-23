"""
This module provides utility functions for string manipulation.
"""

DEEFAULT_PREFIX = "  "


def indent(obj, prefix=DEEFAULT_PREFIX) -> str:
    """
    Indent each line of the str(obj) for pretty printing.

    Args:
        obj (Any): The object to convert to a string and indent.
        prefix (str): The string to use for indentation.

    Returns:
        str: The indented string.
    """
    return "\n".join(f"{prefix}{l}" for l in str(obj).split("\n"))
