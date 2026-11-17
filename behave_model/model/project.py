"""Project model — the root of the domain model."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.background import Background
from behave_model.model.examples import Examples
from behave_model.model.feature import Feature, ScenarioLike
from behave_model.model.metadata import Metadata
from behave_model.model.rule import Rule
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step
from behave_model.model.tag import Tag

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Project:
    """The root container for a parsed Behave project.

    Attributes:
        features: List of Feature objects.
        global_tags: Tags that apply project-wide.
        metadata: Project-level metadata.
    """

    features: list[Feature] = field(default_factory=list)
    global_tags: list[Tag] = field(default_factory=list)
    metadata: Metadata = field(default_factory=Metadata)

    # -- container protocol --------------------------------------------------

    def __iter__(self) -> Iterator[Feature]:
        return iter(self.features)

    def __len__(self) -> int:
        return len(self.features)

    def __getitem__(self, index: int) -> Feature:
        return self.features[index]

    # -- query helpers -------------------------------------------------------

    def all_scenarios(self) -> list[ScenarioLike]:
        """Return every scenario across all features (including rule scenarios)."""
        result: list[ScenarioLike] = []
        for f in self.features:
            result.extend(f.all_scenarios())
        return result

    def all_steps(self) -> list[Step]:
        """Return every step across all features."""
        result: list[Step] = []
        for f in self.features:
            result.extend(f.all_steps())
        return result

    def all_tags(self) -> list[Tag]:
        """Return every tag across all features (including global tags)."""
        tags = list(self.global_tags)
        for f in self.features:
            tags.extend(f.all_tags())
        return tags

    # -- statistics ----------------------------------------------------------

    def statistics(self) -> dict[str, int | float]:
        """Return a dictionary of project metrics."""
        features_count = len(self.features)
        scenarios = self.all_scenarios()
        steps = self.all_steps()
        tags = self.all_tags()
        scenarios_count = len(scenarios)
        steps_count = len(steps)
        scenario_steps = sum(len(s.steps) for s in scenarios)
        avg_steps = (scenario_steps / scenarios_count) if scenarios_count else 0.0
        unique_tags = {t.name for t in tags}
        outlines = [s for s in scenarios if isinstance(s, ScenarioOutline)]
        rules_count = sum(len(f.rules) for f in self.features)
        example_rows = sum(len(ex.table.rows) for s in outlines for ex in s.examples)
        return {
            "features": features_count,
            "scenarios": scenarios_count,
            "scenario_outlines": len(outlines),
            "rules": rules_count,
            "steps": steps_count,
            "average_steps_per_scenario": round(avg_steps, 2),
            "tags": len(unique_tags),
            "total_tag_usages": len(tags),
            "examples": example_rows,
        }

    # -- visitor / traversal -------------------------------------------------

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_project(self)
        for tag in self.global_tags:
            tag.accept(visitor)
        for f in self.features:
            f.accept(visitor)

    def walk(self, strategy: str = "dfs") -> Iterator:
        """Traverse the entire model tree.

        Args:
            strategy: ``"dfs"`` for depth-first (default) or ``"bfs"``
                for breadth-first.

        Returns:
            An iterator over every node in the tree (Project, Tag, Feature,
            Background, Rule, Scenario, ScenarioOutline, Examples, Step,
            Table, DocString, Comment), in the same order ``accept()`` uses.

        Raises:
            ValueError: If ``strategy`` is not ``"dfs"`` or ``"bfs"``.
        """
        if strategy == "dfs":
            return self._walk_dfs()
        if strategy == "bfs":
            return self._walk_bfs()
        raise ValueError(f"Unknown walk strategy: {strategy!r} (expected 'dfs' or 'bfs')")

    def _walk_dfs(self) -> Iterator:
        yield self
        yield from self.global_tags
        for feature in self.features:
            yield from self._walk_feature_dfs(feature)

    def _walk_feature_dfs(self, feature: Feature) -> Iterator:
        yield feature
        yield from feature.tags
        if feature.background is not None:
            yield feature.background
            for step in feature.background.steps:
                yield from self._walk_step(step)
        for scenario in feature.scenarios:
            yield from self._walk_scenario(scenario)
        for rule in feature.rules:
            yield from self._walk_rule_dfs(rule)
        yield from feature.comments

    def _walk_rule_dfs(self, rule) -> Iterator:
        yield rule
        yield from rule.tags
        if rule.background is not None:
            yield rule.background
            for step in rule.background.steps:
                yield from self._walk_step(step)
        for scenario in rule.scenarios:
            yield from self._walk_scenario(scenario)
        yield from rule.comments

    def _walk_scenario(self, scenario: ScenarioLike) -> Iterator:
        yield scenario
        yield from scenario.tags
        for step in scenario.steps:
            yield from self._walk_step(step)
        if isinstance(scenario, ScenarioOutline):
            for ex in scenario.examples:
                yield ex
                yield from ex.tags
                if ex.table is not None:
                    yield ex.table
        yield from scenario.comments

    def _walk_step(self, step: Step) -> Iterator:
        yield step
        if step.doc_string is not None:
            yield step.doc_string
        if step.data_table is not None:
            yield step.data_table
        yield from step.comments

    def _walk_bfs(self) -> Iterator:
        queue = deque([self])
        while queue:
            node = queue.popleft()
            yield node
            queue.extend(self._children(node))

    def _children(self, node) -> list:
        if isinstance(node, Project):
            return [*node.global_tags, *node.features]
        if isinstance(node, Feature):
            children: list = list(node.tags)
            if node.background is not None:
                children.append(node.background)
            children.extend(node.scenarios)
            children.extend(node.rules)
            children.extend(node.comments)
            return children
        if isinstance(node, Background):
            return list(node.steps)
        if isinstance(node, Rule):
            children = list(node.tags)
            if node.background is not None:
                children.append(node.background)
            children.extend(node.scenarios)
            children.extend(node.comments)
            return children
        if isinstance(node, (Scenario, ScenarioOutline)):
            children = list(node.tags)
            children.extend(node.steps)
            if isinstance(node, ScenarioOutline):
                children.extend(node.examples)
            children.extend(node.comments)
            return children
        if isinstance(node, Examples):
            return [*node.tags, node.table] if node.table is not None else list(node.tags)
        if isinstance(node, Step):
            children = []
            if node.doc_string is not None:
                children.append(node.doc_string)
            if node.data_table is not None:
                children.append(node.data_table)
            children.extend(node.comments)
            return children
        return []
