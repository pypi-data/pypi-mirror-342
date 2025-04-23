"""
This module defines the FuncDef class, which represents a function definition in the AST.
"""

from dataclasses import dataclass

from lunae.language.ast.base.expr import Expr
from lunae.utils.indent import indent


@dataclass
class FuncDef(Expr):
    """
    Represents a function definition.

    Attributes:
        name (str): The function name.
        params (list[str]): The list of parameter names.
        body (Expr): The body of the function.
    """

    name: str
    params: list[str]
    body: Expr

    def __str__(self) -> str:
        """
        Returns a string representation of the function definition.

        Returns:
            str: The string representation of the function definition.
        """
        return f"FUNC {self.name!r} {self.params!r}:\n{indent(self.body)}"
