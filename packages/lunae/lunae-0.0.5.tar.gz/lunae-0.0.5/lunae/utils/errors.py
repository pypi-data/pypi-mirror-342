from lunae.utils.indent import indent
from lunae.utils.sourceposition import SourcePosition

SOURCE_MARGIN = 5


class SourceError(Exception):
    """
    Represents an error with source code context.

    Attributes:
        start (SourcePosition | None): The starting position of the error.
        end (SourcePosition | None): The ending position of the error.
        note (str): Additional context or source code snippet.
    """

    def __init__(
        self,
        message: str,
        start: SourcePosition | None,
        end: SourcePosition | None = None,
    ):
        """
        Initializes a SourceError.

        Args:
            message (str): The error message.
            start (SourcePosition | None): The starting position of the error.
            end (SourcePosition | None, optional): The ending position of the error.
        """
        self.note = ""
        self.start = start
        self.end = (
            end
            if end is not None
            else (
                None
                if start is None
                else (
                    SourcePosition(
                        start.line_number,
                        start.character_pos + 1,
                    )
                )
            )
        )
        if start:
            line = (
                f"at line {start.line_number+1}"
                if end is None or start.line_number == end.line_number
                else f"from line {start.line_number+1} to {end.line_number+1}"
            )
            character = (
                f"at character {start.character_pos+1}"
                if end is None or start.character_pos == end.character_pos
                else f"from character {start.character_pos+1} to {end.character_pos+1}"
            )
            full_msg = f"{message} {line}, {character}"
        else:
            full_msg = message
        super().__init__(full_msg)

    def with_source(self, source: str):
        """
        Adds source code context to the error message.

        Args:
            source (str): The source code as a string.
        """
        if self.start and self.end:
            source_lines = source.split("\n")
            lines: list[str] = []
            lines.extend(
                f"  {l}"
                for l in source_lines[
                    self.start.line_number - SOURCE_MARGIN : self.start.line_number
                ]
                if l.strip() != ""
            )
            lines.extend(
                f"! {l}"
                for l in source_lines[self.start.line_number : self.end.line_number + 1]
            )

            begin = min(self.start.character_pos, self.end.character_pos)
            length = max(self.start.character_pos, self.end.character_pos) - begin
            lines.append("  " + " " * begin + "^" * length)

            self.note = "\n".join(lines)

            self.add_note(indent(self.note))


class ParserError(SourceError):
    """
    Represents a parsing error.
    """


class TokenizerError(SourceError):
    """
    Represents a tokenization error.
    """


class InterpreterError(SourceError):
    """
    Represents an interpreter error.
    """
