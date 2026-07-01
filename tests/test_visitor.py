"""Tests for the visitor pattern and traversal."""

from __future__ import annotations

from behave_model.model import (
    Project,
    ScenarioOutline,
    Tag,
)
from behave_model.visitors import CollectingVisitor, CountingVisitor, Visitor


class TestVisitor:
    def test_counting_visitor(self, sample_project):
        visitor = CountingVisitor()
        sample_project.accept(visitor)
        assert visitor.counts["project"] == 1
        assert visitor.counts["feature"] == 2
        assert visitor.counts["scenario"] >= 2
        assert visitor.counts["step"] > 0

    def test_collecting_visitor(self, sample_project):
        visitor = CollectingVisitor()
        sample_project.accept(visitor)
        assert "feature" in visitor.collection
        assert len(visitor.collection["feature"]) == 2
        assert "step" in visitor.collection

    def test_custom_visitor(self, sample_project):
        class StepCollector(Visitor):
            def __init__(self):
                self.steps = []

            def visit_step(self, step):
                self.steps.append(step.full_text)

        v = StepCollector()
        sample_project.accept(v)
        assert len(v.steps) > 0
        assert all(" " in s for s in v.steps)

    def test_visitor_visits_outline_steps(self, sample_project):
        class StepCounter(Visitor):
            def __init__(self):
                self.count = 0

            def visit_step(self, step):
                self.count += 1

        v = StepCounter()
        sample_project.accept(v)
        # login feature has background(2) + scenario1(4) + scenario2(4) + outline(3) = 13
        # shopping has scenario1(3) + outline(3) = 6
        assert v.count == 19


class TestTraversal:
    def test_dfs_walk(self, sample_project):
        nodes = list(sample_project.walk())
        # Should include Project, Features, Tags, Backgrounds, Scenarios, Steps, etc.
        types = [type(n).__name__ for n in nodes]
        assert "Project" in types
        assert "Feature" in types
        assert "Scenario" in types
        assert "Step" in types

    def test_bfs_walk(self, sample_project):
        nodes = list(sample_project.walk(strategy="bfs"))
        types = [type(n).__name__ for n in nodes]
        assert "Project" in types
        assert "Feature" in types

    def test_dfs_starts_with_project(self, sample_project):
        nodes = list(sample_project.walk())
        assert isinstance(nodes[0], Project)

    def test_bfs_starts_with_project(self, sample_project):
        nodes = list(sample_project.walk(strategy="bfs"))
        assert isinstance(nodes[0], Project)

    def test_dfs_and_bfs_same_count(self, sample_project):
        dfs_nodes = list(sample_project.walk())
        bfs_nodes = list(sample_project.walk(strategy="bfs"))
        assert len(dfs_nodes) == len(bfs_nodes)

    def test_walk_includes_tags(self, sample_project):
        nodes = list(sample_project.walk())
        tag_nodes = [n for n in nodes if isinstance(n, Tag)]
        assert len(tag_nodes) > 0

    def test_walk_includes_scenario_outlines(self, sample_project):
        nodes = list(sample_project.walk())
        outline_nodes = [n for n in nodes if isinstance(n, ScenarioOutline)]
        assert len(outline_nodes) >= 2

    def test_walk_empty_project(self):
        p = Project()
        nodes = list(p.walk())
        assert len(nodes) == 1
        assert isinstance(nodes[0], Project)
