"""Tests for exceptions."""

from __future__ import annotations

import pytest

from behave_model.exceptions import (
    BehaveModelError,
    ParseError,
    SerializationError,
    TransformationError,
    ValidationError,
)


class TestExceptions:
    def test_hierarchy(self):
        assert issubclass(ParseError, BehaveModelError)
        assert issubclass(ValidationError, BehaveModelError)
        assert issubclass(TransformationError, BehaveModelError)
        assert issubclass(SerializationError, BehaveModelError)

    def test_validation_error_with_details(self):
        err = ValidationError("test message", rule="my_rule", location="file:10")
        assert err.rule == "my_rule"
        assert err.location == "file:10"
        assert "test message" in str(err)

    def test_parse_error_message(self):
        err = ParseError("bad syntax")
        assert "bad syntax" in str(err)
