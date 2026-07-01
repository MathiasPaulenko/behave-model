# Quick Start Guide

## Installation

```bash
pip install behave-model
```

## Load a Project

```python
from behave_model import load_project

project = load_project("features/")
```

## Explore the Model

```python
# Features
for feature in project.features:
    print(f"Feature: {feature.name}")
    print(f"  Tags: {feature.tag_names}")
    print(f"  Scenarios: {len(feature.scenarios)}")

# Scenarios
for scenario in project.all_scenarios():
    print(f"  Scenario: {scenario.name} — {len(scenario.steps)} steps")

# Steps
for step in project.all_steps():
    print(f"  {step.full_text}")
```

## Query

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
```

## Serialize

```python
from behave_model import JsonSerializer

json_text = JsonSerializer().serialize_project(project)
with open("project.json", "w") as f:
    f.write(json_text)
```

## Validate

```python
from behave_model import Validator

validator = Validator()
issues = validator.validate(project)
for issue in issues:
    print(issue)
```

## Pretty Print

```python
from behave_model import PrettyPrinter

printer = PrettyPrinter()
for feature in project.features:
    print(printer.print_feature(feature))
```

## Transform

```python
from behave_model import rename_tag, sort_tags

rename_tag(project, "@smoke", "@critical")
sort_tags(project)
```

## Statistics

```python
stats = project.statistics()
print(f"Features: {stats['features']}")
print(f"Scenarios: {stats['scenarios']}")
print(f"Steps: {stats['steps']}")
print(f"Avg steps/scenario: {stats['average_steps_per_scenario']}")
print(f"Tags: {stats['tags']}")
```
