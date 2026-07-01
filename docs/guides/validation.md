# Validation Guide

The validation framework provides pluggable rules to check the integrity of your feature files.

## Built-in rules

| Rule | Severity | Description |
| --- | --- | --- |
| `DuplicateScenarioNamesRule` | `error` | Scenarios within a feature must have unique names |
| `DuplicateFeatureNamesRule` | `error` | Features must have unique names |
| `EmptyScenarioRule` | `warning` | Scenarios should have at least one step |
| `EmptyFeatureRule` | `warning` | Features should have at least one scenario |
| `InvalidTableRule` | `error` | Data tables must have consistent column counts |

## Running validation

```python
from behave_model import load_project, Validator

project = load_project("features/")
validator = Validator()
issues = validator.validate(project)

if issues:
    for issue in issues:
        print(f"[{issue.severity}] {issue.rule_name}: {issue.message}")
        if issue.location:
            print(f"  at {issue.location}")
else:
    print("No issues found!")
```

Output:

```text
[error] DuplicateScenarioNames: Scenario 'Login' appears 2 times in feature 'Auth'
  at <features/auth.feature:15>
[warning] EmptyScenario: Scenario 'Placeholder' has no steps
  at <features/auth.feature:25>
```

## ValidationIssue

Each issue contains:

| Field | Type | Description |
| --- | --- | --- |
| `rule_name` | `str` | Name of the rule that found the issue |
| `severity` | `str` | `"error"` or `"warning"` |
| `message` | `str` | Human-readable description |
| `location` | `Location \| None` | Source location of the problem |

## Custom validation rules

Create custom rules by subclassing `ValidationRule`:

```python
from behave_model import ValidationRule, ValidationIssue, Validator

class NoGivenInThenRule(ValidationRule):
    """Ensure no Then step contains 'Given' in its text."""

    name = "NoGivenInThen"
    severity = "error"

    def check(self, project):
        issues = []
        for step in project.all_steps():
            if step.keyword == "Then" and "Given" in step.name:
                issues.append(ValidationIssue(
                    rule_name=self.name,
                    severity=self.severity,
                    message=f"Then step contains 'Given': {step.name}",
                    location=step.location,
                ))
        return issues

# Use it
validator = Validator()
validator.add_rule(NoGivenInThenRule())
issues = validator.validate(project)
```

### Custom rule with parameters

```python
class MaxStepsPerScenarioRule(ValidationRule):
    """Ensure scenarios don't exceed a maximum number of steps."""

    name = "MaxStepsPerScenario"
    severity = "warning"

    def __init__(self, max_steps=10):
        self.max_steps = max_steps

    def check(self, project):
        issues = []
        for scenario in project.all_scenarios():
            if len(scenario.steps) > self.max_steps:
                issues.append(ValidationIssue(
                    rule_name=self.name,
                    severity=self.severity,
                    message=(
                        f"Scenario '{scenario.name}' has {len(scenario.steps)} "
                        f"steps (max {self.max_steps})"
                    ),
                    location=scenario.location,
                ))
        return issues

# Allow max 8 steps per scenario
validator = Validator()
validator.add_rule(MaxStepsPerScenarioRule(max_steps=8))
```

### Rule that checks tags

```python
class RequiredTagRule(ValidationRule):
    """Ensure all features have a @regression tag."""

    name = "RequiredFeatureTag"
    severity = "warning"

    def check(self, project):
        issues = []
        for feature in project.features:
            if "@regression" not in feature.tag_names:
                issues.append(ValidationIssue(
                    rule_name=self.name,
                    severity=self.severity,
                    message=f"Feature '{feature.name}' missing @regression tag",
                    location=feature.location,
                ))
        return issues
```

## Selective validation

```python
from behave_model import (
    Validator,
    DuplicateScenarioNamesRule,
    EmptyScenarioRule,
)

# Only run specific rules
validator = Validator()
validator.rules = [
    DuplicateScenarioNamesRule(),
    EmptyScenarioRule(),
]
issues = validator.validate(project)
```

## CI/CD integration

```python
from behave_model import load_project, Validator

project = load_project("features/")
issues = Validator().validate(project)

errors = [i for i in issues if i.severity == "error"]
if errors:
    print(f"\n{len(errors)} validation errors found:")
    for issue in errors:
        print(f"  [{issue.rule_name}] {issue.message}")
    exit(1)
```

## Next steps

- [Transformations](transformations.md) — Fix issues found by validation
- [API Reference — Validation](../api/validation.md) — Complete API
