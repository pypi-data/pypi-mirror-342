"""
The `lunae.tokenizer` package provides tools for tokenizing input data, including grammar definitions, token readers, and token representations.
"""

from lunae.language.syntax import KEYWORDS
from lunae.tokenizer.grammar import TokenKind
from lunae.tokenizer.reader import TokenizerReader
from lunae.tokenizer.token import Token


def tokenize(source: str) -> list[Token]:
    """
    Tokenizes the given source code into a list of tokens.

    Args:
        source (str): The source code as a string.

    Returns:
        list[Token]: A list of tokens extracted from the source code.
    """
    reader = TokenizerReader(source)
    tokens: list[Token] = []
    indent_stack = [0]

    while not reader.is_end_of_file:
        if reader.is_new_line:
            token = reader.read_indentation()
            indent_level = len(token.match.replace("\t", "    "))

            if not reader.is_end_of_line:  # Non-empty line
                if indent_level > indent_stack[-1]:
                    indent_stack.append(indent_level)
                    tokens.append(
                        Token(
                            TokenKind.INDENT,
                            token.match,
                            token.start,
                            token.end,
                        )
                    )
                while indent_level < indent_stack[-1]:
                    indent_stack.pop()
                    tokens.append(
                        Token(
                            TokenKind.DEDENT,
                            token.match,
                            token.start,
                            token.end,
                        )
                    )
            if reader.is_end_of_file:
                break

        token = reader.read_token()
        if token.kind == TokenKind.IDENT and token.match in KEYWORDS:
            token.kind = TokenKind.KEYWORD
        if token.kind not in (TokenKind.WHITESPACE, TokenKind.COMMENT):
            tokens.append(token)

    while indent_stack:
        if indent_stack.pop() != 0:
            tokens.append(Token(TokenKind.DEDENT, "", reader.start, reader.end))

    return tokens


__all__ = ("tokenize",)
