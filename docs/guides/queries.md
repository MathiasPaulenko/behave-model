# Query API Guide

The Query API provides high-level filtering functions to find features, scenarios, steps, and tags without manually traversing the tree.

## Finding features

### By name

```python
feature = project.find_feature("Login")
if feature:
    print(f"Found: {feature.name}")
```

### By tag

```python
for f in project.find_features_with_tag("@smoke"):
    print(f.name)
```

## Finding scenarios

### By tag

```python
for s in project.find_scenarios(tag="@api"):
    print(f"  {s.name}")
```

### By exact name

```python
for s in project.find_scenarios(name="Successful login"):
    print(s.name)
```

### By name substring

```python
for s in project.find_scenarios(name_contains="login"):
    print(s.name)
```

### Combined filters

```python
# Scenarios with @smoke tag AND name containing "login"
for s in project.find_scenarios(tag="@smoke", name_contains="login"):
    print(s.name)
```

### All scenarios (including those in Rules)

```python
for s in project.all_scenarios():
    print(f"{s.name} ({type(s).__name__})")
```

### Scenario Outlines only

```python
from behave_model import ScenarioOutline

for outline in project.find_outlines():
    print(f"Outline: {outline.name}")
    for examples in outline.examples:
        print(f"  Examples: {examples.name or '(unnamed)'}")
```

### Plain Scenarios only

```python
for s in project.find_plain_scenarios():
    print(f"Scenario: {s.name}")
```

## Finding steps

### By keyword

```python
given_steps = project.find_steps(keyword="Given")
when_steps = project.find_steps(keyword="When")
then_steps = project.find_steps(keyword="Then")

print(f"Given: {len(given_steps)}")
print(f"When: {len(when_steps)}")
print(f"Then: {len(then_steps)}")
```

### By text substring

```python
for step in project.find_steps(text_contains="login"):
    print(f"  {step.full_text}")
```

### Combined

```python
for step in project.find_steps(keyword="Given", text_contains="user"):
    print(f"  {step.full_text}")
```

## Finding tags

### By name

```python
tag = project.find_tag("@smoke")
if tag:
    print(f"Found tag: {tag.name} at {tag.location}")
```

### All tags

```python
for tag in project.all_tags():
    print(f"  {tag.name} — {tag.location}")
```

## Standalone query functions

All query methods on `Project` are also available as standalone functions:

```python
from behave_model import (
    find_feature,
    find_features_with_tag,
    find_scenarios,
    find_scenarios_with_tag,
    find_steps,
    find_tag,
    find_outlines,
    find_plain_scenarios,
)

# These work the same as the Project methods
for f in find_features_with_tag(project, "@smoke"):
    print(f.name)

for s in find_scenarios(project, tag="@api"):
    print(s.name)
```

## Practical examples

### Count scenarios per feature

```python
for feature in project.features:
    total = len(feature.scenarios)
    for rule in feature.rules:
        total += len(rule.scenarios)
    print(f"{feature.name}: {total} scenarios")
```

### Find unused tags

```python
all_tag_names = {t.name for t in project.all_tags()}
used_tag_names = set()

for feature in project.features:
    used_tag_names.update(feature.tag_names)
    for rule in feature.rules:
        used_tag_names.update(rule.tag_names)
    for scenario in feature.scenarios:
        used_tag_names.update(scenario.tag_names)
    for rule in feature.rules:
        for scenario in rule.scenarios:
            used_tag_names.update(scenario.tag_names)

unused = all_tag_names - used_tag_names
if unused:
    print(f"Unused tags: {unused}")
```

### Find duplicate scenario names

```python
from collections import Counter

names = Counter(s.name for s in project.all_scenarios())
for name, count in names.most_common():
    if count > 1:
        print(f"  Duplicate: '{name}' ({count} times)")
```

## Next steps

- [Visitors](visitors.md) — For complex traversal logic
- [Statistics](statistics.md) — Built-in metrics
- [API Reference — Model](../api/model.md) — Complete query API
