<div align="center">

# behave-model

**The canonical object model for [Behave](https://github.com/behave/behave) projects.**

[![CI](https://github.com/MathiasPaulenko/behave-model/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/behave-model/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/behave-model.svg)](https://pypi.org/project/behave-model/)
[![Python](https://img.shields.io/pypi/pyversions/behave-model.svg)](https://pypi.org/project/behave-model/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](https://github.com/MathiasPaulenko/behave-model)

[Documentation](https://mathiaspaulenko.github.io/behave-model/) · [Getting Started](https://mathiaspaulenko.github.io/behave-model/getting-started/quick_start/) · [Guides](https://mathiaspaulenko.github.io/behave-model/guides/domain_model/) · [API Reference](https://mathiaspaulenko.github.io/behave-model/api/overview/)

</div>

---

`behave-model` provides a clean, stable, and extensible Python API that represents every element of a Behave project — features, rules, scenarios, steps, tags, tables, docstrings, and more. It is the foundation for an entire ecosystem of tools: formatters, linters, analyzers, report generators, and anything else that needs to understand `.feature` files.

## Why?

Every Behave tooling project currently parses `.feature` files independently. `behave-model` provides a single, well-tested domain model so that future tools can depend on it instead of reinventing the parser.

- **Compatible with Behave 1.3.x** — Tag Expression v2 and Gherkin v6 (including `Rule` blocks)
- **Clean domain model** — Pure dataclasses, no external runtime dependencies beyond Behave
- **Visitor pattern** — Traverse the entire tree with custom visitors
- **Query API** — Find features, scenarios, steps, and tags by name, tag, or keyword
- **Serializers** — Dict, JSON, and pretty-printed Gherkin output
- **Transformations** — Safe in-place modifications (rename tags, sort, normalize)
- **Validation framework** — Pluggable rules with built-in checks
- **95% test coverage** — Comprehensive unit, integration, and golden file tests

## Installation

```bash
pip install behave-model
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from behave_model import load_project

# Load all .feature files from a directory
project = load_project("features/")

# Access features, rules, and scenarios
print(len(project.features))          # number of features
print(project.features[0].name)       # first feature name
print(len(project.features[0].rules)) # rules (Gherkin v6)

# Query the model
for scenario in project.find_scenarios(tag="@smoke"):
    print(scenario.name)

# Statistics
stats = project.statistics()
print(f"{stats['features']} features, {stats['scenarios']} scenarios, {stats['steps']} steps")

# Traverse the tree
for node in project.walk():
    print(type(node).__name__)
```

> 📖 **[Full Quick Start guide →](https://mathiaspaulenko.github.io/behave-model/getting-started/quick_start/)**

## Domain Model

```text
Project
├── Metadata
├── Feature
│   ├── Tag
│   ├── Background
│   │   └── Step
│   ├── Scenario
│   │   ├── Tag
│   │   └── Step
│   ├── ScenarioOutline
│   │   ├── Tag
│   │   ├── Step
│   │   └── Examples
│   │       └── Table
│   └── Rule (Gherkin v6)
│       ├── Tag
│       ├── Background
│       │   └── Step
│       ├── Scenario
│       └── ScenarioOutline
└── ...
```

Every node has a `Location` (filename, line, column) for precise source mapping.

> 📖 **[Domain Model guide →](https://mathiaspaulenko.github.io/behave-model/guides/domain_model/)**

## Features at a Glance

### Loading

```python
from behave_model import load_project, load_feature

project = load_project("features/")               # all .feature files
feature = load_feature("features/login.feature")  # single file
```

### Visitor Pattern

```python
from behave_model import Visitor

class StepCounter(Visitor):
    def __init__(self):
        self.count = 0

    def visit_step(self, step):
        self.count += 1

visitor = StepCounter()
project.accept(visitor)
print(f"Total steps: {visitor.count}")
```

> 📖 **[Visitors guide →](https://mathiaspaulenko.github.io/behave-model/guides/visitors/)**

### Query API

```python
project.find_feature("Login")
project.find_tag("@smoke")
project.find_scenarios(tag="@api")
project.find_scenarios(name_contains="login")
project.find_steps(keyword="Given")
project.find_steps(text_contains="user")
```

> 📖 **[Query API guide →](https://mathiaspaulenko.github.io/behave-model/guides/queries/)**

### Serialization

```python
from behave_model import JsonSerializer, DictSerializer, PrettyPrinter

# JSON
json_str = JsonSerializer().serialize_project(project)

# Dictionary
data = DictSerializer().serialize_project(project)

# Pretty-printed Gherkin
text = PrettyPrinter().print_feature(feature)
```

> 📖 **[Serializers guide →](https://mathiaspaulenko.github.io/behave-model/guides/serializers/)**

### Transformations

```python
from behave_model import rename_tag, sort_tags, normalize_whitespace

rename_tag(project, "@smoke", "@critical")
sort_tags(project)
normalize_whitespace(project)
```

> 📖 **[Transformations guide →](https://mathiaspaulenko.github.io/behave-model/guides/transformations/)**

### Validation

```python
from behave_model import Validator

validator = Validator()
issues = validator.validate(project)
for issue in issues:
    print(f"[{issue.severity}] {issue.rule_name}: {issue.message}")
```

> 📖 **[Validation guide →](https://mathiaspaulenko.github.io/behave-model/guides/validation/)**

## Architecture

```text
Feature File → Parser Adapter → Domain Model → Visitors → Queries → Transformations → Serializers
```

The Domain Model never depends on report generation or formatting. Each layer has a single responsibility and can be used independently.

| Layer | Package | Responsibility |
|-------|---------|----------------|
| Parser Adapter | `behave_model.parser` | Wraps Behave's parser, adapts to domain model |
| Domain Model | `behave_model.model` | Pure dataclasses for every Gherkin element |
| Visitors | `behave_model.visitors` | Generic traversal pattern |
| Queries | `behave_model.queries` | High-level filtering API |
| Transformations | `behave_model.transformations` | Safe in-place modifications |
| Serializers | `behave_model.serializers` | Dict, JSON, Gherkin output |
| Validation | `behave_model.validation` | Pluggable rule framework |

> 📖 **[Architecture overview →](https://mathiaspaulenko.github.io/behave-model/architecture/)** · **[Design decisions →](https://mathiaspaulenko.github.io/behave-model/design_decisions/)**

## Compatibility

| Feature | Supported |
|---------|-----------|
| Behave 1.3.x | ✅ |
| Tag Expression v1 | ✅ |
| Tag Expression v2 | ✅ |
| Gherkin v6 (Rules) | ✅ |
| Scenario Outlines | ✅ |
| Data Tables | ✅ |
| DocStrings | ✅ |
| Background | ✅ |
| Multi-language features | ✅ |

## Development

```bash
# Clone and install
git clone https://github.com/MathiasPaulenko/behave-model.git
cd behave-model
pip install -e ".[dev]"

# Run tests
make test

# Run tests with coverage
make coverage

# Lint
make lint

# Format
make format

# Build
make build
```

## Documentation

Full documentation is available at **[mathiaspaulenko.github.io/behave-model](https://mathiaspaulenko.github.io/behave-model/)**.

| Section | Link |
|---------|------|
| Getting Started | [Installation](https://mathiaspaulenko.github.io/behave-model/getting-started/installation/) · [Quick Start](https://mathiaspaulenko.github.io/behave-model/getting-started/quick_start/) · [First Project](https://mathiaspaulenko.github.io/behave-model/getting-started/first_project/) |
| Guides | [Domain Model](https://mathiaspaulenko.github.io/behave-model/guides/domain_model/) · [Gherkin v6 Rules](https://mathiaspaulenko.github.io/behave-model/guides/rules/) · [Visitors](https://mathiaspaulenko.github.io/behave-model/guides/visitors/) · [Queries](https://mathiaspaulenko.github.io/behave-model/guides/queries/) · [Serializers](https://mathiaspaulenko.github.io/behave-model/guides/serializers/) · [Transformations](https://mathiaspaulenko.github.io/behave-model/guides/transformations/) · [Validation](https://mathiaspaulenko.github.io/behave-model/guides/validation/) · [Statistics](https://mathiaspaulenko.github.io/behave-model/guides/statistics/) |
| API Reference | [Overview](https://mathiaspaulenko.github.io/behave-model/api/overview/) · [Model](https://mathiaspaulenko.github.io/behave-model/api/model/) · [Parser](https://mathiaspaulenko.github.io/behave-model/api/parser/) · [Visitors](https://mathiaspaulenko.github.io/behave-model/api/visitors/) · [Serializers](https://mathiaspaulenko.github.io/behave-model/api/serializers/) · [Transformations](https://mathiaspaulenko.github.io/behave-model/api/transformations/) · [Validation](https://mathiaspaulenko.github.io/behave-model/api/validation/) · [Exceptions](https://mathiaspaulenko.github.io/behave-model/api/exceptions/) |
| Other | [Architecture](https://mathiaspaulenko.github.io/behave-model/architecture/) · [Design Decisions](https://mathiaspaulenko.github.io/behave-model/design_decisions/) · [Examples](https://mathiaspaulenko.github.io/behave-model/examples/) · [Changelog](https://mathiaspaulenko.github.io/behave-model/changelog/) |

## Contributing

Contributions are welcome! See the [Contributing guide](https://mathiaspaulenko.github.io/behave-model/contributing/) for guidelines.

## License

MIT
