"""
This module provides functionality for parsing function calls.
"""

from lunae.language.ast.base.expr import Expr
from lunae.language.ast.functions.funccall import FuncCall
from lunae.parser.parsers.base.expr import parse_expr
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_func_call(reader: ParserReader, name: str) -> FuncCall:
    """
    Parses a function call.

    Args:
        reader (ParserReader): The parser reader instance.
        name (str): The name of the function being called.

    Returns:
        FuncCall: The parsed function call.
    """
    reader.expect(TokenKind.LPAREN)

    args: list[Expr] = []

    if not reader.match(TokenKind.RPAREN):
        while True:
            args.append(parse_expr(reader))
            if reader.match(TokenKind.RPAREN):
                break
            reader.expect(TokenKind.COMMA)

    return FuncCall(name, args)
