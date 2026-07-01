<div align="center">

# behave-model

**The canonical object model for [Behave](https://github.com/behave/behave) projects.**

[![CI](https://github.com/MathiasPaulenko/behave-model/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/behave-model/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/behave-model.svg)](https://pypi.org/project/behave-model/)
[![Python](https://img.shields.io/pypi/pyversions/behave-model.svg)](https://pypi.org/project/behave-model/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)](https://github.com/MathiasPaulenko/behave-model)

[Documentation](https://mathiaspaulenko.github.io/behave-model/) · [Getting Started](https://mathiaspaulenko.github.io/behave-model/getting-started/quick_start/) · [API Reference](https://mathiaspaulenko.github.io/behave-model/api/overview/) · [Changelog](https://mathiaspaulenko.github.io/behave-model/changelog/)

</div>

---

`behave-model` provides a clean, stable, and extensible Python API that represents every element of a Behave project — features, rules, scenarios, steps, tags, tables, docstrings, and more.

**Why does this exist?** Every Behave tooling project parses `.feature` files independently, duplicating effort and producing inconsistent results. `behave-model` provides a single, well-tested domain model so that tools can depend on it instead of reinventing the parser.

## Installation

```bash
pip install behave-model
```

## Quick Example

```python
from behave_model import load_project

project = load_project("features/")

# Query scenarios by tag
for scenario in project.find_scenarios(tag="@smoke"):
    print(scenario.name)

# Statistics
stats = project.statistics()
print(f"{stats['features']} features, {stats['scenarios']} scenarios, {stats['steps']} steps")

# Validate
from behave_model import Validator
issues = Validator().validate(project)
for issue in issues:
    print(f"[{issue.severity}] {issue.message}")
```

## Requirements

- Python >= 3.11
- `behave >= 1.2.6` (only runtime dependency)

## Features

- **Gherkin v6** — Full `Rule` keyword support
- **Domain model** — Pure frozen dataclasses for every Gherkin element
- **Visitor pattern** — DFS/BFS tree traversal with custom visitors
- **Query API** — Filter by name, tag, keyword, or text content
- **Serializers** — Dict, JSON, and pretty-printed Gherkin output
- **Transformations** — Rename, sort, normalize, add/remove tags and scenarios
- **Validation** — Pluggable rule framework with built-in checks
- **Statistics** — Project metrics out of the box

## Documentation

All guides, API reference, examples, and architecture docs are at **[mathiaspaulenko.github.io/behave-model](https://mathiaspaulenko.github.io/behave-model/)**.

## Development

```bash
git clone https://github.com/MathiasPaulenko/behave-model.git
cd behave-model
pip install -e ".[dev]"
make test        # run tests
make lint        # lint with ruff
make docs        # serve docs locally
```

## Contributing

Contributions are welcome! See the [Contributing guide](https://mathiaspaulenko.github.io/behave-model/contributing/) for guidelines.

## License

MIT — see [LICENSE](https://github.com/MathiasPaulenko/behave-model/blob/main/LICENSE).
