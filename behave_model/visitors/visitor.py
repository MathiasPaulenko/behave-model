"""Generic visitor pattern for the domain model.

Subclass :class:`Visitor` and override the ``visit_*`` methods you need.
Each method receives the corresponding node and defaults to a no-op,
so you only implement what you care about.
"""

from __future__ import annotations

from behave_model.model.background import Background
from behave_model.model.docstring import DocString
from behave_model.model.examples import Examples
from behave_model.model.feature import Feature
from behave_model.model.project import Project
from behave_model.model.rule import Rule
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step
from behave_model.model.table import Table
from behave_model.model.tag import Tag


class Visitor:
    """Base visitor class.

    Override any ``visit_*`` method to react to that node type.
    The default implementations do nothing, allowing selective
    implementation.
    """

    def visit_project(self, project: Project) -> None:
        """Called when visiting a Project node."""

    def visit_feature(self, feature: Feature) -> None:
        """Called when visiting a Feature node."""

    def visit_rule(self, rule: Rule) -> None:
        """Called when visiting a Rule node (Gherkin v6)."""

    def visit_background(self, background: Background) -> None:
        """Called when visiting a Background node."""

    def visit_scenario(self, scenario: Scenario) -> None:
        """Called when visiting a Scenario node."""

    def visit_scenario_outline(self, outline: ScenarioOutline) -> None:
        """Called when visiting a ScenarioOutline node."""

    def visit_examples(self, examples: Examples) -> None:
        """Called when visiting an Examples node."""

    def visit_step(self, step: Step) -> None:
        """Called when visiting a Step node."""

    def visit_tag(self, tag: Tag) -> None:
        """Called when visiting a Tag node."""

    def visit_table(self, table: Table) -> None:
        """Called when visiting a Table node."""

    def visit_docstring(self, docstring: DocString) -> None:
        """Called when visiting a DocString node."""


class CountingVisitor(Visitor):
    """A visitor that counts each node type.

    After traversal, access ``self.counts`` for a dict of type name -> count.
    """

    def __init__(self) -> None:
        self.counts: dict[str, int] = {}

    def _bump(self, key: str) -> None:
        self.counts[key] = self.counts.get(key, 0) + 1

    def visit_project(self, project: Project) -> None:
        self._bump("project")

    def visit_feature(self, feature: Feature) -> None:
        self._bump("feature")

    def visit_rule(self, rule: Rule) -> None:
        self._bump("rule")

    def visit_background(self, background: Background) -> None:
        self._bump("background")

    def visit_scenario(self, scenario: Scenario) -> None:
        self._bump("scenario")

    def visit_scenario_outline(self, outline: ScenarioOutline) -> None:
        self._bump("scenario_outline")

    def visit_examples(self, examples: Examples) -> None:
        self._bump("examples")

    def visit_step(self, step: Step) -> None:
        self._bump("step")

    def visit_tag(self, tag: Tag) -> None:
        self._bump("tag")

    def visit_table(self, table: Table) -> None:
        self._bump("table")

    def visit_docstring(self, docstring: DocString) -> None:
        self._bump("docstring")


class CollectingVisitor(Visitor):
    """A visitor that collects nodes by type.

    After traversal, access ``self.collection[type_name]`` for a list of nodes.
    """

    def __init__(self) -> None:
        self.collection: dict[str, list] = {}

    def _collect(self, key: str, node) -> None:
        self.collection.setdefault(key, []).append(node)

    def visit_feature(self, feature: Feature) -> None:
        self._collect("feature", feature)

    def visit_rule(self, rule: Rule) -> None:
        self._collect("rule", rule)

    def visit_background(self, background: Background) -> None:
        self._collect("background", background)

    def visit_scenario(self, scenario: Scenario) -> None:
        self._collect("scenario", scenario)

    def visit_scenario_outline(self, outline: ScenarioOutline) -> None:
        self._collect("scenario_outline", outline)

    def visit_step(self, step: Step) -> None:
        self._collect("step", step)

    def visit_tag(self, tag: Tag) -> None:
        self._collect("tag", tag)
