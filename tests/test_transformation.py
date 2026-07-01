"""Tests for transformations."""

from __future__ import annotations

import pytest

from behave_model.exceptions import TransformationError
from behave_model.transformations import (
    add_tag_to_feature,
    normalize_whitespace,
    remove_tag,
    rename_scenario,
    rename_tag,
    sort_features,
    sort_scenarios,
    sort_tags,
)


class TestRenameTag:
    def test_rename(self, sample_project):
        rename_tag(sample_project, "@smoke", "@critical")
        assert sample_project.find_tag("@smoke") is None
        assert sample_project.find_tag("@critical") is not None

    def test_same_name_raises(self, sample_project):
        with pytest.raises(TransformationError):
            rename_tag(sample_project, "@smoke", "@smoke")


class TestRenameScenario:
    def test_rename(self, sample_project):
        rename_scenario(sample_project, "Successful login", "Happy login")
        results = sample_project.find_scenarios(name="Happy login")
        assert len(results) == 1

    def test_not_found(self, sample_project):
        with pytest.raises(TransformationError):
            rename_scenario(sample_project, "Nonexistent", "New name")

    def test_same_name_raises(self, sample_project):
        with pytest.raises(TransformationError):
            rename_scenario(sample_project, "Successful login", "Successful login")


class TestSortTags:
    def test_sort(self, sample_project):
        # Add tags in reverse order on a feature
        from behave_model.model import Tag

        sample_project.features[0].tags = [
            Tag(name="@zzz"),
            Tag(name="@aaa"),
            Tag(name="@mmm"),
        ]
        sort_tags(sample_project)
        names = [t.name for t in sample_project.features[0].tags]
        assert names == ["@aaa", "@mmm", "@zzz"]


class TestSortFeatures:
    def test_sort_by_name(self, sample_project):
        sort_features(sample_project)
        names = [f.name for f in sample_project.features]
        assert names == sorted(names)

    def test_sort_by_filename(self, sample_project):
        sort_features(sample_project, key="filename")
        filenames = [f.location.filename for f in sample_project.features]
        assert filenames == sorted(filenames)

    def test_invalid_key(self, sample_project):
        with pytest.raises(TransformationError):
            sort_features(sample_project, key="invalid")


class TestSortScenarios:
    def test_sort(self, login_feature):
        from behave_model.model import Project

        project = Project(features=[login_feature])
        sort_scenarios(project)
        names = [s.name for s in login_feature.scenarios]
        assert names == sorted(names)


class TestNormalizeWhitespace:
    def test_normalize_step(self):
        from behave_model.model import Project, Feature, Scenario, Step

        project = Project(
            features=[
                Feature(
                    name="  Test   Feature  ",
                    scenarios=[
                        Scenario(
                            name="  Test   Scenario  ",
                            steps=[Step(keyword="Given", name="  some   step  ")],
                        ),
                    ],
                )
            ]
        )
        normalize_whitespace(project)
        assert project.features[0].name == "Test Feature"
        assert project.features[0].scenarios[0].name == "Test Scenario"
        assert project.features[0].scenarios[0].steps[0].name == "some step"


class TestRemoveTag:
    def test_remove(self, sample_project):
        remove_tag(sample_project, "@smoke")
        assert sample_project.find_tag("@smoke") is None

    def test_remove_nonexistent_silently(self, sample_project):
        remove_tag(sample_project, "@nonexistent")
        # Should not raise


class TestAddTagToFeature:
    def test_add(self, sample_project):
        add_tag_to_feature(sample_project, "Login", "@new_tag")
        f = sample_project.find_feature("Login")
        assert f.has_tag("@new_tag")

    def test_add_duplicate_noop(self, sample_project):
        add_tag_to_feature(sample_project, "Login", "@smoke")
        f = sample_project.find_feature("Login")
        assert sum(1 for t in f.tags if t.name == "@smoke") == 1

    def test_feature_not_found(self, sample_project):
        with pytest.raises(TransformationError):
            add_tag_to_feature(sample_project, "Nonexistent", "@tag")
