"""Comment model for source-file comments.

Note: the Behave-based parser does not expose comments, so ``comments``
lists are currently always empty after parsing. The class is part of the
public model for hand-built models and future parser support.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.location import Location

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Comment:
    """A comment extracted from a feature file.

    Attributes:
        text: The raw comment text including the ``#`` prefix.
        location: Source location of the comment.
    """

    text: str
    location: Location = field(default_factory=Location)

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_comment(self)

    def __str__(self) -> str:
        return self.text
