from dataclasses import dataclass

from lunae.language.ast.base.expr import Expr


@dataclass
class String(Expr):
    """
    Represents a string literal.

    Attributes:
        value (str): The string value.
    """

    value: str

    def __str__(self):
        return f"STRING {self.value!r}"
