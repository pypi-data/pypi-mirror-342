"""
This module defines the syntax rules for the language.
It includes keywords, binary operators, and unary operators.
"""

from dataclasses import dataclass


@dataclass
class Operator:
    """
    Represents an operator in the language.

    Attributes:
        operator (str): The operator symbol.
        priority (int): The precedence of the operator.
        function (str): The function name associated with the operator.
    """

    operator: str
    priority: int
    function: str

    @staticmethod
    def dict(operators: list[tuple[str, int, str]]):
        return {op[0]: Operator(*op) for op in operators}


KEYWORDS = {"if", "else", "for", "in", "while", "func"}
"""
set[str]: The reserved keywords in the language.
"""

BINARY_OPERATORS = Operator.dict(
    [
        ("+", 1, "add"),
        ("-", 1, "sub"),
        ("*", 2, "mul"),
        ("/", 2, "div"),
        ("%", 2, "mod"),
        ("==", 0, "is"),
        (">", 0, "more"),
        ("<", 0, "less"),
    ]
)
"""
dict[str, Operator]: The binary operators supported by the language.
"""

UNARY_OPERATORS = Operator.dict(
    [
        ("-", 0, "neg"),
        ("!", 0, "not"),
    ]
)
"""
dict[str, Operator]: The unary operators supported by the language.
"""
