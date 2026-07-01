"""ScenarioOutline model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.comment import Comment
from behave_model.model.examples import Examples
from behave_model.model.location import Location
from behave_model.model.step import Step
from behave_model.model.tag import Tag

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class ScenarioOutline:
    """A scenario outline with examples.

    Attributes:
        name: Outline name.
        description: Optional description text.
        tags: Tags applied to the outline.
        steps: Template steps.
        examples: List of Examples blocks.
        comments: Comments associated with the outline.
        location: Source location.
    """

    name: str = ""
    description: str = ""
    tags: list[Tag] = field(default_factory=list)
    steps: list[Step] = field(default_factory=list)
    examples: list[Examples] = field(default_factory=list)
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
        """Check whether the outline has a given tag."""
        return any(t.name == name for t in self.tags)

    def expand(self) -> list[dict[str, str]]:
        """Return all example rows as dicts (one per concrete scenario)."""
        result: list[dict[str, str]] = []
        for ex in self.examples:
            for row in ex.table.iter_dicts():
                result.append(row)
        return result

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_scenario_outline(self)
        for step in self.steps:
            step.accept(visitor)
        for ex in self.examples:
            ex.accept(visitor)
