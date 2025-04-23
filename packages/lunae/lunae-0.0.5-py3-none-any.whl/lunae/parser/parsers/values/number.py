"""
This module provides functionality for parsing numeric literals.
"""

from lunae.language.ast.values.number import Number
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_number(reader: ParserReader) -> Number:
    """
    Parses a numeric literal.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        Number: The parsed numeric literal.
    """
    token = reader.expect(TokenKind.NUMBER)
    return Number(token.number_value)
