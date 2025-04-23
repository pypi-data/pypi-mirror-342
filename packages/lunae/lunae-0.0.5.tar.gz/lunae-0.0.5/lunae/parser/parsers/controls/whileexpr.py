"""
This module provides functionality for parsing while expressions.
"""

from lunae.language.ast.controls.whileexpr import WhileExpr
from lunae.parser.parsers.base.block import parse_block
from lunae.parser.parsers.base.expr import parse_expr
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_while_expr(reader: ParserReader) -> WhileExpr:
    """
    Parses a while expression.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        WhileExpr: The parsed while expression.
    """
    reader.expect(TokenKind.KEYWORD, "while")
    cond = parse_expr(reader)
    reader.expect(TokenKind.COLON)
    body = parse_block(reader)
    return WhileExpr(cond, body)
