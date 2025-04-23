"""
This module defines the ForExpr class, which represents a for-expression in the AST.
"""

from dataclasses import dataclass

from lunae.language.ast.base.expr import Expr
from lunae.utils.indent import indent


@dataclass
class ForExpr(Expr):
    """
    Represents a for-expression.

    Attributes:
        var (str): The loop variable.
        iterable (Expr): The iterable expression.
        body (Expr): The body of the loop.
    """

    var: str
    iterable: Expr
    body: Expr

    def __str__(self) -> str:
        """
        Returns a string representation of the for-expression.

        Returns:
            str: The string representation of the for-expression.
        """
        return f"FOR {self.var!r}\n{indent(self.iterable)}\n{indent(self.body)}"
