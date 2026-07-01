"""Scenario model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.comment import Comment
from behave_model.model.location import Location
from behave_model.model.step import Step
from behave_model.model.tag import Tag

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Scenario:
    """A single scenario within a feature.

    Attributes:
        name: Scenario name.
        description: Optional description text.
        tags: Tags applied to the scenario.
        steps: Steps in the scenario.
        comments: Comments associated with the scenario.
        location: Source location.
    """

    name: str = ""
    description: str = ""
    tags: list[Tag] = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    location: Location = field(default_factory=Location)

    def __iter__(self):
        return iter(self.steps)

    def __len__(self) -> int:
        return len(self.steps)

    @property
    def tag_names(self) -> list[str]:
        """Return tag names as strings."""
        return [t.name for t in self.tags]

    def has_tag(self, name: str) -> bool:
        """Check whether the scenario has a given tag."""
        return any(t.name == name for t in self.tags)

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_scenario(self)
        for step in self.steps:
            step.accept(visitor)
