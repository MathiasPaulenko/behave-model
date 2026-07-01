# Contributing to behave-model

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/MathiasPaulenko/behave-model.git
cd behave-model
pip install -e ".[dev]"
```

## Running Tests

```bash
python -m pytest behave_model/tests/ -v
```

## Coverage

```bash
python -m pytest behave_model/tests/ --cov=behave_model --cov-report=term-missing
```

## Linting

```bash
ruff check behave_model/
ruff format --check behave_model/
```

## Adding a New Validation Rule

1. Create a class extending `ValidationRule` in `behave_model/validation/validator.py`
2. Implement the `check(project)` method returning `list[ValidationIssue]`
3. Add it to the default rules in `Validator.__init__` if it should be on by default
4. Add tests in `test_validation.py`

## Adding a New Serializer

1. Create a new serializer class in `behave_model/serializers/`
2. Follow the pattern of `DictSerializer` or `JsonSerializer`
3. Export it from `behave_model/serializers/__init__.py` and `behave_model/__init__.py`
4. Add tests

## Adding a New Transformation

1. Add the function in `behave_model/transformations/transform.py`
2. Export it from `__init__.py` files
3. Add tests in `test_transformation.py`

## Pull Request Checklist

- [ ] Tests pass
- [ ] Coverage remains above 90%
- [ ] Linting passes
- [ ] CHANGELOG.md updated
