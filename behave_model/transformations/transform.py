"""Safe transformations on the domain model.

Each transformation returns a *new* or *mutated* model while preserving
semantic meaning. Transformations never break the structure of the model.
"""

from __future__ import annotations

from behave_model.exceptions import TransformationError
from behave_model.model.feature import Feature
from behave_model.model.project import Project
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step


def rename_tag(project: Project, old_name: str, new_name: str) -> Project:
    """Rename a tag throughout the entire project.

    Args:
        project: The project to transform.
        old_name: The current tag name (including ``@``).
        new_name: The new tag name (including ``@``).

    Returns:
        The same project (mutated in place).

    Raises:
        TransformationError: If old_name and new_name are the same.
    """
    if old_name == new_name:
        raise TransformationError("Old and new tag names are identical")

    for tag in project.global_tags:
        if tag.name == old_name:
            tag.name = new_name

    for feature in project.features:
        for tag in feature.tags:
            if tag.name == old_name:
                tag.name = new_name
        for scenario in feature.scenarios:
            for tag in scenario.tags:
                if tag.name == old_name:
                    tag.name = new_name
            # outline examples tags
            if isinstance(scenario, ScenarioOutline):
                for ex in scenario.examples:
                    for tag in ex.tags:
                        if tag.name == old_name:
                            tag.name = new_name

    return project


def rename_scenario(project: Project, old_name: str, new_name: str) -> Project:
    """Rename a scenario throughout the project.

    Args:
        project: The project to transform.
        old_name: The current scenario name.
        new_name: The new scenario name.

    Returns:
        The same project (mutated in place).

    Raises:
        TransformationError: If old_name and new_name are the same.
    """
    if old_name == new_name:
        raise TransformationError("Old and new scenario names are identical")

    found = False
    for feature in project.features:
        for scenario in feature.scenarios:
            if scenario.name == old_name:
                scenario.name = new_name
                found = True

    if not found:
        raise TransformationError(f"No scenario named '{old_name}' found")

    return project


def sort_tags(project: Project) -> Project:
    """Sort tags alphabetically on every feature and scenario.

    Returns:
        The same project (mutated in place).
    """
    project.global_tags.sort(key=lambda t: t.name)
    for feature in project.features:
        feature.tags.sort(key=lambda t: t.name)
        for scenario in feature.scenarios:
            scenario.tags.sort(key=lambda t: t.name)
            if isinstance(scenario, ScenarioOutline):
                for ex in scenario.examples:
                    ex.tags.sort(key=lambda t: t.name)
    return project


def sort_features(project: Project, *, key: str = "name") -> Project:
    """Sort features by name (default) or filename.

    Returns:
        The same project (mutated in place).
    """
    if key == "name":
        project.features.sort(key=lambda f: f.name)
    elif key == "filename":
        project.features.sort(key=lambda f: f.location.filename)
    else:
        raise TransformationError(f"Unknown sort key: {key}")
    return project


def normalize_whitespace(project: Project) -> Project:
    """Normalize whitespace in step names and scenario/feature names.

    Strips leading/trailing whitespace and collapses multiple spaces
    into single spaces. Preserves semantic meaning.

    Returns:
        The same project (mutated in place).
    """
    for feature in project.features:
        feature.name = " ".join(feature.name.split())
        feature.description = "\n".join(
            " ".join(line.split()) for line in feature.description.splitlines()
        )
        for scenario in feature.scenarios:
            scenario.name = " ".join(scenario.name.split())
            scenario.description = "\n".join(
                " ".join(line.split()) for line in scenario.description.splitlines()
            )
            for step in scenario.steps:
                step.name = " ".join(step.name.split())
                step.keyword = step.keyword.strip()
        if feature.background:
            for step in feature.background.steps:
                step.name = " ".join(step.name.split())
                step.keyword = step.keyword.strip()
    return project


def sort_scenarios(project: Project, *, key: str = "name") -> Project:
    """Sort scenarios within each feature by name.

    Returns:
        The same project (mutated in place).
    """
    for feature in project.features:
        feature.scenarios.sort(key=lambda s: s.name)
    return project


def remove_tag(project: Project, tag_name: str) -> Project:
    """Remove all occurrences of a tag from the project.

    Returns:
        The same project (mutated in place).
    """
    project.global_tags = [t for t in project.global_tags if t.name != tag_name]
    for feature in project.features:
        feature.tags = [t for t in feature.tags if t.name != tag_name]
        for scenario in feature.scenarios:
            scenario.tags = [t for t in scenario.tags if t.name != tag_name]
            if isinstance(scenario, ScenarioOutline):
                for ex in scenario.examples:
                    ex.tags = [t for t in ex.tags if t.name != tag_name]
    return project


def add_tag_to_feature(project: Project, feature_name: str, tag_name: str) -> Project:
    """Add a tag to a specific feature.

    Returns:
        The same project (mutated in place).

    Raises:
        TransformationError: If the feature is not found.
    """
    from behave_model.model.location import Location
    from behave_model.model.tag import Tag

    for feature in project.features:
        if feature.name == feature_name:
            if not feature.has_tag(tag_name):
                feature.tags.append(Tag(name=tag_name, location=Location()))
            return project
    raise TransformationError(f"Feature '{feature_name}' not found")
