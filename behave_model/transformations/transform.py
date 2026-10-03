"""Safe transformations on the domain model.

Each transformation returns a *new* or *mutated* model while preserving
semantic meaning. Transformations never break the structure of the model.
"""

from __future__ import annotations

from collections.abc import Iterator

from behave_model.exceptions import TransformationError
from behave_model.model.project import Project
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.tag import Tag


def _tag_lists(project: Project) -> Iterator[list[Tag]]:
    """Yield every tag list in the project (global, feature, rule, scenario, examples)."""
    yield project.global_tags
    for feature in project.features:
        yield feature.tags
        for rule in feature.rules:
            yield rule.tags
        for scenario in feature.all_scenarios():
            yield scenario.tags
            if isinstance(scenario, ScenarioOutline):
                for ex in scenario.examples:
                    yield ex.tags


def rename_tag(project: Project, old_name: str, new_name: str) -> Project:
    """Rename a tag throughout the entire project (including inside Rules).

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

    for tags in _tag_lists(project):
        for tag in tags:
            if tag.name == old_name:
                tag.name = new_name

    return project


def rename_scenario(project: Project, old_name: str, new_name: str) -> Project:
    """Rename a scenario throughout the project (case-insensitive match).

    Scenarios inside Gherkin v6 Rules are renamed as well.

    Args:
        project: The project to transform.
        old_name: The current scenario name.
        new_name: The new scenario name.

    Returns:
        The same project (mutated in place).

    Raises:
        TransformationError: If old_name and new_name are the same or no
            scenario with ``old_name`` exists.
    """
    if old_name == new_name:
        raise TransformationError("Old and new scenario names are identical")

    target = old_name.lower()
    found = False
    for feature in project.features:
        for scenario in feature.all_scenarios():
            if scenario.name.lower() == target:
                scenario.name = new_name
                found = True

    if not found:
        raise TransformationError(f"No scenario named '{old_name}' found")

    return project


def sort_tags(project: Project) -> Project:
    """Sort tags alphabetically on every element (features, rules, scenarios, examples).

    Returns:
        The same project (mutated in place).
    """
    for tags in _tag_lists(project):
        tags.sort(key=lambda t: t.name)
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
    """Normalize whitespace in names, descriptions and step text.

    Strips leading/trailing whitespace and collapses multiple spaces
    into single spaces. Preserves semantic meaning. Covers scenarios
    and backgrounds inside Gherkin v6 Rules as well.

    Returns:
        The same project (mutated in place).
    """

    def collapse(text: str) -> str:
        return " ".join(text.split())

    def collapse_lines(text: str) -> str:
        return "\n".join(collapse(line) for line in text.splitlines())

    def normalize_steps(steps) -> None:
        for step in steps:
            step.name = collapse(step.name)
            step.keyword = step.keyword.strip()

    for feature in project.features:
        feature.name = collapse(feature.name)
        feature.description = collapse_lines(feature.description)
        if feature.background:
            normalize_steps(feature.background.steps)
        for rule in feature.rules:
            rule.name = collapse(rule.name)
            rule.description = collapse_lines(rule.description)
            if rule.background:
                normalize_steps(rule.background.steps)
        for scenario in feature.all_scenarios():
            scenario.name = collapse(scenario.name)
            scenario.description = collapse_lines(scenario.description)
            normalize_steps(scenario.steps)
    return project


def sort_scenarios(project: Project, *, key: str = "name") -> Project:
    """Sort scenarios within each feature and each rule.

    Args:
        project: The project to transform.
        key: ``"name"`` (default) sorts alphabetically; ``"line"`` sorts by
            source line number, restoring the original document order.

    Returns:
        The same project (mutated in place).
    """
    if key == "name":
        key_func = lambda s: s.name  # noqa: E731
    elif key == "line":
        key_func = lambda s: s.location.line  # noqa: E731
    else:
        raise TransformationError(f"Unknown sort key: {key}")
    for feature in project.features:
        feature.scenarios.sort(key=key_func)
        for rule in feature.rules:
            rule.scenarios.sort(key=key_func)
    return project


def remove_tag(project: Project, tag_name: str) -> Project:
    """Remove all occurrences of a tag from the project (including inside Rules).

    Returns:
        The same project (mutated in place).
    """
    for tags in _tag_lists(project):
        tags[:] = [t for t in tags if t.name != tag_name]
    return project


def add_tag_to_feature(project: Project, feature_name: str, tag_name: str) -> Project:
    """Add a tag to a specific feature (case-insensitive name match).

    Returns:
        The same project (mutated in place).

    Raises:
        TransformationError: If the feature is not found.
    """
    from behave_model.model.location import Location

    target = feature_name.lower()
    for feature in project.features:
        if feature.name.lower() == target:
            if not feature.has_tag(tag_name):
                feature.tags.append(Tag(name=tag_name, location=Location()))
            return project
    raise TransformationError(f"Feature '{feature_name}' not found")
