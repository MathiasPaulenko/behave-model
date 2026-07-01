"""Loader functions for reading feature files from disk."""

from __future__ import annotations

from pathlib import Path

from behave_model.model.feature import Feature
from behave_model.model.project import Project
from behave_model.parser.adapter import BehaveParserAdapter
from behave_model.parser.parser import parse_feature


def load_feature(path: str | Path, *, language: str | None = None) -> Feature:
    """Load a single ``.feature`` file from disk.

    Args:
        path: Path to the ``.feature`` file.
        language: Optional language code.

    Returns:
        A domain Feature object.

    Raises:
        FileNotFoundError: If the file does not exist.
        ParseError: If the file cannot be parsed.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {path}")

    text = path.read_text(encoding="utf-8")
    behave_feature = parse_feature(text, filename=str(path), language=language)
    adapter = BehaveParserAdapter()
    return adapter.adapt_feature(behave_feature, filename=str(path))


def load_project(path: str | Path, *, language: str | None = None) -> Project:
    """Load all ``.feature`` files from a directory.

    Args:
        path: Path to a directory containing ``.feature`` files (searched
            recursively).
        language: Optional language code applied to all files.

    Returns:
        A domain Project containing all parsed features.

    Raises:
        FileNotFoundError: If the directory does not exist.
        ParseError: If any file cannot be parsed.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    # Collect all .feature files recursively
    feature_files = sorted(path.rglob("*.feature"))

    if not feature_files:
        return Project(
            features=[],
            global_tags=[],
            metadata=Metadata(source_path=str(path)),
        )

    adapter = BehaveParserAdapter()
    features = []
    for fpath in feature_files:
        text = fpath.read_text(encoding="utf-8")
        behave_feature = parse_feature(text, filename=str(fpath), language=language)
        features.append(adapter.adapt_feature(behave_feature, filename=str(fpath)))

    return Project(
        features=features,
        global_tags=[],
        metadata=Metadata(source_path=str(path)),
    )


# Late import to avoid circular dependency
from behave_model.model.metadata import Metadata  # noqa: E402
