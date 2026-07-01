"""Utility functions for behave-model."""

from __future__ import annotations

from behave_model.model.project import Project


def count_by_type(project: Project) -> dict[str, int]:
    """Count nodes by type name using the project's walk() method."""
    counts: dict[str, int] = {}
    for node in project.walk():
        type_name = type(node).__name__
        counts[type_name] = counts.get(type_name, 0) + 1
    return counts


def flatten_steps(project: Project) -> list[str]:
    """Return a list of 'keyword name' strings for every step in the project."""
    return [step.full_text for step in project.all_steps()]


def unique_tag_names(project: Project) -> list[str]:
    """Return sorted unique tag names across the project."""
    return sorted({t.name for t in project.all_tags()})


def feature_filenames(project: Project) -> list[str]:
    """Return all feature filenames in the project."""
    return [f.location.filename for f in project.features]
