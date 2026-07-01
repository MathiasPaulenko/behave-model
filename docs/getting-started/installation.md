# Installation

## Requirements

- Python 3.11 or higher
- [Behave](https://github.com/behave/behave) 1.2.6+ (installed automatically as a dependency)

## Install from PyPI

```bash
pip install behave-model
```

## Install from source

```bash
git clone https://github.com/MathiasPaulenko/behave-model.git
cd behave-model
pip install -e .
```

## Development installation

For contributing or running tests locally:

```bash
git clone https://github.com/MathiasPaulenko/behave-model.git
cd behave-model
pip install -e ".[dev]"
```

This installs `behave-model` along with:

- `pytest` and `pytest-cov` — testing and coverage
- `ruff` — linting and formatting
- `mkdocs` and `mkdocs-material` — documentation building

## Verify installation

```python
import behave_model
print(behave_model.__version__)
```

## Using with existing Behave projects

`behave-model` wraps Behave's parser, so it works with any existing `.feature` files. No changes to your feature files are needed.

```python
from behave_model import load_project

project = load_project("features/")
print(f"Loaded {len(project.features)} features")
```

## Next steps

- [Quick Start](quick_start.md) — Get up and running in 5 minutes
- [First Project](first_project.md) — A complete walkthrough
