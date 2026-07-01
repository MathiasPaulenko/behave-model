"""Tests for the query API."""

from __future__ import annotations

from behave_model.model import Feature, Project, Scenario, Step, Tag
from behave_model.queries import (
    find_feature,
    find_features_with_tag,
    find_outlines,
    find_plain_scenarios,
    find_scenarios,
    find_scenarios_with_tag,
    find_steps,
    find_tag,
)


class TestFindFeature:
    def test_exact_name(self, sample_project):
        f = find_feature(sample_project, "Login")
        assert f is not None
        assert f.name == "Login"

    def test_case_insensitive(self, sample_project):
        f = find_feature(sample_project, "login")
        assert f is not None
        assert f.name == "Login"

    def test_not_found(self, sample_project):
        assert find_feature(sample_project, "Nonexistent") is None

    def test_method_on_project(self, sample_project):
        f = sample_project.find_feature("Login")
        assert f is not None
        assert f.name == "Login"


class TestFindTag:
    def test_found(self, sample_project):
        tag = find_tag(sample_project, "@smoke")
        assert tag is not None
        assert tag.name == "@smoke"

    def test_not_found(self, sample_project):
        assert find_tag(sample_project, "@nonexistent") is None

    def test_method_on_project(self, sample_project):
        tag = sample_project.find_tag("@auth")
        assert tag is not None


class TestFindScenarios:
    def test_by_tag(self, sample_project):
        results = find_scenarios(sample_project, tag="@happy")
        assert len(results) == 1
        assert results[0].name == "Successful login"

    def test_by_name(self, sample_project):
        results = find_scenarios(sample_project, name="Successful login")
        assert len(results) == 1

    def test_by_name_contains(self, sample_project):
        results = find_scenarios(sample_project, name_contains="login")
        assert len(results) >= 2

    def test_method_on_project(self, sample_project):
        results = sample_project.find_scenarios(tag="@error")
        assert len(results) == 1


class TestFindSteps:
    def test_by_keyword(self, sample_project):
        results = find_steps(sample_project, keyword="Given")
        assert len(results) > 0
        assert all(s.keyword == "Given" for s in results)

    def test_by_text_contains(self, sample_project):
        results = find_steps(sample_project, text_contains="cart")
        assert len(results) > 0
        assert all("cart" in s.name.lower() for s in results)

    def test_combined(self, sample_project):
        results = find_steps(sample_project, keyword="When", text_contains="user")
        assert len(results) > 0

    def test_method_on_project(self, sample_project):
        results = sample_project.find_steps(keyword="Then")
        assert len(results) > 0


class TestFindFeaturesWithTag:
    def test_found(self, sample_project):
        results = find_features_with_tag(sample_project, "@smoke")
        assert len(results) == 1
        assert results[0].name == "Login"

    def test_not_found(self, sample_project):
        results = find_features_with_tag(sample_project, "@nonexistent")
        assert len(results) == 0


class TestFindScenariosWithTag:
    def test_found(self, sample_project):
        results = find_scenarios_with_tag(sample_project, "@api")
        assert len(results) == 1
        assert "Login with role" in results[0].name


class TestFindOutlinesAndPlain:
    def test_find_outlines(self, sample_project):
        outlines = find_outlines(sample_project)
        assert len(outlines) >= 2

    def test_find_plain_scenarios(self, sample_project):
        plain = find_plain_scenarios(sample_project)
        assert len(plain) >= 3
        assert all(not isinstance(s, type(None)) for s in plain)
