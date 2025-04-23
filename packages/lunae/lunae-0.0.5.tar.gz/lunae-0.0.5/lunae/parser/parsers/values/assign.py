"""
This module provides functionality for parsing assignment expressions.
"""

from lunae.language.ast.values.assign import Assign
from lunae.parser.parsers.base.expr import parse_expr
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_assign(reader: ParserReader) -> Assign:
    """
    Parses an assignment expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Assign: The parsed assignment expression.
    """
    name = reader.expect(TokenKind.IDENT).match
    reader.expect(TokenKind.ASSIGN)
    value = parse_expr(reader)
    return Assign(name, value)
