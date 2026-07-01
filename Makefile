.PHONY: install dev test test-verbose lint format coverage build clean docs docs-serve

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -q

test-verbose:
	pytest tests/ -v --tb=short

lint:
	ruff check behave_model/ tests/
	ruff format --check behave_model/ tests/

format:
	ruff format behave_model/ tests/
	ruff check --fix behave_model/ tests/

coverage:
	pytest tests/ --cov=behave_model --cov-report=term-missing --cov-report=html

build:
	python -m build

docs:
	mkdocs build --strict

docs-serve:
	mkdocs serve

clean:
	rm -rf build/ dist/ *.egg-info/ .coverage .pytest_cache/ htmlcov/ .tox/ .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
