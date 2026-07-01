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
| `add_rule(rule)` | `None` | Add a custom validation rule |

---

## ValidationRule

Base class for custom validation rules.

```python
from behave_model import ValidationRule, ValidationIssue

class MyRule(ValidationRule):
    name = "MyRule"
    severity = "warning"

    def check(self, project):
        issues = []
        # ... check logic ...
        return issues
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Rule name (shown in issues) |
| `severity` | `str` | `"error"` or `"warning"` |

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
| `rule_name` | `str` | Name of the rule that found the issue |
| `severity` | `str` | `"error"` or `"warning"` |
| `message` | `str` | Human-readable description |
| `location` | `Location \| None` | Source location of the problem |

---

## Built-in rules

### DuplicateScenarioNamesRule

Scenarios within a feature must have unique names.

| Property | Value |
| --- | --- |
| `name` | `"DuplicateScenarioNames"` |
| `severity` | `"error"` |

### DuplicateFeatureNamesRule

Features must have unique names.

| Property | Value |
| --- | --- |
| `name` | `"DuplicateFeatureNames"` |
| `severity` | `"error"` |

### EmptyScenarioRule

Scenarios should have at least one step.

| Property | Value |
| --- | --- |
| `name` | `"EmptyScenario"` |
| `severity` | `"warning"` |

### EmptyFeatureRule

Features should have at least one scenario.

| Property | Value |
| --- | --- |
| `name` | `"EmptyFeature"` |
| `severity` | `"warning"` |

### InvalidTableRule

Data tables must have consistent column counts across all rows.

| Property | Value |
| --- | --- |
| `name` | `"InvalidTable"` |
| `severity` | `"error"` |
