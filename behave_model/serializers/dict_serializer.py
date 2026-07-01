"""Dictionary serializer — converts domain objects to plain dicts."""

from __future__ import annotations

from behave_model.model.background import Background
from behave_model.model.comment import Comment
from behave_model.model.docstring import DocString
from behave_model.model.examples import Examples
from behave_model.model.feature import Feature
from behave_model.model.location import Location
from behave_model.model.project import Project
from behave_model.model.rule import Rule
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step
from behave_model.model.table import Table
from behave_model.model.tag import Tag


class DictSerializer:
    """Serializes domain objects into plain Python dictionaries."""

    def serialize_project(self, project: Project) -> dict:
        return {
            "type": "project",
            "features": [self.serialize_feature(f) for f in project.features],
            "global_tags": [self.serialize_tag(t) for t in project.global_tags],
            "metadata": {
                "source_path": project.metadata.source_path,
                "tool_version": project.metadata.tool_version,
            },
            "statistics": project.statistics(),
        }

    def serialize_feature(self, feature: Feature) -> dict:
        return {
            "type": "feature",
            "name": feature.name,
            "description": feature.description,
            "language": feature.language,
            "tags": [self.serialize_tag(t) for t in feature.tags],
            "background": (
                self.serialize_background(feature.background) if feature.background else None
            ),
            "scenarios": [self._serialize_scenario(s) for s in feature.scenarios],
            "rules": [self.serialize_rule(r) for r in feature.rules],
            "comments": [self.serialize_comment(c) for c in feature.comments],
            "location": self.serialize_location(feature.location),
        }

    def serialize_rule(self, rule: Rule) -> dict:
        return {
            "type": "rule",
            "name": rule.name,
            "description": rule.description,
            "tags": [self.serialize_tag(t) for t in rule.tags],
            "background": (self.serialize_background(rule.background) if rule.background else None),
            "scenarios": [self._serialize_scenario(s) for s in rule.scenarios],
            "comments": [self.serialize_comment(c) for c in rule.comments],
            "location": self.serialize_location(rule.location),
        }

    def serialize_background(self, background: Background) -> dict:
        return {
            "type": "background",
            "name": background.name,
            "steps": [self.serialize_step(s) for s in background.steps],
            "location": self.serialize_location(background.location),
        }

    def _serialize_scenario(self, scenario: Scenario | ScenarioOutline) -> dict:
        if isinstance(scenario, ScenarioOutline):
            return self.serialize_scenario_outline(scenario)
        return self.serialize_scenario(scenario)

    def serialize_scenario(self, scenario: Scenario) -> dict:
        return {
            "type": "scenario",
            "name": scenario.name,
            "description": scenario.description,
            "tags": [self.serialize_tag(t) for t in scenario.tags],
            "steps": [self.serialize_step(s) for s in scenario.steps],
            "comments": [self.serialize_comment(c) for c in scenario.comments],
            "location": self.serialize_location(scenario.location),
        }

    def serialize_scenario_outline(self, outline: ScenarioOutline) -> dict:
        return {
            "type": "scenario_outline",
            "name": outline.name,
            "description": outline.description,
            "tags": [self.serialize_tag(t) for t in outline.tags],
            "steps": [self.serialize_step(s) for s in outline.steps],
            "examples": [self.serialize_examples(e) for e in outline.examples],
            "comments": [self.serialize_comment(c) for c in outline.comments],
            "location": self.serialize_location(outline.location),
        }

    def serialize_examples(self, examples: Examples) -> dict:
        return {
            "type": "examples",
            "name": examples.name,
            "tags": [self.serialize_tag(t) for t in examples.tags],
            "table": self.serialize_table(examples.table),
            "location": self.serialize_location(examples.location),
        }

    def serialize_step(self, step: Step) -> dict:
        return {
            "type": "step",
            "keyword": step.keyword,
            "name": step.name,
            "doc_string": (self.serialize_docstring(step.doc_string) if step.doc_string else None),
            "data_table": (self.serialize_table(step.data_table) if step.data_table else None),
            "comments": [self.serialize_comment(c) for c in step.comments],
            "location": self.serialize_location(step.location),
        }

    def serialize_table(self, table: Table) -> dict:
        return {
            "type": "table",
            "headers": list(table.headers),
            "rows": [list(row.cells) for row in table.rows],
            "location": self.serialize_location(table.location),
        }

    def serialize_docstring(self, docstring: DocString) -> dict:
        return {
            "type": "docstring",
            "content": docstring.content,
            "content_type": docstring.content_type,
            "delimiter": docstring.delimiter,
            "location": self.serialize_location(docstring.location),
        }

    def serialize_tag(self, tag: Tag) -> dict:
        return {
            "type": "tag",
            "name": tag.name,
            "location": self.serialize_location(tag.location),
        }

    def serialize_comment(self, comment: Comment) -> dict:
        return {
            "type": "comment",
            "text": comment.text,
            "location": self.serialize_location(comment.location),
        }

    def serialize_location(self, location: Location) -> dict:
        return {
            "filename": location.filename,
            "line": location.line,
            "column": location.column,
        }
