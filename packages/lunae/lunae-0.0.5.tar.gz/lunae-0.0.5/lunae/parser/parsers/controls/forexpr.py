"""
This module provides functionality for parsing for expressions.
"""

from lunae.language.ast.controls.forexpr import ForExpr
from lunae.parser.parsers.base.block import parse_block
from lunae.parser.parsers.base.expr import parse_expr
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_for_expr(reader: ParserReader) -> ForExpr:
    """
    Parses a for expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        ForExpr: The parsed for expression.
    """
    reader.expect(TokenKind.KEYWORD, "for")
    var = reader.expect(TokenKind.IDENT).match
    reader.expect(TokenKind.KEYWORD, "in")
    iterable = parse_expr(reader)
    reader.expect(TokenKind.COLON)
    body = parse_block(reader)
    return ForExpr(var, iterable, body)
