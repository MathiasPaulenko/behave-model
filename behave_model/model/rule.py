"""Rule model (Gherkin v6).

A Rule groups related scenarios within a Feature, optionally with its
own Background.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Union

from behave_model.model.background import Background
from behave_model.model.comment import Comment
from behave_model.model.location import Location
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.tag import Tag

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor

ScenarioLike = Union[Scenario, ScenarioOutline]


@dataclass
class Rule:
    """A Rule block within a Feature (Gherkin v6).

    Attributes:
        name: Rule name.
        description: Optional description text.
        tags: Tags applied to the rule.
        background: Optional Background specific to this rule.
        scenarios: Scenarios and ScenarioOutlines inside this rule.
        comments: Comments associated with the rule.
        location: Source location.
    """

    name: str = ""
    description: str = ""
    tags: list[Tag] = field(default_factory=list)
    background: Background | None = None
    scenarios: list[ScenarioLike] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    location: Location = field(default_factory=Location)

    def __iter__(self):
        return iter(self.scenarios)

    def __len__(self) -> int:
        return len(self.scenarios)

    @property
    def tag_names(self) -> list[str]:
        """Return tag names as strings."""
        return [t.name for t in self.tags]

    def has_tag(self, name: str) -> bool:
        """Check whether the rule has a given tag."""
        return any(t.name == name for t in self.tags)

    def all_scenarios(self) -> list[ScenarioLike]:
        """Return all scenario-like elements in this rule."""
        return list(self.scenarios)

    def all_steps(self) -> list:
        """Return every step in the rule (background + scenarios)."""
        from behave_model.model.step import Step

        steps: list[Step] = []
        if self.background:
            steps.extend(self.background.steps)
        for s in self.scenarios:
            steps.extend(s.steps)
        return steps

    def accept(self, visitor: "Visitor") -> None:
        """Accept a visitor."""
        visitor.visit_rule(self)
        if self.background:
            self.background.accept(visitor)
        for s in self.scenarios:
            s.accept(visitor)
