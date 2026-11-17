"""Loader functions for reading feature files from disk."""

from __future__ import annotations

from pathlib import Path

from behave_model.exceptions import ParseError
from behave_model.model.feature import Feature
from behave_model.model.metadata import Metadata
from behave_model.model.project import Project
from behave_model.parser.adapter import BehaveParserAdapter
from behave_model.parser.parser import parse_feature


def _read_feature_text(path: Path) -> str:
    """Read a feature file as UTF-8 (BOM stripped via ``utf-8-sig``)."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeError as exc:
        raise ParseError(f"Cannot decode feature file {path}: {exc}") from exc


def load_feature(path: str | Path, *, language: str | None = None) -> Feature:
    """Load a single ``.feature`` file from disk.

    Args:
        path: Path to the ``.feature`` file.
        language: Optional language code.

    Returns:
        A domain Feature object.

    Raises:
        FileNotFoundError: If the file does not exist.
        IsADirectoryError: If ``path`` is a directory, not a file.
        OSError: If ``path`` exists but is not a regular file.
        ParseError: If the file cannot be decoded or parsed.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Feature file not found: {path}")
    if path.is_dir():
        raise IsADirectoryError(f"Expected a .feature file, got directory: {path}")
    if not path.is_file():
        raise OSError(f"Not a regular file: {path}")

    text = _read_feature_text(path)
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
        NotADirectoryError: If ``path`` is a file, not a directory.
        ParseError: If any file cannot be decoded or parsed.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Expected a directory, got file: {path}")

    # Collect .feature files recursively; skip directories named *.feature.
    feature_files = sorted(p for p in path.rglob("*.feature") if p.is_file())

    if not feature_files:
        return Project(
            features=[],
            global_tags=[],
            metadata=Metadata(source_path=str(path)),
        )

    adapter = BehaveParserAdapter()
    features = []
    for fpath in feature_files:
        text = _read_feature_text(fpath)
        behave_feature = parse_feature(text, filename=str(fpath), language=language)
        features.append(adapter.adapt_feature(behave_feature, filename=str(fpath)))

    return Project(
        features=features,
        global_tags=[],
        metadata=Metadata(source_path=str(path)),
    )
