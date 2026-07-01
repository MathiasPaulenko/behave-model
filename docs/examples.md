# Examples

Real-world usage patterns for `behave-model`.

## Example 1: Project health report

Generate a comprehensive health report for your Behave project.

```python
from behave_model import load_project, Validator
from collections import Counter

project = load_project("features/")

# Statistics
stats = project.statistics()
print("=== Project Statistics ===")
print(f"  Features:          {stats['features']}")
print(f"  Rules:             {stats['rules']}")
print(f"  Scenarios:         {stats['scenarios']}")
print(f"  Scenario Outlines: {stats['scenario_outlines']}")
print(f"  Steps:             {stats['steps']}")
print(f"  Tags:              {stats['tags']}")
print(f"  Avg steps/scenario: {stats['average_steps_per_scenario']:.1f}")

# Validation
print("\n=== Validation ===")
issues = Validator().validate(project)
errors = [i for i in issues if i.severity == "error"]
warnings = [i for i in issues if i.severity == "warning"]
print(f"  Errors:   {len(errors)}")
print(f"  Warnings: {len(warnings)}")
for issue in issues:
    print(f"    [{issue.severity}] {issue.rule_name}: {issue.message}")

# Tag distribution
print("\n=== Tag Distribution ===")
tag_counts = Counter(tag.name for tag in project.all_tags())
for tag, count in tag_counts.most_common():
    print(f"  {tag:20s} ({count})")

# Features without tags
print("\n=== Features Without Tags ===")
for f in project.features:
    if not f.tags:
        print(f"  {f.name}")
```

## Example 2: Clean and export features

Normalize, sort, and re-export all feature files.

```python
from behave_model import (
    load_project,
    normalize_whitespace,
    sort_tags,
    sort_features,
    sort_scenarios,
    PrettyPrinter,
)

project = load_project("features/")

# Clean up
normalize_whitespace(project)
sort_tags(project)
sort_features(project)
sort_scenarios(project)

# Export
printer = PrettyPrinter()
for feature in project.features:
    text = printer.print_feature(feature)
    with open(feature.location.filename, "w") as f:
        f.write(text)
    print(f"Cleaned: {feature.location.filename}")
```

## Example 3: Find duplicate scenario names

```python
from behave_model import load_project
from collections import Counter

project = load_project("features/")

names = Counter(s.name for s in project.all_scenarios())
duplicates = {n: c for n, c in names.items() if c > 1}

if duplicates:
    print("Duplicate scenario names found:")
    for name, count in sorted(duplicates.items()):
        print(f"  '{name}' — {count} times")
        for s in project.find_scenarios(name=name):
            print(f"    at {s.location}")
else:
    print("No duplicates found.")
```

## Example 4: Export to JSON for API consumption

```python
from behave_model import load_project, JsonSerializer
import json

project = load_project("features/")
json_text = JsonSerializer().serialize_project(project)

# Pretty-print and save
data = json.loads(json_text)
with open("project_export.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Exported {len(data['features'])} features to project_export.json")
```

## Example 5: Custom visitor for step analysis

```python
from behave_model import load_project, Visitor
from collections import Counter

class StepAnalyzer(Visitor):
    def __init__(self):
        self.keyword_counts = Counter()
        self.longest_step = None
        self._max_len = 0

    def visit_step(self, step):
        kw = step.keyword.strip()
        self.keyword_counts[kw] += 1

        if len(step.name) > self._max_len:
            self._max_len = len(step.name)
            self.longest_step = step

project = load_project("features/")
analyzer = StepAnalyzer()
project.accept(analyzer)

print("Step keyword distribution:")
for kw, count in analyzer.keyword_counts.most_common():
    print(f"  {kw:10s} {count}")

if analyzer.longest_step:
    s = analyzer.longest_step
    print(f"\nLongest step ({len(s.name)} chars):")
    print(f"  {s.full_text}")
    print(f"  at {s.location}")
```

## Example 6: CI/CD validation gate

```python
import sys
from behave_model import load_project, Validator

project = load_project("features/")
issues = Validator().validate(project)

errors = [i for i in issues if i.severity == "error"]
if errors:
    print(f"\n❌ {len(errors)} validation errors found:")
    for issue in errors:
        loc = str(issue.location) if issue.location else "unknown"
        print(f"  [{issue.rule_name}] {issue.message}")
        print(f"    at {loc}")
    sys.exit(1)
else:
    print("✅ All validation checks passed")
```

## Example 7: Migrate tags from v1 to v2

```python
from behave_model import load_project, rename_tag, remove_tag, PrettyPrinter

project = load_project("features/")

# Migrate old tag naming convention to new one
tag_mappings = {
    "@wip": "@draft",
    "@deprecated": "@to-remove",
    "@manual": "@needs-manual-check",
}

for old, new in tag_mappings.items():
    rename_tag(project, old, new)
    print(f"Renamed: {old} → {new}")

# Remove tags that are no longer needed
for tag in ["@old-test", "@legacy"]:
    remove_tag(project, tag)
    print(f"Removed: {tag}")

# Export updated features
printer = PrettyPrinter()
for feature in project.features:
    text = printer.print_feature(feature)
    with open(feature.location.filename, "w") as f:
        f.write(text)
```

## Example 8: Count scenarios per Rule

```python
from behave_model import load_project

project = load_project("features/")

for feature in project.features:
    if feature.rules:
        print(f"\n{feature.name}:")
        for rule in feature.rules:
            scenario_count = len(rule.scenarios)
            has_bg = "yes" if rule.background else "no"
            tags = ", ".join(rule.tag_names) or "(none)"
            print(f"  Rule: {rule.name}")
            print(f"    Scenarios: {scenario_count}")
            print(f"    Background: {has_bg}")
            print(f"    Tags: {tags}")
```
