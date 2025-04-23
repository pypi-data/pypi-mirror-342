"""
Handles reading and interpreting tokens for parsing.
"""

from typing import Optional

from lunae.tokenizer.grammar import TokenKind
from lunae.tokenizer.token import Token
from lunae.utils.errors import ParserError


class ParserReader:
    """
    A utility class for reading and processing tokens during parsing.

    Attributes:
        tokens (list[Token]): The list of tokens to process.
        pos (int): The current position in the token list.
    """

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def skip(self):
        """
        Advances the reader to the next token.
        """
        self.pos += 1

    def peek(self, offset: int = 0) -> Optional[Token]:
        """
        Peeks at a token at a given offset from the current position.

        Args:
            offset (int): The offset from the current position.

        Returns:
            Optional[Token]: The token at the given offset, or None if out of bounds.
        """
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def is_followed(self, kind: TokenKind, match: str | None = None, offset: int = 0):
        """
        Checks if a token of a specific kind and value follows at a given offset.

        Args:
            kind (TokenKind): The kind of token to check.
            match (str | None): The value of the token to check, if any.
            offset (int): The offset from the current position.

        Returns:
            bool: True if the token matches, False otherwise.
        """
        peek = self.peek(offset)
        return peek and peek.kind == kind and (match is None or peek.match == match)

    def match(self, kind: TokenKind, value: str | None = None) -> Optional[Token]:
        """
        Matches the current token against a specific kind and value.

        Args:
            kind (TokenKind): The kind of token to match.
            value (str | None): The value of the token to match, if any.

        Returns:
            Optional[Token]: The matched token, or None if no match.
        """
        tok = self.peek()
        if tok and tok.kind == kind and (value is None or tok.match == value):
            self.skip()
            return tok
        return None

    def expect(self, kind: TokenKind, match: str | None = None) -> Token:
        """
        Expects a token of a specific kind and value, raising an error if not found.

        Args:
            kind (TokenKind): The kind of token to expect.
            match (str | None): The value of the token to expect, if any.

        Returns:
            Token: The matched token.

        Raises:
            ParserError: If the expected token is not found.
        """
        tok = self.match(kind, match)
        if not tok:
            expected = match or kind
            actual = self.peek()
            raise ParserError(
                f"Expected '{expected}', got '{actual.kind if actual else None}'",
                actual.start if actual else None,
                actual.end if actual else None,
            )
        return tok
