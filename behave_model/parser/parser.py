"""Low-level parser functions wrapping Behave's parser."""

from __future__ import annotations

from behave import parser as behave_parser

from behave_model.exceptions import ParseError


def parse_feature(text: str, *, filename: str = "", language: str | None = None):
    """Parse a feature from raw text.

    Args:
        text: The raw feature file content.
        filename: Source filename for location information.
        language: Optional language code (e.g. ``en``, ``es``).

    Returns:
        A behave.model.Feature object.

    Raises:
        ParseError: If the text cannot be parsed.
    """
    try:
        return behave_parser.parse_feature(text, language=language, filename=filename or None)
    except Exception as exc:
        raise ParseError(f"Failed to parse feature: {exc}") from exc


def parse_project(texts: dict[str, str], *, language: str | None = None):
    """Parse multiple feature texts into a list of behave features.

    Args:
        texts: A mapping of filename -> feature file content.
        language: Optional language code.

    Returns:
        A list of behave.model.Feature objects.

    Raises:
        ParseError: If any text cannot be parsed.
    """
    features = []
    for filename, text in texts.items():
        features.append(parse_feature(text, filename=filename, language=language))
    return features
