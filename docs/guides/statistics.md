# Statistics Guide

`behave-model` provides built-in statistics for any project, giving you instant insight into the size and composition of your feature suite.

## Quick statistics

```python
from behave_model import load_project

project = load_project("features/")
stats = project.statistics()

print(f"Features:     {stats['features']}")
print(f"Scenarios:    {stats['scenarios']}")
print(f"Steps:        {stats['steps']}")
print(f"Avg steps:    {stats['average_steps_per_scenario']:.1f}")
print(f"Tags:         {stats['tags']}")
```

## Available metrics

| Metric | Type | Description |
| --- | --- | --- |
| `features` | `int` | Total number of features |
| `scenarios` | `int` | Total scenarios (including those in Rules) |
| `steps` | `int` | Total steps across all scenarios and backgrounds |
| `tags` | `int` | Total unique tags in the project |
| `average_steps_per_scenario` | `float` | Mean steps per scenario |
| `scenario_outlines` | `int` | Number of Scenario Outlines |
| `examples` | `int` | Total example rows across all outlines |
| `rules` | `int` | Number of Gherkin v6 Rules |

## Detailed breakdown

```python
stats = project.statistics()

# Overview
print("=== Project Overview ===")
print(f"  Features:          {stats['features']}")
print(f"  Rules:             {stats['rules']}")
print(f"  Scenarios:         {stats['scenarios']}")
print(f"  Scenario Outlines: {stats['scenario_outlines']}")
print(f"  Examples:          {stats['examples']}")
print(f"  Steps:             {stats['steps']}")
print(f"  Tags:              {stats['tags']}")
print(f"  Avg steps/scenario: {stats['average_steps_per_scenario']:.1f}")
```

## Per-feature statistics

```python
for feature in project.features:
    scenario_count = len(feature.scenarios)
    for rule in feature.rules:
        scenario_count += len(rule.scenarios)

    step_count = sum(len(s.steps) for s in feature.scenarios)
    for rule in feature.rules:
        step_count += sum(len(s.steps) for s in rule.scenarios)
        if rule.background:
            step_count += len(rule.background.steps)

    print(f"\n{feature.name}:")
    print(f"  Scenarios: {scenario_count}")
    print(f"  Steps:     {step_count}")
    print(f"  Rules:     {len(feature.rules)}")
    print(f"  Tags:      {len(feature.tags)}")
```

## Tag distribution

```python
from collections import Counter

tag_counts = Counter()
for tag in project.all_tags():
    tag_counts[tag.name] += 1

print("Tag distribution:")
for tag, count in tag_counts.most_common():
    bar = "█" * count
    print(f"  {tag:20s} {bar} ({count})")
```

Output:

```text
Tag distribution:
  @smoke               ████ (4)
  @auth                ███ (3)
  @api                 ██ (2)
  @happy               █ (1)
```

## Step keyword distribution

```python
from behave_model import CountingVisitor

class KeywordStats(CountingVisitor):
    def __init__(self):
        super().__init__()
        self.keywords = Counter()

    def visit_step(self, step):
        self.keywords[step.keyword.strip()] += 1

stats = KeywordStats()
project.accept(stats)

print("Step keywords:")
for kw, count in stats.keywords.most_common():
    print(f"  {kw:10s} {count}")
```

## Export statistics as JSON

```python
import json
from behave_model import load_project

project = load_project("features/")
stats = project.statistics()

with open("stats.json", "w") as f:
    json.dump(stats, f, indent=2)
```

## Next steps

- [Query API](queries.md) — Filter and find specific elements
- [Visitors](visitors.md) — Custom analysis with the visitor pattern
- [API Reference — Model](../api/model.md) — Complete statistics API
