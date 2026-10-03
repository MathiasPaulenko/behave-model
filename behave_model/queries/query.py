"""High-level query API for searching and filtering domain models.

The query functions are available as methods on :class:`Project` and
:class:`Feature` via the :class:`QueryMixin`, but can also be used
standalone through the functions in this module.
"""

from __future__ import annotations

from collections.abc import Iterator

from behave_model.model.feature import Feature, ScenarioLike
from behave_model.model.project import Project
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step
from behave_model.model.tag import Tag

# -- standalone functions ----------------------------------------------------


def find_feature(project: Project, name: str) -> Feature | None:
    """Find a feature by exact name (case-insensitive)."""
    lower = name.lower()
    for f in project.features:
        if f.name.lower() == lower:
            return f
    return None


def find_tag(project: Project, name: str) -> Tag | None:
    """Find a tag by exact name across the entire project."""
    for tag in project.all_tags():
        if tag.name == name:
            return tag
    return None


def _iter_scenario_contexts(
    project: Project,
) -> Iterator[tuple[Feature, object, ScenarioLike]]:
    """Yield ``(feature, rule_or_None, scenario)`` for every scenario.

    Needed because tag matching must account for inherited tags (feature
    and rule tags apply to their scenarios, per Gherkin semantics).
    """
    for feature in project.features:
        for s in feature.scenarios:
            yield feature, None, s
        for rule in feature.rules:
            for s in rule.scenarios:
                yield feature, rule, s


def _effective_tag_names(feature: Feature, rule, scenario: ScenarioLike) -> set[str]:
    """Tags that effectively apply to a scenario (inherited + own + examples)."""
    names = set(feature.tag_names)
    if rule is not None:
        names.update(rule.tag_names)
    names.update(scenario.tag_names)
    if isinstance(scenario, ScenarioOutline):
        for ex in scenario.examples:
            names.update(t.name for t in ex.tags)
    return names


def find_scenarios(
    project: Project,
    *,
    tag: str | None = None,
    name: str | None = None,
    name_contains: str | None = None,
) -> list[ScenarioLike]:
    """Find scenarios by tag, exact name, or name substring.

    The ``tag`` filter matches inherited tags as well: a scenario is
    returned if the tag is applied to the scenario itself, one of its
    ``Examples`` blocks, its enclosing rule, or its feature — matching
    how Behave interprets tag inheritance. ``name`` and ``name_contains``
    are case-insensitive.
    """
    results: list[ScenarioLike] = []
    name_lower = name.lower() if name is not None else None
    contains_lower = name_contains.lower() if name_contains is not None else None
    for feature, rule, s in _iter_scenario_contexts(project):
        if tag is not None and tag not in _effective_tag_names(feature, rule, s):
            continue
        if name_lower is not None and s.name.lower() != name_lower:
            continue
        if contains_lower is not None and contains_lower not in s.name.lower():
            continue
        results.append(s)
    return results


def find_steps(
    project: Project,
    *,
    keyword: str | None = None,
    text_contains: str | None = None,
) -> list[Step]:
    """Find steps by keyword and/or text substring."""
    results: list[Step] = []
    for step in project.all_steps():
        if keyword is not None and step.keyword.lower() != keyword.lower():
            continue
        if text_contains is not None and text_contains.lower() not in step.name.lower():
            continue
        results.append(step)
    return results


def find_features_with_tag(project: Project, tag: str) -> list[Feature]:
    """Return all features that have a given tag."""
    return [f for f in project.features if f.has_tag(tag)]


def find_scenarios_with_tag(project: Project, tag: str) -> list[ScenarioLike]:
    """Return all scenarios (including outlines) that have a given tag.

    Inherited tags count: scenarios whose feature, enclosing rule, or
    ``Examples`` block carries the tag are included.
    """
    return [
        s
        for feature, rule, s in _iter_scenario_contexts(project)
        if tag in _effective_tag_names(feature, rule, s)
    ]


def find_outlines(project: Project) -> list[ScenarioOutline]:
    """Return all scenario outlines in the project."""
    return [s for s in project.all_scenarios() if isinstance(s, ScenarioOutline)]


def find_plain_scenarios(project: Project) -> list[Scenario]:
    """Return all plain (non-outline) scenarios in the project."""
    return [s for s in project.all_scenarios() if isinstance(s, Scenario)]


# -- mixin -------------------------------------------------------------------


class QueryMixin:
    """Mixin that adds query methods to Project.

    This is applied to :class:`behave_model.model.project.Project` at
    import time so that users can call ``project.find_feature("Login")``
    directly.
    """

    def find_feature(self: Project, name: str) -> Feature | None:
        """Find a feature by exact name (case-insensitive)."""
        return find_feature(self, name)

    def find_tag(self: Project, name: str) -> Tag | None:
        """Find a tag by exact name across the entire project."""
        return find_tag(self, name)

    def find_scenarios(
        self: Project,
        *,
        tag: str | None = None,
        name: str | None = None,
        name_contains: str | None = None,
    ) -> list[ScenarioLike]:
        """Find scenarios by tag, exact name, or name substring.

        Tag matching includes tags inherited from the feature, the
        enclosing rule, and ``Examples`` blocks.
        """
        return find_scenarios(self, tag=tag, name=name, name_contains=name_contains)

    def find_steps(
        self: Project,
        *,
        keyword: str | None = None,
        text_contains: str | None = None,
    ) -> list[Step]:
        """Find steps by keyword and/or text substring."""
        return find_steps(self, keyword=keyword, text_contains=text_contains)

    def find_features_with_tag(self: Project, tag: str) -> list[Feature]:
        """Return all features that have a given tag."""
        return find_features_with_tag(self, tag)

    def find_scenarios_with_tag(self: Project, tag: str) -> list[ScenarioLike]:
        """Return all scenarios (including outlines) with a given tag, including inherited tags."""
        return find_scenarios_with_tag(self, tag)

    def find_outlines(self: Project) -> list[ScenarioOutline]:
        """Return all scenario outlines in the project."""
        return find_outlines(self)

    def find_plain_scenarios(self: Project) -> list[Scenario]:
        """Return all plain (non-outline) scenarios in the project."""
        return find_plain_scenarios(self)


# Apply the mixin to Project at import time
for _method_name in dir(QueryMixin):
    if not _method_name.startswith("_"):
        _method = getattr(QueryMixin, _method_name)
        if callable(_method) and not hasattr(Project, _method_name):
            setattr(Project, _method_name, _method)
