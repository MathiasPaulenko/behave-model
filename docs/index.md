# behave-model

**The canonical object model for [Behave](https://github.com/behave/behave) projects.**

`behave-model` provides a clean, stable, and extensible Python API that represents every element of a Behave project — features, rules, scenarios, steps, tags, tables, docstrings, and more.

## Key Features

- :material-check-circle: **Compatible with Behave 1.3.x** — Tag Expression v2 and Gherkin v6 (including `Rule` blocks)
- :material-check-circle: **Clean domain model** — Pure dataclasses, no external runtime dependencies beyond Behave
- :material-check-circle: **Visitor pattern** — Traverse the entire tree with custom visitors
- :material-check-circle: **Query API** — Find features, scenarios, steps, and tags by name, tag, or keyword
- :material-check-circle: **Serializers** — Dict, JSON, and pretty-printed Gherkin output
- :material-check-circle: **Transformations** — Safe in-place modifications (rename tags, sort, normalize)
- :material-check-circle: **Validation framework** — Pluggable rules with built-in checks
- :material-check-circle: **95% test coverage** — Comprehensive unit, integration, and golden file tests

## Installation

```bash
pip install behave-model
```

## Quick Example

```python
from behave_model import load_project

project = load_project("features/")

# Access features and rules
print(len(project.features))          # number of features
print(len(project.features[0].rules)) # rules (Gherkin v6)

# Query scenarios by tag
for scenario in project.find_scenarios(tag="@smoke"):
    print(scenario.name)

# Statistics
stats = project.statistics()
print(f"{stats['features']} features, {stats['scenarios']} scenarios")
```

## Next Steps

- [Quick Start Guide](quick_start.md) — Get up and running in 5 minutes
- [API Reference](api_reference.md) — Complete class and function reference
- [Architecture](architecture.md) — Understand the layered design
- [Contributing](contributing.md) — How to contribute to the project
