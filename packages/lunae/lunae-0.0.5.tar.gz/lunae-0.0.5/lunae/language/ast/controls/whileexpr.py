"""
This module defines the WhileExpr class, which represents a while-expression in the AST.
"""

from dataclasses import dataclass

from lunae.language.ast.base.expr import Expr
from lunae.utils.indent import indent


@dataclass
class WhileExpr(Expr):
    """
    Represents a while-expression.

    Attributes:
        cond (Expr): The condition expression.
        body (Expr): The body of the loop.
    """

    cond: Expr
    body: Expr

    def __str__(self):
        return f"WHILE\n{indent(self.cond)}\n{indent(self.body)}"
