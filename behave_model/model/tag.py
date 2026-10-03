"""Tag model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.location import Location

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Tag:
    """A tag attached to a feature or scenario.

    Attributes:
        name: The tag name including the leading ``@``.
        location: Source location of the tag.
    """

    name: str
    location: Location = field(default_factory=Location)

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_tag(self)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
