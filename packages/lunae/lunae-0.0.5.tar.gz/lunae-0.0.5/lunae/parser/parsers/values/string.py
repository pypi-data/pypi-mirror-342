"""
This module provides functionality for parsing string literals.
"""

from lunae.language.ast.values.string import String
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_string(reader: ParserReader) -> String:
    """
    Parses a string literal.

    Args:
        reader (ParserReader): The parser reader instance.

    Returns:
        String: The parsed string literal.
    """
    token = reader.expect(TokenKind.STRING)
    return String(token.string_value)
