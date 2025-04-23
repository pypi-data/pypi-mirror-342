"""
This module defines the Expr class.
"""

from dataclasses import dataclass


@dataclass
class Expr:
    """
    Base class for all expressions.
    """

    def __str__(self):
        return "EXPR"
