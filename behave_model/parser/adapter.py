"""Adapter that converts Behave model objects into behave-model domain objects."""

from __future__ import annotations

from behave_model.model.background import Background
from behave_model.model.comment import Comment
from behave_model.model.docstring import DocString
from behave_model.model.examples import Examples
from behave_model.model.feature import Feature
from behave_model.model.location import Location
from behave_model.model.metadata import Metadata
from behave_model.model.project import Project
from behave_model.model.rule import Rule
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step
from behave_model.model.table import Table, TableRow
from behave_model.model.tag import Tag


class BehaveParserAdapter:
    """Converts behave.model objects into behave_model domain objects.

    This adapter is the bridge between Behave's internal model and the
    behave-model domain model. It preserves all structural information
    (tags, steps, tables, docstrings, locations) while wrapping them in
    a clean, extensible API.
    """

    def adapt_feature(self, behave_feature, *, filename: str = "") -> Feature:
        """Convert a behave.model.Feature into a domain Feature."""
        fname = filename or getattr(behave_feature, "filename", "") or ""
        line = getattr(behave_feature, "line", 0) or 0
        location = Location(filename=fname, line=line)

        # -- tags --
        tags = self._adapt_tags(behave_feature.tags, fname)

        # -- description --
        desc = behave_feature.description
        if isinstance(desc, list):
            description = "\n".join(desc)
        elif desc is None:
            description = ""
        else:
            description = str(desc)

        # -- background --
        background = None
        if behave_feature.background:
            background = self._adapt_background(behave_feature.background, fname)

        # -- scenarios (directly under feature) --
        scenarios = []
        for behave_scenario in behave_feature.scenarios:
            scenarios.append(self._adapt_scenario(behave_scenario, fname))

        # -- rules (Gherkin v6) --
        rules = []
        for behave_rule in getattr(behave_feature, "rules", []):
            rules.append(self._adapt_rule(behave_rule, fname))

        # -- language --
        language = getattr(behave_feature, "language", "en") or "en"

        return Feature(
            name=behave_feature.name or "",
            description=description,
            tags=tags,
            background=background,
            scenarios=scenarios,
            rules=rules,
            comments=[],
            location=location,
            language=language,
        )

    def adapt_project(self, behave_features, *, source_path: str = "") -> Project:
        """Convert a list of behave.model.Feature into a domain Project."""
        features = []
        for bf in behave_features:
            features.append(self.adapt_feature(bf))

        return Project(
            features=features,
            global_tags=[],
            metadata=Metadata(source_path=source_path),
        )

    # -- internal helpers ----------------------------------------------------

    def _adapt_tags(self, behave_tags, filename: str) -> list[Tag]:
        tags = []
        for bt in behave_tags:
            line = getattr(bt, "line", 0) or 0
            name = str(bt)
            if not name.startswith("@"):
                name = "@" + name
            tags.append(Tag(name=name, location=Location(filename=filename, line=line)))
        return tags

    def _adapt_background(self, behave_background, filename: str) -> Background:
        line = getattr(behave_background, "line", 0) or 0
        steps = [self._adapt_step(s, filename) for s in behave_background.steps]
        return Background(
            name=behave_background.name or "",
            steps=steps,
            location=Location(filename=filename, line=line),
        )

    def _adapt_scenario(self, behave_scenario, filename: str):
        """Convert a behave scenario (plain or outline) into the domain model."""
        line = getattr(behave_scenario, "line", 0) or 0
        tags = self._adapt_tags(behave_scenario.tags, filename)
        steps = [self._adapt_step(s, filename) for s in behave_scenario.steps]

        # description
        desc = getattr(behave_scenario, "description", None)
        if isinstance(desc, list):
            description = "\n".join(desc)
        elif desc is None:
            description = ""
        else:
            description = str(desc)

        # ScenarioOutline vs Scenario
        scenario_type = type(behave_scenario).__name__

        if scenario_type == "ScenarioOutline":
            examples = []
            for behave_ex in behave_scenario.examples:
                examples.append(self._adapt_examples(behave_ex, filename))
            return ScenarioOutline(
                name=behave_scenario.name or "",
                description=description,
                tags=tags,
                steps=steps,
                examples=examples,
                comments=[],
                location=Location(filename=filename, line=line),
            )

        return Scenario(
            name=behave_scenario.name or "",
            description=description,
            tags=tags,
            steps=steps,
            comments=[],
            location=Location(filename=filename, line=line),
        )

    def _adapt_rule(self, behave_rule, filename: str) -> Rule:
        """Convert a behave.model.Rule into a domain Rule."""
        line = getattr(behave_rule, "line", 0) or 0
        tags = self._adapt_tags(getattr(behave_rule, "tags", []), filename)

        desc = getattr(behave_rule, "description", None)
        if isinstance(desc, list):
            description = "\n".join(desc)
        elif desc is None:
            description = ""
        else:
            description = str(desc)

        background = None
        if getattr(behave_rule, "background", None):
            background = self._adapt_background(behave_rule.background, filename)

        scenarios = []
        for behave_scenario in behave_rule.scenarios:
            scenarios.append(self._adapt_scenario(behave_scenario, filename))

        return Rule(
            name=behave_rule.name or "",
            description=description,
            tags=tags,
            background=background,
            scenarios=scenarios,
            comments=[],
            location=Location(filename=filename, line=line),
        )

    def _adapt_examples(self, behave_examples, filename: str) -> Examples:
        line = getattr(behave_examples, "line", 0) or 0
        tags = self._adapt_tags(getattr(behave_examples, "tags", []), filename)
        table = self._adapt_table(behave_examples.table, filename)
        return Examples(
            name=behave_examples.name or "",
            tags=tags,
            table=table,
            location=Location(filename=filename, line=line),
        )

    def _adapt_step(self, behave_step, filename: str) -> Step:
        line = getattr(behave_step, "line", 0) or 0
        keyword = behave_step.keyword or ""
        name = behave_step.name or ""

        # docstring (Behave stores it in .text)
        doc_string = None
        step_text = getattr(behave_step, "text", None)
        if step_text:
            doc_string = DocString(
                content=step_text,
                content_type="",
                delimiter='"""',
                location=Location(filename=filename, line=line),
            )

        # data table
        data_table = None
        step_table = getattr(behave_step, "table", None)
        if step_table:
            data_table = self._adapt_table(step_table, filename)

        return Step(
            keyword=keyword,
            name=name,
            doc_string=doc_string,
            data_table=data_table,
            comments=[],
            location=Location(filename=filename, line=line),
        )

    def _adapt_table(self, behave_table, filename: str) -> Table:
        headers = list(behave_table.headings)
        rows = []
        for behave_row in behave_table.rows:
            row_line = getattr(behave_row, "line", 0) or 0
            rows.append(
                TableRow(
                    cells=list(behave_row.cells),
                    location=Location(filename=filename, line=row_line),
                )
            )
        return Table(
            headers=headers,
            rows=rows,
            location=Location(filename=filename, line=0),
        )
