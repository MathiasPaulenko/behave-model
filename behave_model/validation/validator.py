"""Validation framework with pluggable rules.

Each rule is a class that implements :meth:`ValidationRule.check`.
The :class:`Validator` runs all registered rules and collects results.
"""

from __future__ import annotations

from dataclasses import dataclass

from behave_model.model.project import Project


@dataclass
class ValidationIssue:
    """A single validation issue.

    Attributes:
        rule: Name of the rule that produced the issue.
        message: Human-readable description.
        severity: ``"error"`` or ``"warning"``.
        location: Optional location string (e.g. ``"file.feature:12"``).
    """

    rule: str
    message: str
    severity: str = "error"
    location: str = ""

    def __str__(self) -> str:
        prefix = f"[{self.severity.upper()}] {self.rule}"
        if self.location:
            prefix += f" ({self.location})"
        return f"{prefix}: {self.message}"


class ValidationRule:
    """Base class for validation rules.

    Override :meth:`check` to implement validation logic.
    """

    name: str = "base_rule"

    def check(self, project: Project) -> list[ValidationIssue]:
        """Run the rule against a project and return issues."""
        raise NotImplementedError


class DuplicateScenarioNamesRule(ValidationRule):
    """Detects scenarios with the same name within a feature (case-insensitive)."""

    name = "duplicate_scenario_names"

    def check(self, project: Project) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for feature in project.features:
            seen: dict[str, int] = {}
            for scenario in feature.all_scenarios():
                key = scenario.name.lower()
                if key in seen:
                    loc = f"{scenario.location.filename}:{scenario.location.line}"
                    issues.append(
                        ValidationIssue(
                            rule=self.name,
                            message=(
                                f"Duplicate scenario name '{scenario.name}' "
                                f"in feature '{feature.name}'"
                            ),
                            severity="error",
                            location=loc,
                        )
                    )
                seen[key] = seen.get(key, 0) + 1
        return issues


class EmptyScenarioRule(ValidationRule):
    """Detects scenarios with no steps."""

    name = "empty_scenario"

    def check(self, project: Project) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for feature in project.features:
            for scenario in feature.all_scenarios():
                if len(scenario.steps) == 0:
                    loc = f"{scenario.location.filename}:{scenario.location.line}"
                    issues.append(
                        ValidationIssue(
                            rule=self.name,
                            message=(
                                f"Scenario '{scenario.name}' has no steps "
                                f"in feature '{feature.name}'"
                            ),
                            severity="warning",
                            location=loc,
                        )
                    )
        return issues


class EmptyFeatureRule(ValidationRule):
    """Detects features with no scenarios."""

    name = "empty_feature"

    def check(self, project: Project) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for feature in project.features:
            if len(feature.all_scenarios()) == 0:
                loc = f"{feature.location.filename}:{feature.location.line}"
                issues.append(
                    ValidationIssue(
                        rule=self.name,
                        message=f"Feature '{feature.name}' has no scenarios",
                        severity="warning",
                        location=loc,
                    )
                )
        return issues


class InvalidTableRule(ValidationRule):
    """Detects tables with inconsistent column counts."""

    name = "invalid_table"

    def check(self, project: Project) -> list[ValidationIssue]:
        from behave_model.model.scenario_outline import ScenarioOutline

        issues: list[ValidationIssue] = []
        for feature in project.features:
            # all_steps() covers feature/rule backgrounds and rule scenarios
            for step in feature.all_steps():
                if step.data_table:
                    self._check_table(step.data_table, step, issues)
            for scenario in feature.all_scenarios():
                if isinstance(scenario, ScenarioOutline):
                    for ex in scenario.examples:
                        self._check_table(ex.table, ex, issues)
        return issues

    def _check_table(self, table, owner, issues: list[ValidationIssue]) -> None:
        expected = len(table.headers)
        for i, row in enumerate(table.rows):
            if len(row.cells) != expected:
                loc = f"{table.location.filename}:{row.location.line}"
                issues.append(
                    ValidationIssue(
                        rule=self.name,
                        message=(
                            f"Row {i} has {len(row.cells)} cells but expected {expected} (headers)"
                        ),
                        severity="error",
                        location=loc,
                    )
                )


class DuplicateFeatureNamesRule(ValidationRule):
    """Detects features with the same name."""

    name = "duplicate_feature_names"

    def check(self, project: Project) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        seen: dict[str, int] = {}
        for feature in project.features:
            key = feature.name.lower()
            if key in seen:
                loc = f"{feature.location.filename}:{feature.location.line}"
                issues.append(
                    ValidationIssue(
                        rule=self.name,
                        message=f"Duplicate feature name '{feature.name}'",
                        severity="error",
                        location=loc,
                    )
                )
            seen[key] = seen.get(key, 0) + 1
        return issues


class Validator:
    """Runs validation rules against a project.

    By default, all built-in rules are registered. Custom rules can be
    added via :meth:`add_rule`.
    """

    def __init__(self) -> None:
        self.rules: list[ValidationRule] = [
            DuplicateScenarioNamesRule(),
            EmptyScenarioRule(),
            EmptyFeatureRule(),
            InvalidTableRule(),
            DuplicateFeatureNamesRule(),
        ]

    def add_rule(self, rule: ValidationRule) -> Validator:
        """Add a custom validation rule."""
        self.rules.append(rule)
        return self

    def remove_rule(self, name: str) -> Validator:
        """Remove all rules with the given ``name`` (class-level ``name`` attribute)."""
        self.rules = [r for r in self.rules if r.name != name]
        return self

    def validate(self, project: Project) -> list[ValidationIssue]:
        """Run all rules and return the collected issues."""
        issues: list[ValidationIssue] = []
        for rule in self.rules:
            issues.extend(rule.check(project))
        return issues

    def validate_strict(self, project: Project) -> list[ValidationIssue]:
        """Run all rules and raise if any errors are found.

        Raises:
            ValidationError: If any error-severity issues are found.
        """
        from behave_model.exceptions import ValidationError

        issues = self.validate(project)
        errors = [i for i in issues if i.severity == "error"]
        if errors:
            messages = "\n".join(str(e) for e in errors)
            raise ValidationError(f"Validation failed with {len(errors)} error(s):\n{messages}")
        return issues
