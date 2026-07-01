"""High-level query API for searching and filtering domain models.

The query functions are available as methods on :class:`Project` and
:class:`Feature` via the :class:`QueryMixin`, but can also be used
standalone through the functions in this module.
"""

from __future__ import annotations

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


def find_scenarios(
    project: Project,
    *,
    tag: str | None = None,
    name: str | None = None,
    name_contains: str | None = None,
) -> list[ScenarioLike]:
    """Find scenarios by tag, exact name, or name substring."""
    results: list[ScenarioLike] = []
    for s in project.all_scenarios():
        if tag is not None and not s.has_tag(tag):
            continue
        if name is not None and s.name != name:
            continue
        if name_contains is not None and name_contains.lower() not in s.name.lower():
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
    """Return all scenarios (including outlines) that have a given tag."""
    return [s for s in project.all_scenarios() if s.has_tag(tag)]


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
        """Find scenarios by tag, exact name, or name substring."""
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
        """Return all scenarios (including outlines) that have a given tag."""
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
