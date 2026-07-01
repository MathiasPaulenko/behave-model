"""Tests for statistics and utils."""

from __future__ import annotations

from behave_model.model import Feature, Project, Scenario, Step, Tag
from behave_model.utils import (
    count_by_type,
    feature_filenames,
    flatten_steps,
    unique_tag_names,
)


class TestStatistics:
    def test_empty_project(self):
        p = Project()
        stats = p.statistics()
        assert stats["features"] == 0
        assert stats["scenarios"] == 0
        assert stats["steps"] == 0
        assert stats["average_steps_per_scenario"] == 0.0
        assert stats["tags"] == 0

    def test_sample_project(self, sample_project):
        stats = sample_project.statistics()
        assert stats["features"] == 2
        assert stats["scenarios"] == 5
        assert stats["steps"] > 0
        assert stats["average_steps_per_scenario"] > 0
        assert stats["tags"] > 0

    def test_tags_count_unique(self):
        p = Project(
            features=[
                Feature(
                    name="F1",
                    tags=[Tag(name="@a"), Tag(name="@b")],
                    scenarios=[
                        Scenario(name="S1", tags=[Tag(name="@a")]),
                    ],
                )
            ]
        )
        stats = p.statistics()
        # @a appears twice, @b once -> 2 unique
        assert stats["tags"] == 2
        assert stats["total_tag_usages"] == 3


class TestUtils:
    def test_count_by_type(self, sample_project):
        counts = count_by_type(sample_project)
        assert counts["Project"] == 1
        assert counts["Feature"] == 2
        assert counts["Step"] > 0

    def test_flatten_steps(self, sample_project):
        steps = flatten_steps(sample_project)
        assert len(steps) > 0
        assert all(" " in s for s in steps)

    def test_unique_tag_names(self, sample_project):
        tags = unique_tag_names(sample_project)
        assert len(tags) > 0
        assert tags == sorted(tags)
        assert all(t.startswith("@") for t in tags)

    def test_feature_filenames(self, sample_project):
        filenames = feature_filenames(sample_project)
        assert len(filenames) == 2
        assert all(f.endswith(".feature") for f in filenames)
