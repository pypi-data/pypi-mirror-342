"""
This module defines the IfExpr class, which represents an if-expression in the AST.
"""

from dataclasses import dataclass
from typing import Optional

from lunae.language.ast.base.expr import Expr
from lunae.utils.indent import indent


@dataclass
class IfExpr(Expr):
    """
    Represents an if-expression.

    Attributes:
        cond (Expr): The condition expression.
        then_branch (Expr): The expression for the 'then' branch.
        else_branch (Optional[Expr]): The expression for the 'else' branch, if any.
    """

    cond: Expr
    then_branch: Expr
    else_branch: Optional[Expr]

    def __str__(self) -> str:
        """
        Returns a string representation of the if-expression.

        Returns:
            str: The string representation of the if-expression.
        """
        return f"IF\n{indent(self.cond)}\n{indent(self.then_branch)}\n{indent(self.else_branch)}"
