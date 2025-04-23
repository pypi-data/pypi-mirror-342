from dataclasses import dataclass

from lunae.parser.parsers.base.expr import Expr


@dataclass
class Var(Expr):
    """
    Represents a variable.

    Attributes:
        name (str): The name of the variable.
    """

    name: str

    def __str__(self):
        return f"VAR {self.name!r}"
