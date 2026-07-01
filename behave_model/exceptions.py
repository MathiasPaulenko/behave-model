"""Exception hierarchy for behave-model."""

from __future__ import annotations


class BehaveModelError(Exception):
    """Base exception for all behave-model errors."""


class ParseError(BehaveModelError):
    """Raised when a feature file cannot be parsed."""


class ValidationError(BehaveModelError):
    """Raised when a validation rule fails."""

    def __init__(self, message: str, *, rule: str = "", location: str = "") -> None:
        super().__init__(message)
        self.rule = rule
        self.location = location


class TransformationError(BehaveModelError):
    """Raised when a transformation cannot be applied."""


class SerializationError(BehaveModelError):
    """Raised when serialization fails."""
