"""Tests for the parser adapter and loaders."""

from __future__ import annotations

from pathlib import Path

import pytest

from behave_model.exceptions import ParseError
from behave_model.parser.adapter import BehaveParserAdapter
from behave_model.parser.loader import load_feature, load_project
from behave_model.parser.parser import parse_feature, parse_project


class TestParseFeature:
    def test_basic(self):
        text = "Feature: Test\n  Scenario: S1\n    Given a step\n"
        f = parse_feature(text, filename="test.feature")
        assert f.name == "Test"
        assert len(f.scenarios) == 1

    def test_invalid_text_raises(self):
        with pytest.raises(ParseError):
            parse_feature("not valid gherkin at all !!!", filename="bad.feature")


class TestAdapter:
    def test_adapt_simple_feature(self):
        text = "Feature: Login\n  Scenario: Successful\n    Given a step\n    Then another step\n"
        bf = parse_feature(text, filename="login.feature")
        adapter = BehaveParserAdapter()
        f = adapter.adapt_feature(bf, filename="login.feature")
        assert f.name == "Login"
        assert f.location.filename == "login.feature"
        assert len(f.scenarios) == 1
        s = f.scenarios[0]
        assert s.name == "Successful"
        assert len(s.steps) == 2
        assert s.steps[0].keyword == "Given"
        assert s.steps[0].name == "a step"

    def test_adapt_tags(self):
        text = "@smoke @api\nFeature: Test\n  Scenario: S1\n    Given a step\n"
        bf = parse_feature(text, filename="test.feature")
        adapter = BehaveParserAdapter()
        f = adapter.adapt_feature(bf, filename="test.feature")
        assert len(f.tags) == 2
        assert f.tags[0].name == "@smoke"
        assert f.tags[1].name == "@api"

    def test_adapt_background(self):
        text = "Feature: Test\n  Background:\n    Given a setup\n  Scenario: S1\n    When an action\n"
        bf = parse_feature(text, filename="test.feature")
        adapter = BehaveParserAdapter()
        f = adapter.adapt_feature(bf, filename="test.feature")
        assert f.background is not None
        assert len(f.background.steps) == 1
        assert f.background.steps[0].name == "a setup"

    def test_adapt_scenario_outline(self):
        text = (
            "Feature: Test\n"
            "  Scenario Outline: SO <val>\n"
            "    Given a <val>\n"
            "    Examples:\n"
            "      | val |\n"
            "      | a   |\n"
            "      | b   |\n"
        )
        bf = parse_feature(text, filename="test.feature")
        adapter = BehaveParserAdapter()
        f = adapter.adapt_feature(bf, filename="test.feature")
        from behave_model.model.scenario_outline import ScenarioOutline

        so = f.scenarios[0]
        assert isinstance(so, ScenarioOutline)
        assert so.name == "SO <val>"
        assert len(so.examples) == 1
        assert so.examples[0].headers == ["val"]
        assert len(so.examples[0].rows) == 2
        assert so.examples[0].rows[0].cells == ["a"]

    def test_adapt_data_table(self):
        text = (
            "Feature: Test\n"
            "  Scenario: S1\n"
            "    Given data:\n"
            "      | col1 | col2 |\n"
            "      | a    | b    |\n"
        )
        bf = parse_feature(text, filename="test.feature")
        adapter = BehaveParserAdapter()
        f = adapter.adapt_feature(bf, filename="test.feature")
        step = f.scenarios[0].steps[0]
        assert step.data_table is not None
        assert step.data_table.headers == ["col1", "col2"]
        assert step.data_table.rows[0].cells == ["a", "b"]

    def test_adapt_description(self):
        text = "Feature: Test\n  As a user\n  I want something\n  Scenario: S1\n    Given a step\n"
        bf = parse_feature(text, filename="test.feature")
        adapter = BehaveParserAdapter()
        f = adapter.adapt_feature(bf, filename="test.feature")
        assert "As a user" in f.description
        assert "I want something" in f.description

    def test_adapt_project(self):
        text1 = "Feature: F1\n  Scenario: S1\n    Given a step\n"
        text2 = "Feature: F2\n  Scenario: S2\n    Given a step\n"
        bf1 = parse_feature(text1, filename="f1.feature")
        bf2 = parse_feature(text2, filename="f2.feature")
        adapter = BehaveParserAdapter()
        project = adapter.adapt_project([bf1, bf2], source_path=".")
        assert len(project.features) == 2
        assert project.metadata.source_path == "."


class TestLoadFeature:
    def test_load_from_file(self, examples_dir):
        path = examples_dir / "login.feature"
        f = load_feature(path)
        assert f.name == "Login"
        assert len(f.scenarios) == 3

    def test_file_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_feature("nonexistent.feature")


class TestLoadProject:
    def test_load_from_directory(self, examples_dir):
        project = load_project(examples_dir)
        assert len(project.features) >= 3
        names = {f.name for f in project.features}
        assert "Login" in names
        assert "Shopping Cart" in names

    def test_empty_directory(self, tmp_path):
        project = load_project(tmp_path)
        assert len(project.features) == 0

    def test_directory_not_found(self):
        with pytest.raises(FileNotFoundError):
            load_project("/nonexistent/path/xyz")
