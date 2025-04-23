"""
Represents individual tokens and their properties.
"""

from dataclasses import dataclass

from lunae.tokenizer.grammar import TokenKind
from lunae.utils.errors import TokenizerError
from lunae.utils.sourceposition import SourcePosition


@dataclass
class Token:
    """
    Represents a token in the source code.

    Attributes:
        kind (str): The type of the token (e.g., "NUMBER", "STRING").
        match (str): The matched string for the token.
        start (SourcePosition): The starting position of the token.
        end (SourcePosition): The ending position of the token.
    """

    kind: TokenKind
    match: str
    start: SourcePosition
    end: SourcePosition

    @property
    def string_value(self) -> str:
        """
        Returns the string value of the token based on its kind.

        Returns:
            str: The value of the token.

        Raises:
            TokenizerError: If the token kind is unexpected.
        """
        if self.kind == TokenKind.STRING:
            return bytes(self.match[1:-1], "utf-8").decode("unicode_escape")

        raise TokenizerError(
            f"Unexpected token kind: {self.kind} has no value", self.start, self.end
        )

    @property
    def number_value(self) -> float:
        """
        Returns the float value of the token based on its kind.

        Returns:
            float: The value of the token.

        Raises:
            TokenizerError: If the token kind is unexpected.
        """
        if self.kind == TokenKind.NUMBER:
            return float(self.match)

        raise TokenizerError(
            f"Unexpected token kind: {self.kind} has no value", self.start, self.end
        )
