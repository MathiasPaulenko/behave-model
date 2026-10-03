# API Reference — Validation

## Validator

Runs all registered validation rules against a project.

```python
from behave_model import Validator

validator = Validator()
issues = validator.validate(project)
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `rules` | `list[ValidationRule]` | Registered validation rules |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `validate(project)` | `list[ValidationIssue]` | Run all rules and collect issues |
| `validate_strict(project)` | `list[ValidationIssue]` | Like `validate`, but raises `ValidationError` on any error-severity issue |
| `add_rule(rule)` | `Validator` | Add a custom validation rule (returns self for chaining) |
| `remove_rule(name)` | `Validator` | Remove a rule by name (returns self for chaining) |

---

## ValidationRule

Base class for custom validation rules.

```python
from behave_model import ValidationRule, ValidationIssue

class MyRule(ValidationRule):
    name = "my_rule"

    def check(self, project):
        issues = []
        # ... check logic ...
        return issues
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Rule name (shown in issues) — snake_case by convention |

Severity is not declared on the rule — it is set per `ValidationIssue`
when creating the issue.

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `check(project)` | `list[ValidationIssue]` | Run the rule and return issues |

---

## ValidationIssue

A single validation finding.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `rule` | `str` | Name of the rule that found the issue |
| `message` | `str` | Human-readable description |
| `severity` | `str` | `"error"` or `"warning"` |
| `location` | `str` | Source location string (e.g. `"file.feature:12"`), or `""` |

---

## Built-in rules

### DuplicateScenarioNamesRule

Scenarios within a feature must have unique names (case-insensitive;
includes scenarios inside Rules).

| Property | Value |
| --- | --- |
| `name` | `"duplicate_scenario_names"` |
| `severity` | `"error"` |

### DuplicateFeatureNamesRule

Features must have unique names.

| Property | Value |
| --- | --- |
| `name` | `"duplicate_feature_names"` |
| `severity` | `"error"` |

### EmptyScenarioRule

Scenarios should have at least one step (includes scenarios inside Rules).

| Property | Value |
| --- | --- |
| `name` | `"empty_scenario"` |
| `severity` | `"warning"` |

### EmptyFeatureRule

Features should have at least one scenario (scenarios inside Rules count).

| Property | Value |
| --- | --- |
| `name` | `"empty_feature"` |
| `severity` | `"warning"` |

### InvalidTableRule

Data tables must have consistent column counts across all rows
(includes tables in rules, backgrounds, and Examples).

| Property | Value |
| --- | --- |
| `name` | `"invalid_table"` |
| `severity` | `"error"` |
