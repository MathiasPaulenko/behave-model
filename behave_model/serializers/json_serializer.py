"""JSON serializer — converts domain objects to JSON strings."""

from __future__ import annotations

import json

from behave_model.exceptions import SerializationError
from behave_model.model.feature import Feature
from behave_model.model.project import Project
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
        if isinstance(obj, Project):
            return self._dict_serializer.serialize_project(obj)
        if isinstance(obj, Feature):
            return self._dict_serializer.serialize_feature(obj)
        raise SerializationError(f"Unsupported type for JSON serialization: {type(obj)}")
