"""
This module defines the Block class.
"""

from dataclasses import dataclass

from lunae.language.ast.base.expr import Expr
from lunae.utils.indent import indent


@dataclass
class Block(Expr):
    """
    Represents a block of statements.

    Attributes:
        statements (list[Expr]): The list of statements in the block.
    """

    statements: list[Expr]

    def __str__(self):
        return f"BLOCK\n{'\n'.join(indent(s) for s in self.statements)}"
