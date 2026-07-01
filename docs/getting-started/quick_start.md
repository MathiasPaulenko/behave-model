# Quick Start

## 1. Install

```bash
pip install behave-model
```

## 2. Load a project

```python
from behave_model import load_project

project = load_project("features/")
```

`load_project` recursively finds all `.feature` files in the given directory and parses them into the domain model.

## 3. Explore the model

```python
# Iterate features
for feature in project.features:
    print(f"Feature: {feature.name}")
    print(f"  Tags: {', '.join(feature.tag_names)}")
    print(f"  Scenarios: {len(feature.scenarios)}")
    print(f"  Rules: {len(feature.rules)}")

# Iterate all scenarios (including those inside Rules)
for scenario in project.all_scenarios():
    print(f"  Scenario: {scenario.name} — {len(scenario.steps)} steps")

# Iterate all steps
for step in project.all_steps():
    print(f"  {step.full_text}")
```

## 4. Query

```python
# Find features by tag
for f in project.find_features_with_tag("@smoke"):
    print(f.name)

# Find scenarios by tag
for s in project.find_scenarios(tag="@api"):
    print(s.name)

# Find steps by keyword
given_steps = project.find_steps(keyword="Given")
print(f"{len(given_steps)} Given steps")

# Find by name
for s in project.find_scenarios(name_contains="login"):
    print(s.name)
```

## 5. Serialize

**JSON:**

```python
from behave_model import JsonSerializer

json_text = JsonSerializer().serialize_project(project)
with open("project.json", "w") as f:
    f.write(json_text)
```

**Dict:**

```python
from behave_model import DictSerializer

data = DictSerializer().serialize_project(project)
print(data["features"][0]["name"])
```

**Pretty Print:**

```python
from behave_model import PrettyPrinter

printer = PrettyPrinter()
for feature in project.features:
    print(printer.print_feature(feature))
```

## 6. Validate

```python
from behave_model import Validator

validator = Validator()
issues = validator.validate(project)
for issue in issues:
    print(f"[{issue.severity}] {issue.message} — {issue.location}")
```

## 7. Transform

```python
from behave_model import rename_tag, sort_tags, sort_features

# Rename a tag project-wide
rename_tag(project, "@smoke", "@critical")

# Sort tags alphabetically in all elements
sort_tags(project)

# Sort features by name
sort_features(project)
```

## 8. Statistics

```python
stats = project.statistics()
print(f"Features: {stats['features']}")
print(f"Scenarios: {stats['scenarios']}")
print(f"Steps: {stats['steps']}")
print(f"Avg steps/scenario: {stats['average_steps_per_scenario']}")
print(f"Tags: {stats['tags']}")
```

## 9. Visitors

```python
from behave_model import CountingVisitor

counter = CountingVisitor()
project.accept(counter)
print(counter.counts)
# {'project': 1, 'feature': 4, 'scenario': 12, 'step': 45, ...}
```

## Next steps

- [First Project](first_project.md) — A complete walkthrough
- [Domain Model Guide](../guides/domain_model.md) — Understand every class
- [API Reference](../api/overview.md) — Complete reference
