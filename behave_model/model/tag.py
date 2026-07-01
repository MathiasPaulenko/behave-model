"""Tag model."""

from __future__ import annotations

from dataclasses import dataclass

from behave_model.model.location import Location


@dataclass
class Tag:
    """A tag attached to a feature or scenario.

    Attributes:
        name: The tag name including the leading ``@``.
        location: Source location of the tag.
    """

    name: str
    location: Location = Location()

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tag):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
