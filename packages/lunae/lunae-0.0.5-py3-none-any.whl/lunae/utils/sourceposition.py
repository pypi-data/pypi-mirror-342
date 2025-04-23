"""
This module defines the SourcePosition class, which represents a position in the source code.
"""

from dataclasses import dataclass


@dataclass
class SourcePosition:
    """
    Represents a position in the source code.

    Attributes:
        line_number (int): The line number in the source code (0-based).
        character_pos (int): The character position in the line (0-based).
    """

    line_number: int
    character_pos: int
