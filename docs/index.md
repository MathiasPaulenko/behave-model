---
title: behave-model — The canonical object model for Behave projects
description: Parse, query, transform, validate, and serialize Behave/Gherkin feature files with a clean Python API. Full Gherkin v6 Rules and Tag Expression v2 support.
---

# behave-model

**The canonical object model for [Behave](https://github.com/behave/behave) projects.**

`behave-model` provides a clean, stable, and extensible Python API that represents every element of a Behave project — features, rules, scenarios, steps, tags, tables, docstrings, and more.

---

## :rocket: Key Features

- :material-language-python: **Clean domain model** — Pure dataclasses, no external runtime dependencies beyond Behave
- :material-check-circle: **Compatible with Behave 1.3.x** — Tag Expression v2 and Gherkin v6 (including `Rule` blocks)
- :material-graph: **Visitor pattern** — Traverse the entire tree with custom visitors (DFS & BFS)
- :material-database-search: **Query API** — Find features, scenarios, steps, and tags by name, tag, or keyword
- :material-code-json: **Serializers** — Dict, JSON, and pretty-printed Gherkin output
- :material-swap-horizontal: **Transformations** — Safe in-place modifications (rename tags, sort, normalize)
- :material-shield-check: **Validation framework** — Pluggable rules with built-in checks
- :material-chart-bar: **Statistics** — Project metrics out of the box
- :material-test-tube: **95% test coverage** — Comprehensive unit, integration, and golden file tests

---

## :material-download: Installation

=== :material-language-python: pip

    ```bash
    pip install behave-model
    ```

=== :material-source-repository: From source

    ```bash
    git clone https://github.com/MathiasPaulenko/behave-model.git
    cd behave-model
    pip install -e ".[dev]"
    ```

---

## :material-lightning-bolt: Quick Example

```python
from behave_model import load_project

# Load all .feature files from a directory
project = load_project("features/")

# Access features and Gherkin v6 Rules
print(len(project.features))           # number of features
print(len(project.features[0].rules))  # rules (Gherkin v6)

# Query scenarios by tag
for scenario in project.find_scenarios(tag="@smoke"):
    print(f"  {scenario.name}")

# Get project statistics
stats = project.statistics()
print(f"{stats['features']} features, {stats['scenarios']} scenarios")
```

---

## :material-sitemap: Architecture at a Glance

```mermaid
graph TD
    A[Feature File] --> B[Parser Adapter]
    B --> C[Domain Model]
    C --> D[Visitors]
    C --> E[Queries]
    C --> F[Transformations]
    C --> G[Serializers]
    C --> H[Validation]
    C --> I[Statistics]
```

Each layer has a single responsibility and can be used independently. Read the [Architecture Overview](architecture.md) for details.

---

## :material-book-open-variant: Documentation Sections

| Section | Description |
| --- | --- |
| [Getting Started](getting-started/installation.md) | Install and run your first project in 5 minutes |
| [Guides](guides/domain_model.md) | In-depth guides for each subsystem |
| [API Reference](api/overview.md) | Complete class and function reference |
| [Architecture](architecture.md) | Layered design and design decisions |
| [Examples](examples.md) | Real-world usage patterns |
| [Changelog](changelog.md) | Release history and breaking changes |
| [Contributing](contributing.md) | How to contribute to the project |

---

## :material-compatibility: Compatibility

| Feature | Behave 1.3.x | behave-model |
| --- | --- | --- |
| Gherkin v6 `Rule` keyword | :material-check: | :material-check: |
| Tag Expression v2 | :material-check: | :material-check: |
| Scenario Outlines & Examples | :material-check: | :material-check: |
| Data Tables | :material-check: | :material-check: |
| DocStrings | :material-check: | :material-check: |
| Backgrounds (Feature & Rule) | :material-check: | :material-check: |
| Multi-language support | :material-check: | :material-check: |

---

## :material-license: License

MIT — see [LICENSE](https://github.com/MathiasPaulenko/behave-model/blob/main/LICENSE) for details.
