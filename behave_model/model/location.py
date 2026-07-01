"""Location model representing a position in a source file."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    """Represents a position in a feature file.

    Attributes:
        filename: Path to the source file.
        line: 1-based line number.
        column: 1-based column number (0 if unknown).
    """

    filename: str = ""
    line: int = 0
    column: int = 0

    def __str__(self) -> str:
        parts: list[str] = []
        if self.filename:
            parts.append(self.filename)
        if self.line:
            parts.append(f"line {self.line}")
        if self.column:
            parts.append(f"column {self.column}")
        return ", ".join(parts) if parts else "<unknown>"
