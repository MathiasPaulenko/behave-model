# Contributing to behave-model

Thank you for your interest in contributing! This guide covers everything you need to get started.

## Development setup

```bash
git clone https://github.com/MathiasPaulenko/behave-model.git
cd behave-model
pip install -e ".[dev]"
```

This installs `behave-model` with all development dependencies:

- `pytest` and `pytest-cov` — testing and coverage
- `ruff` — linting and formatting
- `mkdocs` and `mkdocs-material` — documentation building
- `build` and `twine` — package building and validation

## Running tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=behave_model --cov-report=term-missing

# Run a specific test file
python -m pytest tests/test_model.py -v

# Run only rule tests
python -m pytest tests/test_rules.py -v
```

## Linting and formatting

```bash
# Check linting
ruff check behave_model/ tests/

# Auto-fix linting issues
ruff check --fix behave_model/ tests/

# Check formatting
ruff format --check behave_model/ tests/

# Apply formatting
ruff format behave_model/ tests/
```

## Building documentation

```bash
# Serve docs locally with live reload
mkdocs serve

# Build static site
mkdocs build

# Build and view in browser
mkdocs serve --dev-addr 127.0.0.1:8000
```

## Building the package

```bash
# Build distributions
python -m build

# Validate distributions
python -m twine check dist/*
```

## Project structure

```text
behave-model/
├── behave_model/          # Source code
│   ├── __init__.py        # Public API exports
│   ├── exceptions.py      # Exception hierarchy
│   ├── model/             # Domain model classes
│   ├── parser/            # Parser adapter
│   ├── visitors/          # Visitor pattern
│   ├── queries.py         # Query functions
│   ├── serializers/       # Dict, JSON, PrettyPrinter
│   ├── transformations/   # In-place mutations
│   └── validation/        # Validation framework
├── tests/                 # Test suite
├── examples/              # Example .feature files
├── docs/                  # MkDocs documentation
├── .github/workflows/     # CI/CD workflows
├── pyproject.toml         # Package configuration
├── mkdocs.yml             # Documentation configuration
└── Makefile               # Common tasks
```

## Adding a new validation rule

1. Create a class extending `ValidationRule` in `behave_model/validation/`
2. Implement the `check(project)` method returning `list[ValidationIssue]`
3. Add it to the default rules in `Validator.__init__` if it should be on by default
4. Add tests in `tests/test_validation.py`
5. Update `CHANGELOG.md`

```python
from behave_model import ValidationRule, ValidationIssue

class MyCustomRule(ValidationRule):
    name = "MyCustomRule"
    severity = "warning"

    def check(self, project):
        issues = []
        # ... your logic ...
        return issues
```

## Adding a new serializer

1. Create a new serializer class in `behave_model/serializers/`
2. Follow the pattern of `DictSerializer` or `JsonSerializer`
3. Export it from `behave_model/serializers/__init__.py` and `behave_model/__init__.py`
4. Add tests
5. Update `CHANGELOG.md`

## Adding a new transformation

1. Add the function in `behave_model/transformations/`
2. Export it from `__init__.py` files
3. Add tests in `tests/test_transformation.py`
4. Update `CHANGELOG.md`

## Adding a new model class

1. Create the dataclass in `behave_model/model/`
2. Add `Location` and `accept(visitor)` if it should be visitable
3. Add a `visit_*` method to the base `Visitor`
4. Update `CountingVisitor` and `CollectingVisitor`
5. Update serializers and pretty printer
6. Export from `behave_model/__init__.py`
7. Add tests
8. Update `CHANGELOG.md`

## Pull request checklist

- [ ] Tests pass (`pytest tests/ -v`)
- [ ] Coverage remains above 90%
- [ ] Linting passes (`ruff check behave_model/ tests/`)
- [ ] Formatting passes (`ruff format --check behave_model/ tests/`)
- [ ] `CHANGELOG.md` updated
- [ ] Documentation updated if needed

## Reporting bugs

Please use [GitHub Issues](https://github.com/MathiasPaulenko/behave-model/issues) to report bugs. Include:

- Python version
- Behave version
- Minimal reproduction case
- Expected vs actual behavior
