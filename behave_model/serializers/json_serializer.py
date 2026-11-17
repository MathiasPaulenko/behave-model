"""JSON serializer — converts domain objects to JSON strings."""

from __future__ import annotations

import json

from behave_model.exceptions import SerializationError
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
from behave_model.serializers.dict_serializer import DictSerializer


class JsonSerializer:
    """Serializes domain objects into JSON strings."""

    def __init__(self, *, indent: int | None = 2, ensure_ascii: bool = False) -> None:
        self._dict_serializer = DictSerializer()
        self._indent = indent
        self._ensure_ascii = ensure_ascii

    def serialize_project(self, project: Project) -> str:
        try:
            data = self._dict_serializer.serialize_project(project)
            return json.dumps(data, indent=self._indent, ensure_ascii=self._ensure_ascii)
        except (TypeError, ValueError) as exc:
            raise SerializationError(f"Failed to serialize project to JSON: {exc}") from exc

    def serialize_feature(self, feature: Feature) -> str:
        try:
            data = self._dict_serializer.serialize_feature(feature)
            return json.dumps(data, indent=self._indent, ensure_ascii=self._ensure_ascii)
        except (TypeError, ValueError) as exc:
            raise SerializationError(f"Failed to serialize feature to JSON: {exc}") from exc

    def to_dict(self, obj) -> dict:
        """Convert any domain object to a dict using the dict serializer."""
        ser = self._dict_serializer
        handlers = (
            (Project, ser.serialize_project),
            (Feature, ser.serialize_feature),
            (Rule, ser.serialize_rule),
            (Background, ser.serialize_background),
            (ScenarioOutline, ser.serialize_scenario_outline),
            (Scenario, ser.serialize_scenario),
            (Examples, ser.serialize_examples),
            (Step, ser.serialize_step),
            (Table, ser.serialize_table),
            (DocString, ser.serialize_docstring),
            (Tag, ser.serialize_tag),
            (Comment, ser.serialize_comment),
            (Location, ser.serialize_location),
        )
        for cls, handler in handlers:
            if isinstance(obj, cls):
                return handler(obj)
        raise SerializationError(f"Unsupported type for JSON serialization: {type(obj)}")
