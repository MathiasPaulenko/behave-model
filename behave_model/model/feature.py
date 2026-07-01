"""Feature model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Union
from typing import TYPE_CHECKING

from behave_model.model.background import Background
from behave_model.model.comment import Comment
from behave_model.model.location import Location
from behave_model.model.rule import Rule
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.tag import Tag

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor

# Union type for any scenario-like element
ScenarioLike = Union[Scenario, ScenarioOutline]


@dataclass
class Feature:
    """A feature parsed from a ``.feature`` file.

    Attributes:
        name: Feature name.
        description: Optional description text (multi-line).
        tags: Tags applied at the feature level.
        background: Optional Background block (feature-level).
        scenarios: List of Scenario and ScenarioOutline objects directly
            under the feature (not inside a Rule).
        rules: List of Rule blocks (Gherkin v6).
        comments: Comments associated with the feature.
        location: Source location.
        language: Feature file language (default ``en``).
    """

    name: str = ""
    description: str = ""
    tags: list[Tag] = field(default_factory=list)
    background: Background | None = None
    scenarios: list[ScenarioLike] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    comments: list[Comment] = field(default_factory=list)
    location: Location = field(default_factory=Location)
    language: str = "en"

    def __iter__(self) -> Iterator[ScenarioLike]:
        return iter(self.scenarios)

    def __len__(self) -> int:
        return len(self.scenarios)

    @property
    def tag_names(self) -> list[str]:
        """Return tag names as strings."""
        return [t.name for t in self.tags]

    def has_tag(self, name: str) -> bool:
        """Check whether the feature has a given tag."""
        return any(t.name == name for t in self.tags)

    def outlines(self) -> list[ScenarioOutline]:
        """Return only scenario outlines."""
        return [s for s in self.scenarios if isinstance(s, ScenarioOutline)]

    def plain_scenarios(self) -> list[Scenario]:
        """Return only plain (non-outline) scenarios."""
        return [s for s in self.scenarios if isinstance(s, Scenario)]

    def all_scenarios(self) -> list[ScenarioLike]:
        """Return all scenario-like elements (including those inside rules)."""
        result = list(self.scenarios)
        for rule in self.rules:
            result.extend(rule.scenarios)
        return result

    def all_tags(self) -> list[Tag]:
        """Return all tags (feature + rule + scenario tags)."""
        tags = list(self.tags)
        for s in self.scenarios:
            tags.extend(s.tags)
        for rule in self.rules:
            tags.extend(rule.tags)
            for s in rule.scenarios:
                tags.extend(s.tags)
        return tags

    def all_steps(self):
        """Return every step in the feature (background + scenarios + rules)."""
        from behave_model.model.step import Step

        steps: list[Step] = []
        if self.background:
            steps.extend(self.background.steps)
        for s in self.scenarios:
            steps.extend(s.steps)
        for rule in self.rules:
            steps.extend(rule.all_steps())
        return steps

    def accept(self, visitor: "Visitor") -> None:
        """Accept a visitor."""
        visitor.visit_feature(self)
        if self.background:
            self.background.accept(visitor)
        for s in self.scenarios:
            s.accept(visitor)
        for rule in self.rules:
            rule.accept(visitor)
