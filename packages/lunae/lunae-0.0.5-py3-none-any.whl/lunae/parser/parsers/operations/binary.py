"""
This module provides functionality for parsing binary operations.
"""

from lunae.language.ast.base.expr import Expr
from lunae.language.ast.functions.funccall import FuncCall
from lunae.language.syntax import BINARY_OPERATORS
from lunae.parser.parsers.operations.unary import parse_unary
from lunae.parser.reader import ParserReader
from lunae.tokenizer.grammar import TokenKind


def parse_binary(reader: ParserReader, min_prec: int = 0) -> FuncCall | Expr:
    """
    Parses a binary operation using precedence climbing.

    Args:
        reader (ParserReader): The parser reader instance.
        min_prec (int, optional): The minimum precedence for the operation. Defaults to 0.

    Returns:
        FuncCall: The parsed binary operation.
    """
    left = parse_unary(reader)
    while True:
        tok = reader.peek()
        if not tok or tok.kind != TokenKind.OP:
            break
        op = BINARY_OPERATORS[tok.match]
        if op.priority < min_prec:
            break
        reader.skip()
        right = parse_binary(reader, min_prec + 1)
        left = FuncCall(op.function, [left, right])
    return left
