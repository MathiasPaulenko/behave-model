"""Background model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.location import Location
from behave_model.model.step import Step

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Background:
    """A Background block that runs before every scenario in a feature.

    Attributes:
        name: Optional background name.
        steps: Steps that execute before each scenario.
        location: Source location.
    """

    name: str = ""
    steps: list[Step] = field(default_factory=list)
    location: Location = field(default_factory=Location)

    def __iter__(self):
        return iter(self.steps)

    def __len__(self) -> int:
        return len(self.steps)

    def accept(self, visitor: "Visitor") -> None:
        """Accept a visitor."""
        visitor.visit_background(self)
        for step in self.steps:
            step.accept(visitor)
