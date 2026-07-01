"""Unit tests for domain model classes."""

from __future__ import annotations

from behave_model.model import (
    Background,
    Comment,
    DocString,
    Examples,
    Feature,
    Location,
    Metadata,
    Project,
    Scenario,
    ScenarioOutline,
    Step,
    Table,
    TableRow,
    Tag,
)


class TestLocation:
    def test_default_values(self):
        loc = Location()
        assert loc.filename == ""
        assert loc.line == 0
        assert loc.column == 0

    def test_str_with_filename_and_line(self):
        loc = Location(filename="test.feature", line=10)
        assert "test.feature" in str(loc)
        assert "line 10" in str(loc)

    def test_str_unknown(self):
        loc = Location()
        assert str(loc) == "<unknown>"

    def test_frozen(self):
        loc = Location(filename="a", line=1)
        try:
            loc.line = 2
            assert False, "Should have raised"
        except AttributeError:
            pass


class TestTag:
    def test_basic(self):
        tag = Tag(name="@smoke")
        assert tag.name == "@smoke"
        assert str(tag) == "@smoke"

    def test_equality_by_name(self):
        t1 = Tag(name="@smoke", location=Location(line=1))
        t2 = Tag(name="@smoke", location=Location(line=5))
        assert t1 == t2

    def test_hash_by_name(self):
        t1 = Tag(name="@smoke")
        t2 = Tag(name="@smoke")
        assert hash(t1) == hash(t2)

    def test_inequality(self):
        assert Tag(name="@smoke") != Tag(name="@api")


class TestComment:
    def test_basic(self):
        c = Comment(text="# This is a comment")
        assert c.text == "# This is a comment"
        assert str(c) == "# This is a comment"


class TestDocString:
    def test_basic(self):
        ds = DocString(content='{"key": "value"}', content_type="json")
        assert ds.content == '{"key": "value"}'
        assert ds.content_type == "json"

    def test_lines(self):
        ds = DocString(content="line1\nline2\nline3")
        assert ds.lines == ["line1", "line2", "line3"]


class TestTable:
    def test_empty(self):
        t = Table()
        assert len(t) == 0
        assert t.num_rows == 0
        assert t.num_columns == 0

    def test_with_data(self):
        t = Table(
            headers=["name", "age"],
            rows=[TableRow(cells=["Alice", "30"]), TableRow(cells=["Bob", "25"])],
        )
        assert len(t) == 2
        assert t.num_rows == 2
        assert t.num_columns == 2
        assert t[0].cells == ["Alice", "30"]

    def test_iter_dicts(self):
        t = Table(
            headers=["name", "age"],
            rows=[TableRow(cells=["Alice", "30"])],
        )
        dicts = list(t.iter_dicts())
        assert dicts == [{"name": "Alice", "age": "30"}]

    def test_column_widths(self):
        t = Table(
            headers=["name", "age"],
            rows=[TableRow(cells=["Alice", "30"]), TableRow(cells="Bob")],
        )
        widths = t.column_widths()
        assert widths[0] == 5  # "Alice" is longest
        assert widths[1] == 3  # "age" header

    def test_row_as_dict_without_headers(self):
        row = TableRow(cells=["a", "b"])
        d = row.as_dict()
        assert d == {"col0": "a", "col1": "b"}


class TestStep:
    def test_basic(self):
        step = Step(keyword="Given", name="the user is logged in")
        assert step.keyword == "Given"
        assert step.name == "the user is logged in"
        assert step.text == "the user is logged in"
        assert step.full_text == "Given the user is logged in"

    def test_text_setter(self):
        step = Step(keyword="Given", name="old")
        step.text = "new"
        assert step.name == "new"

    def test_str(self):
        step = Step(keyword="Then", name="the test passes")
        assert str(step) == "Then the test passes"

    def test_with_docstring(self):
        ds = DocString(content='{"key": "val"}')
        step = Step(keyword="Given", name="a payload", doc_string=ds)
        assert step.doc_string is not None
        assert step.doc_string.content == '{"key": "val"}'

    def test_with_table(self):
        table = Table(headers=["a"], rows=[TableRow(cells=["1"])])
        step = Step(keyword="Given", name="data", data_table=table)
        assert step.data_table is not None
        assert len(step.data_table) == 1


class TestBackground:
    def test_basic(self):
        bg = Background(
            name="",
            steps=[Step(keyword="Given", name="a connection")],
        )
        assert len(bg) == 1
        assert bg.steps[0].name == "a connection"

    def test_iter(self):
        steps = [Step(keyword="Given", name="a"), Step(keyword="And", name="b")]
        bg = Background(steps=steps)
        assert list(bg) == steps


class TestScenario:
    def test_basic(self):
        s = Scenario(
            name="Test scenario",
            tags=[Tag(name="@smoke")],
            steps=[Step(keyword="Given", name="a step")],
        )
        assert s.name == "Test scenario"
        assert len(s) == 1
        assert s.has_tag("@smoke")
        assert not s.has_tag("@api")
        assert s.tag_names == ["@smoke"]

    def test_iter(self):
        steps = [Step(keyword="Given", name="a"), Step(keyword="Then", name="b")]
        s = Scenario(name="Test", steps=steps)
        assert list(s) == steps


class TestScenarioOutline:
    def test_basic(self):
        so = ScenarioOutline(
            name="Outline test",
            steps=[Step(keyword="Given", name="a <value>")],
            examples=[
                Examples(
                    name="",
                    table=Table(
                        headers=["value"],
                        rows=[TableRow(cells=["1"]), TableRow(cells=["2"])],
                    ),
                )
            ],
        )
        assert so.name == "Outline test"
        assert len(so) == 1
        assert len(so.examples) == 1

    def test_expand(self):
        so = ScenarioOutline(
            name="Outline",
            steps=[Step(keyword="Given", name="a <value>")],
            examples=[
                Examples(
                    table=Table(
                        headers=["value", "result"],
                        rows=[
                            TableRow(cells=["1", "ok"]),
                            TableRow(cells=["2", "ok"]),
                        ],
                    ),
                )
            ],
        )
        expanded = so.expand()
        assert len(expanded) == 2
        assert expanded[0] == {"value": "1", "result": "ok"}
        assert expanded[1] == {"value": "2", "result": "ok"}


class TestFeature:
    def test_basic(self):
        f = Feature(
            name="Login",
            tags=[Tag(name="@smoke")],
            scenarios=[Scenario(name="Successful login")],
        )
        assert f.name == "Login"
        assert len(f) == 1
        assert f.has_tag("@smoke")
        assert f.tag_names == ["@smoke"]

    def test_outlines_and_plain(self):
        f = Feature(
            name="Test",
            scenarios=[
                Scenario(name="Plain"),
                ScenarioOutline(name="Outline"),
            ],
        )
        assert len(f.plain_scenarios()) == 1
        assert len(f.outlines()) == 1
        assert len(f.all_scenarios()) == 2

    def test_all_tags(self):
        f = Feature(
            name="Test",
            tags=[Tag(name="@feature")],
            scenarios=[
                Scenario(name="S1", tags=[Tag(name="@scenario")]),
            ],
        )
        all_tags = f.all_tags()
        assert len(all_tags) == 2

    def test_all_steps_with_background(self):
        f = Feature(
            name="Test",
            background=Background(steps=[Step(keyword="Given", name="bg")]),
            scenarios=[
                Scenario(name="S1", steps=[Step(keyword="When", name="action")]),
            ],
        )
        steps = f.all_steps()
        assert len(steps) == 2


class TestProject:
    def test_empty(self):
        p = Project()
        assert len(p) == 0
        assert p.statistics()["features"] == 0

    def test_statistics(self):
        p = Project(
            features=[
                Feature(
                    name="F1",
                    scenarios=[
                        Scenario(
                            name="S1",
                            steps=[
                                Step(keyword="Given", name="a"),
                                Step(keyword="Then", name="b"),
                            ],
                        ),
                    ],
                ),
            ],
        )
        stats = p.statistics()
        assert stats["features"] == 1
        assert stats["scenarios"] == 1
        assert stats["steps"] == 2
        assert stats["average_steps_per_scenario"] == 2.0

    def test_iter_and_getitem(self):
        f1 = Feature(name="F1")
        f2 = Feature(name="F2")
        p = Project(features=[f1, f2])
        assert list(p) == [f1, f2]
        assert p[0] == f1
        assert p[1] == f2


class TestMetadata:
    def test_default(self):
        m = Metadata()
        assert m.source_path == ""
        assert m.tool_version == "0.1.0"
        assert m.extra == {}
