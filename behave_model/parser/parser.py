"""Low-level parser functions wrapping Behave's parser."""

from __future__ import annotations

from behave import parser as behave_parser

from behave_model.exceptions import ParseError


def parse_feature(text: str, *, filename: str = "", language: str | None = None):
    """Parse a feature from raw text.

    Args:
        text: The raw feature file content. A leading UTF-8 BOM is stripped.
        filename: Source filename for location information.
        language: Optional language code (e.g. ``en``, ``es``).

    Returns:
        A behave.model.Feature object.

    Raises:
        TypeError: If ``text`` is not a string.
        ParseError: If the text cannot be parsed or contains no feature
            (empty input, comments only, whitespace only).
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    # Behave does not strip a UTF-8 BOM; do it here so callers that read
    # files with plain ``utf-8`` decoding still parse correctly.
    text = text.removeprefix("\ufeff")
    try:
        feature = behave_parser.parse_feature(text, language=language, filename=filename or None)
    except Exception as exc:
        raise ParseError(f"Failed to parse feature {filename or '<text>'}: {exc}") from exc
    if feature is None:
        raise ParseError(f"No feature found in {filename or '<text>'}")
    return feature


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
