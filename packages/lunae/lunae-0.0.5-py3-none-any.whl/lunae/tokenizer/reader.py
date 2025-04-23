"""
Handles reading and processing source data for tokenization.
"""

from lunae.tokenizer.grammar import (
    COMILED_INDENT_REGEX,
    COMPILED_TOKEN_REGEX,
    TokenKind,
)
from lunae.tokenizer.token import Token
from lunae.utils.errors import TokenizerError
from lunae.utils.sourceposition import SourcePosition


class TokenizerReader:
    """
    A class responsible for reading and processing tokens.
    """

    def __init__(self, source: str):
        """
        Initializes the TokenizerReader with the given source.

        Args:
            source (str): The source code to tokenize.
        """
        self.source = source
        self.read_pos = 0
        self.line_number = 0
        self.line_start_pos = 0

    @property
    def line_end_pos(self) -> int:
        """
        Gets the position of the end of the current line.

        Returns:
            int: The position of the end of the current line.
        """
        pos = self.source.find("\n", self.line_start_pos)
        return len(self.source) if pos == -1 else pos

    @property
    def character_pos(self) -> int:
        """
        Gets the current character position in the line.

        Returns:
            int: The current character position.
        """
        return self.read_pos - self.line_start_pos

    @property
    def is_new_line(self) -> bool:
        """
        Checks if the current position is the start of a new line.

        Returns:
            bool: True if at the start of a new line, False otherwise.
        """
        return self.read_pos == self.line_start_pos

    @property
    def is_end_of_file(self) -> bool:
        """
        Checks if the current position is at the end of the file.

        Returns:
            bool: True if at the end of the file, False otherwise.
        """
        return self.read_pos >= len(self.source)

    @property
    def is_end_of_line(self) -> bool:
        """
        Checks if the current position is at the end of the line.

        Returns:
            bool: True if at the end of the line, False otherwise.
        """
        return self.is_end_of_file or self.source[self.read_pos] == "\n"

    @property
    def start(self) -> SourcePosition:
        """
        Gets the start position of the current token.

        Returns:
            SourcePosition: The start position.
        """
        return SourcePosition(self.line_number, self.character_pos)

    @property
    def end(self) -> SourcePosition:
        """
        Gets the end position of the current token.

        Returns:
            SourcePosition: The end position.
        """
        return SourcePosition(self.line_number, self.character_pos)

    def read_token(self) -> Token:
        """
        Reads the next token from the source.

        Returns:
            Token: The next token.
        """
        match = COMPILED_TOKEN_REGEX.match(self.source, self.read_pos)

        assert match and match.lastgroup

        kind = TokenKind[match.lastgroup]

        if kind == TokenKind.UNKNOWN:
            raise TokenizerError(
                f"Unexpected character: {self.source[self.read_pos]!r}",
                SourcePosition(self.line_number, self.character_pos),
            )

        start = self.start

        self.read_pos = match.end()

        if kind == TokenKind.NEWLINE:
            self.line_number += 1
            self.line_start_pos = match.end()

        return Token(
            kind,
            match.group(0),
            start,
            self.end,
        )

    def read_indentation(self) -> Token:
        """
        Reads the indentation token from the source.

        Returns:
            Token: The indentation token.
        """
        match = COMILED_INDENT_REGEX.match(self.source, self.read_pos)
        assert match, "Should always match (accept empty strings)"

        start = self.start

        self.read_pos = match.end()

        return Token(
            TokenKind.WHITESPACE,
            match.group(0),
            start,
            self.end,
        )
