"""Tests for the validation framework."""

from __future__ import annotations

import pytest

from behave_model.exceptions import ValidationError
from behave_model.model import (
    Feature,
    Project,
    Scenario,
    Table,
    TableRow,
)
from behave_model.validation import (
    DuplicateFeatureNamesRule,
    DuplicateScenarioNamesRule,
    EmptyFeatureRule,
    EmptyScenarioRule,
    InvalidTableRule,
    ValidationIssue,
    ValidationRule,
    Validator,
)


class TestValidationRules:
    def test_duplicate_scenario_names(self):
        rule = DuplicateScenarioNamesRule()
        project = Project(
            features=[
                Feature(
                    name="F1",
                    scenarios=[
                        Scenario(name="Dup"),
                        Scenario(name="Dup"),
                    ],
                )
            ]
        )
        issues = rule.check(project)
        assert len(issues) == 1
        assert issues[0].rule == "duplicate_scenario_names"

    def test_empty_scenario(self):
        rule = EmptyScenarioRule()
        project = Project(
            features=[
                Feature(
                    name="F1",
                    scenarios=[Scenario(name="Empty")],
                )
            ]
        )
        issues = rule.check(project)
        assert len(issues) == 1
        assert issues[0].severity == "warning"

    def test_empty_feature(self):
        rule = EmptyFeatureRule()
        project = Project(features=[Feature(name="Empty")])
        issues = rule.check(project)
        assert len(issues) == 1

    def test_invalid_table(self):
        rule = InvalidTableRule()
        from behave_model.model.scenario_outline import Examples, ScenarioOutline

        project = Project(
            features=[
                Feature(
                    name="F1",
                    scenarios=[
                        ScenarioOutline(
                            name="SO",
                            examples=[
                                Examples(
                                    table=Table(
                                        headers=["a", "b"],
                                        rows=[TableRow(cells=["1"])],  # wrong count
                                    ),
                                )
                            ],
                        )
                    ],
                )
            ]
        )
        issues = rule.check(project)
        assert len(issues) == 1
        assert issues[0].severity == "error"

    def test_duplicate_feature_names(self):
        rule = DuplicateFeatureNamesRule()
        project = Project(
            features=[
                Feature(name="Dup"),
                Feature(name="Dup"),
            ]
        )
        issues = rule.check(project)
        assert len(issues) == 1


class TestValidator:
    def test_validate_clean_project(self, sample_project):
        validator = Validator()
        issues = validator.validate(sample_project)
        # Sample project should have no errors (may have warnings)
        errors = [i for i in issues if i.severity == "error"]
        assert len(errors) == 0

    def test_validate_with_errors(self):
        validator = Validator()
        project = Project(
            features=[
                Feature(
                    name="F1",
                    scenarios=[
                        Scenario(name="Dup"),
                        Scenario(name="Dup"),
                    ],
                )
            ]
        )
        issues = validator.validate(project)
        assert len(issues) >= 1

    def test_validate_strict_raises(self):
        validator = Validator()
        project = Project(
            features=[
                Feature(
                    name="F1",
                    scenarios=[
                        Scenario(name="Dup"),
                        Scenario(name="Dup"),
                    ],
                )
            ]
        )
        with pytest.raises(ValidationError):
            validator.validate_strict(project)

    def test_validate_strict_no_errors(self, sample_project):
        validator = Validator()
        # Should not raise
        issues = validator.validate_strict(sample_project)
        # May have warnings but no errors
        assert all(i.severity != "error" for i in issues)

    def test_add_custom_rule(self):
        class CustomRule(ValidationRule):
            name = "custom_rule"

            def check(self, project):
                return [
                    ValidationIssue(
                        rule=self.name,
                        message="Custom issue",
                        severity="warning",
                    )
                ]

        validator = Validator()
        validator.add_rule(CustomRule())
        issues = validator.validate(Project())
        custom = [i for i in issues if i.rule == "custom_rule"]
        assert len(custom) == 1

    def test_validation_issue_str(self):
        issue = ValidationIssue(
            rule="test_rule",
            message="Something wrong",
            severity="error",
            location="file.feature:10",
        )
        s = str(issue)
        assert "[ERROR]" in s
        assert "test_rule" in s
        assert "Something wrong" in s
        assert "file.feature:10" in s
