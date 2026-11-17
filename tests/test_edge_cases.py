"""Regression tests for edge cases found during the stabilization audit."""

from __future__ import annotations

import pytest

from behave_model.exceptions import (
    ParseError,
    SerializationError,
    TransformationError,
)
from behave_model.model import (
    Comment,
    DocString,
    Examples,
    Feature,
    Location,
    Project,
    Scenario,
    ScenarioOutline,
    Step,
    Table,
    TableRow,
    Tag,
)
from behave_model.parser import (
    BehaveParserAdapter,
    load_feature,
    load_project,
    parse_feature,
)
from behave_model.serializers import JsonSerializer, PrettyPrinter
from behave_model.transformations import (
    add_tag_to_feature,
    normalize_whitespace,
    remove_tag,
    rename_tag,
)
from behave_model.validation import ValidationRule, Validator
from behave_model.visitors import Visitor

OUTLINE_NO_TABLE = """\
Feature: F
  Scenario Outline: S
    Given a step
    Examples:
"""

ES_FEATURE = """\
# language: es
Característica: Login
  Escenario: Entrar
    Dado un usuario
"""


class TestParserEdgeCases:
    def test_empty_text_raises_parse_error(self):
        with pytest.raises(ParseError, match="No feature found"):
            parse_feature("")

    def test_whitespace_only_raises_parse_error(self):
        with pytest.raises(ParseError, match="No feature found"):
            parse_feature("   \n\t\n  ")

    def test_comments_only_raises_parse_error(self):
        with pytest.raises(ParseError, match="No feature found"):
            parse_feature("# just a comment\n# another one\n")

    def test_utf8_bom_is_stripped(self):
        feature = parse_feature("\ufeffFeature: BOM\n")
        assert feature.name == "BOM"

    def test_non_string_text_raises_type_error(self):
        with pytest.raises(TypeError, match="text must be str"):
            parse_feature(123)
        with pytest.raises(TypeError):
            parse_feature(None)

    def test_adapt_feature_none_raises_parse_error(self):
        with pytest.raises(ParseError, match="empty parse result"):
            BehaveParserAdapter().adapt_feature(None)

    def test_examples_without_table_gets_empty_table(self):
        adapter = BehaveParserAdapter()
        feature = adapter.adapt_feature(parse_feature(OUTLINE_NO_TABLE))
        outline = feature.scenarios[0]
        assert isinstance(outline.examples[0].table, Table)
        assert outline.examples[0].table.headers == []
        assert outline.examples[0].table.rows == []
        # downstream consumers must not blow up on the empty table
        assert outline.expand() == []

    def test_table_location_line_is_preserved(self):
        text = "Feature: F\n  Scenario: S\n    Given a step\n      | a | b |\n      | 1 | 2 |\n"
        feature = BehaveParserAdapter().adapt_feature(parse_feature(text))
        table = feature.scenarios[0].steps[0].data_table
        assert table.location.line == 4

    def test_empty_docstring_is_preserved(self):
        text = 'Feature: F\n  Scenario: S\n    Given a step\n      """\n      """\n'
        feature = BehaveParserAdapter().adapt_feature(parse_feature(text))
        step = feature.scenarios[0].steps[0]
        assert step.doc_string is not None
        assert step.doc_string.content == ""

    def test_parse_project_with_empty_text_raises(self):
        with pytest.raises(ParseError):
            parse_feature("")


class TestLoaderEdgeCases:
    def test_empty_file_raises_parse_error(self, tmp_path):
        p = tmp_path / "empty.feature"
        p.write_text("", encoding="utf-8")
        with pytest.raises(ParseError, match="No feature found"):
            load_feature(p)

    def test_comments_only_file_raises_parse_error(self, tmp_path):
        p = tmp_path / "comments.feature"
        p.write_text("# nothing here\n", encoding="utf-8")
        with pytest.raises(ParseError, match="No feature found"):
            load_feature(p)

    def test_bom_file_parses(self, tmp_path):
        p = tmp_path / "bom.feature"
        p.write_bytes("Feature: BOM\n".encode("utf-8-sig"))
        assert load_feature(p).name == "BOM"

    def test_non_utf8_file_raises_parse_error(self, tmp_path):
        p = tmp_path / "latin1.feature"
        p.write_bytes("Feature: Olá\n".encode("latin-1"))
        with pytest.raises(ParseError, match="Cannot decode"):
            load_feature(p)

    def test_feature_named_directory_is_skipped(self, tmp_path):
        (tmp_path / "ok.feature").write_text("Feature: OK\n", encoding="utf-8")
        (tmp_path / "tricky.feature").mkdir()
        project = load_project(tmp_path)
        assert [f.name for f in project.features] == ["OK"]

    def test_non_regular_file_raises_oserror(self, tmp_path):
        fifo = tmp_path / "pipe.feature"
        if hasattr(__import__("os"), "mkfifo"):
            __import__("os").mkfifo(fifo)
            with pytest.raises(OSError):
                load_feature(fifo)


class TestTagNormalization:
    def test_tag_name_gets_leading_at(self):
        assert Tag(name="smoke").name == "@smoke"
        assert Tag(name="@smoke").name == "@smoke"
        assert Tag(name="").name == ""

    def test_has_tag_without_at(self, sample_project):
        feature = next(f for f in sample_project.features if f.tags)
        bare = feature.tags[0].name.lstrip("@")
        assert feature.has_tag(bare)
        assert feature.has_tag("@" + bare)

    def test_query_functions_accept_bare_names(self, sample_project):
        tag = sample_project.features[0].tags[0].name
        bare = tag.lstrip("@")
        assert sample_project.find_tag(bare) is not None
        assert sample_project.find_scenarios(tag=bare)
        assert sample_project.find_scenarios_with_tag(bare)
        assert sample_project.find_features_with_tag(bare)


class TestExamplesTableInvariant:
    def test_none_table_normalized_to_empty(self):
        ex = Examples(table=None)
        assert isinstance(ex.table, Table)
        assert ex.table.headers == []
        assert ex.table.rows == []

    def test_walk_survives_reassigned_none_table(self):
        outline = ScenarioOutline(name="o", examples=[Examples()])
        outline.examples[0].table = None  # post-construction pathological input
        feature = Feature(name="f", scenarios=[outline])
        nodes = list(Project(features=[feature]).walk())
        assert not any(n is None for n in nodes)


class TestTraversalConsistency:
    def test_walk_includes_global_tags(self):
        project = Project(global_tags=[Tag("@wip")])
        nodes = list(project.walk())
        assert any(isinstance(n, Tag) and n.name == "@wip" for n in nodes)
        bfs_nodes = list(project.walk(strategy="bfs"))
        assert any(isinstance(n, Tag) and n.name == "@wip" for n in bfs_nodes)

    def test_accept_visits_global_tags(self):
        class TagCounter(Visitor):
            def __init__(self):
                self.count = 0

            def visit_tag(self, tag):
                self.count += 1

        project = Project(global_tags=[Tag("@a"), Tag("@b")])
        counter = TagCounter()
        project.accept(counter)
        assert counter.count == 2

    def test_dfs_order_matches_accept_order(self, sample_project):
        # DFS must yield each node's children in the same relative order
        # that accept() visits them (comments last).
        feature = Feature(
            name="f",
            comments=[Comment(text="# tail")],
            scenarios=[Scenario(name="s", comments=[Comment(text="# s")])],
        )
        nodes = list(Project(features=[feature]).walk())
        comment = next(n for n in nodes if isinstance(n, Comment))
        scenario = next(n for n in nodes if isinstance(n, Scenario))
        assert nodes.index(comment) > nodes.index(scenario)

    def test_invalid_strategy_raises_eagerly(self, sample_project):
        with pytest.raises(ValueError, match="Unknown walk strategy"):
            sample_project.walk(strategy="bogus")


class TestTransformationEdgeCases:
    def test_rename_tag_not_found_raises(self, sample_project):
        with pytest.raises(TransformationError, match="No tag named"):
            rename_tag(sample_project, "@doesnotexist", "@new")

    def test_rename_tag_normalizes_names(self, sample_project):
        tag = sample_project.features[0].tags[0].name
        rename_tag(sample_project, tag.lstrip("@"), "renamed")
        assert "@renamed" in {t.name for t in sample_project.all_tags()}

    def test_rename_tag_replaces_objects(self, sample_project):
        feature = sample_project.features[0]
        original = feature.tags[0]
        rename_tag(sample_project, original.name, "@brand")
        assert original.name != "@brand"  # original object untouched
        assert feature.tags[0].name == "@brand"
        assert feature.tags[0].location == original.location

    def test_remove_tag_normalizes_name(self, sample_project):
        tag = sample_project.features[0].tags[0].name
        remove_tag(sample_project, tag.lstrip("@"))
        assert tag not in {t.name for t in sample_project.all_tags()}

    def test_add_tag_normalizes_name(self, sample_project):
        feature = sample_project.features[0]
        add_tag_to_feature(sample_project, feature.name, "newtag")
        assert feature.has_tag("@newtag")

    def test_normalize_whitespace_covers_backgrounds_and_examples(self):
        from behave_model.model import Background

        outline = ScenarioOutline(
            name="  spaced   out ",
            steps=[Step(keyword=" Given ", name="  a   step ")],
            examples=[Examples(name="  ex   name ")],
        )
        feature = Feature(
            name="  My   Feature ",
            background=Background(name="  bg   name ", steps=[]),
            scenarios=[outline],
        )
        normalize_whitespace(Project(features=[feature]))
        assert feature.name == "My Feature"
        assert feature.background.name == "bg name"
        assert outline.name == "spaced out"
        assert outline.examples[0].name == "ex name"
        assert outline.steps[0].name == "a step"
        assert outline.steps[0].keyword == "Given"


class TestValidationEdgeCases:
    def test_add_rule_rejects_non_rule(self):
        with pytest.raises(TypeError, match="ValidationRule"):
            Validator().add_rule(object())

    def test_add_rule_accepts_rule(self):
        class MyRule(ValidationRule):
            name = "mine"

            def check(self, project):
                return []

        v = Validator().add_rule(MyRule())
        assert any(r.name == "mine" for r in v.rules)


class TestSerializerEdgeCases:
    def test_headerless_table_no_phantom_header(self):
        table = Table(headers=[], rows=[TableRow(cells=["a", "b"])])
        out = PrettyPrinter()._print_table(table, indent=4)
        assert out == ["    | a | b |"]

    def test_docstring_with_delimiter_line_switches_delimiter(self):
        doc = DocString(content='"""\nsome text', delimiter='"""')
        out = PrettyPrinter()._print_docstring(doc, indent=4)
        assert out[0].strip() == "```"
        assert out[-1].strip() == "```"

    def test_docstring_with_delimiter_content_prints_content_faithfully(self):
        # A docstring whose content contains a literal ``"""`` line cannot be
        # re-parsed by behave either way (behave only supports ``"""``); the
        # printer emits the other spec-compliant delimiter so the content is
        # preserved in valid Gherkin for the broader ecosystem.
        text = 'Feature: F\n  Scenario: S\n    Given x\n      """\n      """\n'
        feature = BehaveParserAdapter().adapt_feature(parse_feature(text))
        feature.scenarios[0].steps[0].doc_string.content = '"""\ninner'
        printed = PrettyPrinter().print_feature(feature)
        lines = printed.splitlines()
        assert "```" in printed
        assert '      """' in lines
        assert "      inner" in lines

    def test_non_english_feature_prints_localized(self):
        feature = BehaveParserAdapter().adapt_feature(parse_feature(ES_FEATURE, language="es"))
        out = PrettyPrinter().print_feature(feature)
        assert out.startswith("# language: es")
        assert "Característica:" in out
        assert "Escenario:" in out or "Ejemplo:" in out

    def test_non_english_roundtrip(self):
        feature = BehaveParserAdapter().adapt_feature(parse_feature(ES_FEATURE, language="es"))
        printed = PrettyPrinter().print_feature(feature)
        reparsed = BehaveParserAdapter().adapt_feature(parse_feature(printed))
        assert reparsed.name == feature.name
        assert reparsed.language == "es"
        assert reparsed.scenarios[0].steps[0].keyword == "Dado"

    def test_to_dict_dispatches_all_types(self, sample_project):
        ser = JsonSerializer()
        feature = sample_project.features[0]
        assert ser.to_dict(sample_project)["type"] == "project"
        assert ser.to_dict(feature)["type"] == "feature"
        assert ser.to_dict(feature.scenarios[0])["type"] == "scenario"
        assert ser.to_dict(Tag("@x"))["type"] == "tag"
        assert ser.to_dict(Location(filename="f", line=1)) == {
            "filename": "f",
            "line": 1,
            "column": 0,
        }
        assert ser.to_dict(Table(headers=["a"]))["type"] == "table"
        with pytest.raises(SerializationError):
            ser.to_dict(object())


class TestStatisticsEdgeCases:
    def test_average_excludes_background_steps(self):
        from behave_model.model import Background

        feature = Feature(
            name="f",
            background=Background(name="", steps=[Step(keyword="Given", name="bg")]),
            scenarios=[
                Scenario(name="a", steps=[Step(keyword="Given", name="s")]),
                Scenario(
                    name="b",
                    steps=[
                        Step(keyword="Given", name="s1"),
                        Step(keyword="When", name="s2"),
                        Step(keyword="Then", name="s3"),
                    ],
                ),
            ],
        )
        stats = Project(features=[feature]).statistics()
        # steps total counts the background, but the average is over
        # scenario-defined steps only: (1 + 3) / 2 = 2.0
        assert stats["steps"] == 5
        assert stats["average_steps_per_scenario"] == 2.0
