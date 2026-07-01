"""Tests for serializers (dict, JSON, pretty printer)."""

from __future__ import annotations

import json

from behave_model.model import (
    Feature,
    Project,
    Scenario,
    Step,
    Table,
    TableRow,
    Tag,
)
from behave_model.serializers import DictSerializer, JsonSerializer, PrettyPrinter


class TestDictSerializer:
    def test_serialize_project(self, sample_project):
        ser = DictSerializer()
        data = ser.serialize_project(sample_project)
        assert data["type"] == "project"
        assert len(data["features"]) == 2
        assert "statistics" in data

    def test_serialize_feature(self, login_feature):
        ser = DictSerializer()
        data = ser.serialize_feature(login_feature)
        assert data["type"] == "feature"
        assert data["name"] == "Login"
        assert len(data["tags"]) == 2
        assert data["background"] is not None
        assert len(data["scenarios"]) == 3

    def test_serialize_scenario(self, login_feature):
        ser = DictSerializer()
        s = login_feature.scenarios[0]
        data = ser.serialize_scenario(s)
        assert data["type"] == "scenario"
        assert data["name"] == "Successful login"
        assert len(data["steps"]) == 4

    def test_serialize_step(self):
        ser = DictSerializer()
        step = Step(keyword="Given", name="a step")
        data = ser.serialize_step(step)
        assert data["keyword"] == "Given"
        assert data["name"] == "a step"

    def test_serialize_table(self):
        ser = DictSerializer()
        table = Table(
            headers=["a", "b"],
            rows=[TableRow(cells=["1", "2"])],
        )
        data = ser.serialize_table(table)
        assert data["headers"] == ["a", "b"]
        assert data["rows"] == [["1", "2"]]

    def test_serialize_tag(self):
        ser = DictSerializer()
        tag = Tag(name="@smoke")
        data = ser.serialize_tag(tag)
        assert data["name"] == "@smoke"


class TestJsonSerializer:
    def test_serialize_project(self, sample_project):
        ser = JsonSerializer()
        text = ser.serialize_project(sample_project)
        data = json.loads(text)
        assert data["type"] == "project"
        assert len(data["features"]) == 2

    def test_serialize_feature(self, login_feature):
        ser = JsonSerializer()
        text = ser.serialize_feature(login_feature)
        data = json.loads(text)
        assert data["name"] == "Login"

    def test_valid_json(self, sample_project):
        ser = JsonSerializer()
        text = ser.serialize_project(sample_project)
        # Should not raise
        json.loads(text)


class TestPrettyPrinter:
    def test_print_feature(self, login_feature):
        printer = PrettyPrinter()
        text = printer.print_feature(login_feature)
        assert "Feature: Login" in text
        assert "Background:" in text
        assert "Scenario: Successful login" in text
        assert "Scenario Outline: Login with role" in text

    def test_print_project(self, sample_project):
        printer = PrettyPrinter()
        text = printer.print_project(sample_project)
        assert "Feature: Login" in text
        assert "Feature: Shopping Cart" in text

    def test_print_scenario(self):
        printer = PrettyPrinter()
        s = Scenario(
            name="Test",
            tags=[Tag(name="@smoke")],
            steps=[Step(keyword="Given", name="a step")],
        )
        text = printer._print_scenario(s)
        joined = "\n".join(text)
        assert "@smoke" in joined
        assert "Scenario: Test" in joined
        assert "Given a step" in joined

    def test_print_table(self):
        printer = PrettyPrinter()
        table = Table(
            headers=["name", "age"],
            rows=[TableRow(cells=["Alice", "30"])],
        )
        lines = printer._print_table(table, indent=4)
        text = "\n".join(lines)
        assert "| name  | age |" in text
        assert "| Alice | 30  |" in text

    def test_roundtrip(self, login_feature):
        """Print and re-parse should preserve key structure."""
        printer = PrettyPrinter()
        text = printer.print_feature(login_feature)

        from behave_model.parser.adapter import BehaveParserAdapter
        from behave_model.parser.parser import parse_feature

        bf = parse_feature(text, filename="roundtrip.feature")
        adapter = BehaveParserAdapter()
        f2 = adapter.adapt_feature(bf, filename="roundtrip.feature")

        assert f2.name == login_feature.name
        assert len(f2.scenarios) == len(login_feature.scenarios)
        assert len(f2.all_steps()) == len(login_feature.all_steps())

    def test_print_docstring(self):
        from behave_model.model import DocString

        printer = PrettyPrinter()
        step = Step(
            keyword="Given",
            name="a payload",
            doc_string=DocString(content='{"key": "value"}', content_type="json"),
        )
        lines = printer._print_step(step, indent=4)
        text = "\n".join(lines)
        assert '"""json' in text
        assert '{"key": "value"}' in text
        assert text.count('"""') == 2
