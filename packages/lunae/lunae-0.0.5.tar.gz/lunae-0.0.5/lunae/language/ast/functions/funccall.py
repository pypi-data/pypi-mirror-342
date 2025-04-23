"""
This module defines the FuncCall class, which represents a function call in the AST.
"""

from dataclasses import dataclass

from lunae.language.ast.base.expr import Expr
from lunae.utils.indent import indent


@dataclass
class FuncCall(Expr):
    """
    Represents a function call.

    Attributes:
        func (str): The function name.
        args (list[Expr]): The arguments to the function.
    """

    func: str
    args: list[Expr]

    def __str__(self) -> str:
        """
        Returns a string representation of the function call.

        Returns:
            str: The string representation of the function call.
        """
        return f"CALL {self.func!r}\n{'\n'.join(indent(a) for a in self.args)}"
