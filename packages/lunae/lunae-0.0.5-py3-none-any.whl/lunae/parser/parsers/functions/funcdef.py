"""
This module provides the parser for function definitions.
"""

from lunae.language.ast.functions.funcdef import FuncDef
from lunae.parser.parsers.base.block import parse_block
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_func_def(reader: ParserReader) -> FuncDef:
    """
    Parses a function definition.

    Args:
        reader (ParserReader): The parser reader.

    Returns:
        FuncDef: The parsed function definition node.
    """
    reader.expect(TokenKind.KEYWORD, "func")
    name = reader.expect(TokenKind.IDENT).match
    reader.expect(TokenKind.LPAREN)
    params: list[str] = []
    if not reader.match(TokenKind.RPAREN):
        while True:
            params.append(reader.expect(TokenKind.IDENT).match)
            if reader.match(TokenKind.RPAREN):
                break
            reader.expect(TokenKind.COMMA)

    reader.expect(TokenKind.COLON)
    return FuncDef(name, params, parse_block(reader))
