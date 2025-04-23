"""
The `lunae.parser` package provides tools for parsing token into an abstract syntax tree (AST).
"""

from lunae.language.ast.base.block import Block
from lunae.parser.parsers.base.block import parse_reader
from lunae.parser.reader import ParserReader
from lunae.tokenizer import Token


def parse(tokens: list[Token]) -> Block:
    """
    Parses a list of tokens into an abstract syntax tree (AST).

    Args:
        tokens (list[Token]): The list of tokens to parse.

    Returns:
        Block: The root block of the parsed AST.
    """
    reader = ParserReader(tokens)
    ast = parse_reader(reader)
    return ast


__all__ = ("parse",)
