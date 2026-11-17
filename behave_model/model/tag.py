"""Tag model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.location import Location

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


def normalize_tag_name(name: str) -> str:
    """Return the canonical form of a tag name (with leading ``@``).

    ``"smoke"`` becomes ``"@smoke"``; names already starting with ``@``
    and empty names are returned unchanged.
    """
    if name and not name.startswith("@"):
        return "@" + name
    return name


@dataclass
class Tag:
    """A tag attached to a feature or scenario.

    Attributes:
        name: The tag name including the leading ``@``. Bare names are
            normalized to include it at construction time.
        location: Source location of the tag.
    """

    name: str
    location: Location = field(default_factory=Location)

    def __post_init__(self) -> None:
        self.name = normalize_tag_name(self.name)

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
