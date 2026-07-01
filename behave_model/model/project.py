"""Project model — the root of the domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from behave_model.model.background import Background
from behave_model.model.feature import Feature, ScenarioLike
from behave_model.model.metadata import Metadata
from behave_model.model.step import Step
from behave_model.model.tag import Tag


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
        avg_steps = (steps_count / scenarios_count) if scenarios_count else 0.0
        unique_tags = {t.name for t in tags}
        return {
            "features": features_count,
            "scenarios": scenarios_count,
            "steps": steps_count,
            "average_steps_per_scenario": round(avg_steps, 2),
            "tags": len(unique_tags),
            "total_tag_usages": len(tags),
        }

    # -- visitor / traversal -------------------------------------------------

    def accept(self, visitor) -> None:
        """Accept a visitor."""
        visitor.visit_project(self)
        for f in self.features:
            f.accept(visitor)

    def walk(self, strategy: str = "dfs") -> Iterator:
        """Traverse the entire model tree.

        Args:
            strategy: ``"dfs"`` for depth-first (default) or ``"bfs"``
                for breadth-first.

        Yields:
            Every node in the tree (Project, Feature, Background, Scenario,
            ScenarioOutline, Examples, Step, Table, DocString, Tag).
        """
        if strategy == "bfs":
            yield from self._walk_bfs()
        else:
            yield from self._walk_dfs()

    def _walk_dfs(self) -> Iterator:
        yield self
        for feature in self.features:
            yield from self._walk_feature_dfs(feature)

    def _walk_feature_dfs(self, feature: Feature) -> Iterator:
        yield feature
        for tag in feature.tags:
            yield tag
        if feature.background:
            yield feature.background
            for step in feature.background.steps:
                yield from self._walk_step(step)
        for scenario in feature.scenarios:
            yield from self._walk_scenario(scenario)
        for rule in feature.rules:
            yield from self._walk_rule_dfs(rule)

    def _walk_rule_dfs(self, rule) -> Iterator:
        yield rule
        for tag in rule.tags:
            yield tag
        if rule.background:
            yield rule.background
            for step in rule.background.steps:
                yield from self._walk_step(step)
        for scenario in rule.scenarios:
            yield from self._walk_scenario(scenario)

    def _walk_scenario(self, scenario: ScenarioLike) -> Iterator:
        yield scenario
        for tag in scenario.tags:
            yield tag
        for step in scenario.steps:
            yield from self._walk_step(step)
        # scenario outline examples
        from behave_model.model.scenario_outline import ScenarioOutline

        if isinstance(scenario, ScenarioOutline):
            for ex in scenario.examples:
                yield ex
                yield ex.table

    def _walk_step(self, step: Step) -> Iterator:
        yield step
        if step.doc_string:
            yield step.doc_string
        if step.data_table:
            yield step.data_table

    def _walk_bfs(self) -> Iterator:
        queue: list = [self]
        while queue:
            node = queue.pop(0)
            yield node
            queue.extend(self._children(node))

    def _children(self, node) -> list:
        if isinstance(node, Project):
            return list(node.features)
        if isinstance(node, Feature):
            children: list = list(node.tags)
            if node.background:
                children.append(node.background)
            children.extend(node.scenarios)
            children.extend(node.rules)
            return children
        if isinstance(node, Background):
            return list(node.steps)
        from behave_model.model.rule import Rule

        if isinstance(node, Rule):
            children = list(node.tags)
            if node.background:
                children.append(node.background)
            children.extend(node.scenarios)
            return children
        from behave_model.model.scenario_outline import ScenarioOutline

        if isinstance(node, (Scenario, ScenarioOutline)):
            children = list(node.tags)
            children.extend(node.steps)
            if isinstance(node, ScenarioOutline):
                children.extend(node.examples)
            return children
        from behave_model.model.examples import Examples

        if isinstance(node, Examples):
            return [node.table]
        if isinstance(node, Step):
            children = []
            if node.doc_string:
                children.append(node.doc_string)
            if node.data_table:
                children.append(node.data_table)
            return children
        return []


# Late import to avoid circular dependency at module load time
from behave_model.model.scenario import Scenario  # noqa: E402
