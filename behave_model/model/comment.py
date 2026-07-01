"""Comment model preserving source-file comments."""

from __future__ import annotations

from dataclasses import dataclass

from behave_model.model.location import Location


@dataclass
class Comment:
    """A comment extracted from a feature file.

    Attributes:
        text: The raw comment text including the ``#`` prefix.
        location: Source location of the comment.
    """

    text: str
    location: Location = Location()

    def __str__(self) -> str:
        return self.text
