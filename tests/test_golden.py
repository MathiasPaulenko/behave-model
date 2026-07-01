"""Golden file tests — parse example features and verify structural integrity."""

from __future__ import annotations

import json
from pathlib import Path

from behave_model.parser.loader import load_feature, load_project
from behave_model.serializers import JsonSerializer, PrettyPrinter

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"


class TestGoldenLogin:
    def test_structure(self):
        f = load_feature(EXAMPLES_DIR / "login.feature")
        assert f.name == "Login"
        assert len(f.tags) == 2
        assert f.background is not None
        assert len(f.background.steps) == 2
        assert len(f.scenarios) == 3

    def test_scenario_names(self):
        f = load_feature(EXAMPLES_DIR / "login.feature")
        names = [s.name for s in f.scenarios]
        assert "Successful login" in names
        assert "Failed login with wrong password" in names
        assert "Login with role <role>" in names

    def test_outline_examples(self):
        f = load_feature(EXAMPLES_DIR / "login.feature")
        from behave_model.model.scenario_outline import ScenarioOutline

        outlines = [s for s in f.scenarios if isinstance(s, ScenarioOutline)]
        assert len(outlines) == 1
        assert len(outlines[0].examples) == 1
        assert outlines[0].examples[0].headers == ["role", "password", "result"]
        assert len(outlines[0].examples[0].rows) == 3

    def test_step_counts(self):
        f = load_feature(EXAMPLES_DIR / "login.feature")
        # background: 2 steps
        # scenario 1: 4 steps
        # scenario 2: 4 steps
        # outline: 3 steps
        assert len(f.all_steps()) == 13


class TestGoldenShopping:
    def test_structure(self):
        f = load_feature(EXAMPLES_DIR / "shopping_cart.feature")
        assert f.name == "Shopping Cart"
        assert len(f.scenarios) == 3

    def test_outline(self):
        f = load_feature(EXAMPLES_DIR / "shopping_cart.feature")
        from behave_model.model.scenario_outline import ScenarioOutline

        outlines = [s for s in f.scenarios if isinstance(s, ScenarioOutline)]
        assert len(outlines) == 1
        assert len(outlines[0].examples[0].rows) == 3


class TestGoldenDataTables:
    def test_structure(self):
        f = load_feature(EXAMPLES_DIR / "data_tables.feature")
        assert f.name == "Data Tables"
        assert len(f.scenarios) == 2

    def test_data_table(self):
        f = load_feature(EXAMPLES_DIR / "data_tables.feature")
        step = f.scenarios[0].steps[0]
        assert step.data_table is not None
        assert step.data_table.headers == ["name", "email", "age"]
        assert len(step.data_table.rows) == 2

    def test_docstring(self):
        f = load_feature(EXAMPLES_DIR / "data_tables.feature")
        step = f.scenarios[1].steps[0]
        assert step.doc_string is not None
        assert "admin" in step.doc_string.content


class TestGoldenProject:
    def test_load_all(self):
        project = load_project(EXAMPLES_DIR)
        assert len(project.features) >= 3
        stats = project.statistics()
        assert stats["features"] >= 3
        assert stats["scenarios"] >= 7
        assert stats["steps"] > 0

    def test_json_serialization(self):
        project = load_project(EXAMPLES_DIR)
        ser = JsonSerializer()
        text = ser.serialize_project(project)
        data = json.loads(text)
        assert data["type"] == "project"
        assert len(data["features"]) >= 3

    def test_pretty_printer_roundtrip(self):
        """Parse -> Print -> Parse should preserve names and counts."""
        project = load_project(EXAMPLES_DIR)
        printer = PrettyPrinter()

        for feature in project.features:
            text = printer.print_feature(feature)
            from behave_model.parser.adapter import BehaveParserAdapter
            from behave_model.parser.parser import parse_feature

            bf = parse_feature(text, filename=feature.location.filename)
            adapter = BehaveParserAdapter()
            f2 = adapter.adapt_feature(bf, filename=feature.location.filename)

            assert f2.name == feature.name
            assert len(f2.scenarios) == len(feature.scenarios)
            assert len(f2.all_steps()) == len(feature.all_steps())
