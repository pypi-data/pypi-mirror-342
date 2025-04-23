"""
Defines the grammar and token types for the tokenizer.

Attributes:
    TOKEN_TYPES (list[tuple[str, str]]): A list of token types and their regex patterns.
    COMPILED_TOKEN_REGEX (re.Pattern): A compiled regex pattern for all token types.
    COMILED_INDENT_REGEX (re.Pattern): A compiled regex pattern for indentation.
"""

import re
from enum import Enum

from lunae.language.syntax import BINARY_OPERATORS, UNARY_OPERATORS

OPERATORS = set().union(UNARY_OPERATORS, BINARY_OPERATORS)
OPERATORS_REGEX = (re.escape(op) for op in OPERATORS)


class TokenKind(Enum):
    """
    Represents the different kinds of tokens used in the tokenizer.
    """

    NUMBER = r"\d+(\.\d+)?"
    STRING = r'"(\\.|[^"\\])*"'
    IDENT = r"[a-zA-Z_][a-zA-Z0-9_]*"
    OP = "(" + "|".join(OPERATORS_REGEX) + ")"
    ASSIGN = r"="
    LPAREN = r"\("
    RPAREN = r"\)"
    LBRACK = r"\["
    RBRACK = r"\]"
    COLON = r":"
    COMMA = r","
    COMMENT = r"#.*"
    NEWLINE = r"\n"
    WHITESPACE = r"[ \t]+"
    UNKNOWN = r"."
    KEYWORD = 1
    INDENT = 2
    DEDENT = 3

    def __repr__(self):
        return f"TokenKind.{self.name}"


COMPILED_TOKEN_REGEX = re.compile(
    "|".join(
        f"(?P<{token.name}>{token.value})"
        for token in TokenKind
        if isinstance(token.value, str)
    )
)
COMILED_INDENT_REGEX = re.compile(r"[ \t]*")
