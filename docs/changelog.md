# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-07-02

### Fixed
- `__version__` was stuck at `0.1.0` — now correctly reports `1.0.1`.
- README `make docs` command fixed to `make docs-serve` (the actual serve target).
- Removed non-existent `.pre-commit-config.yaml` from changelog.
- Replaced hardcoded coverage badge with dynamic Codecov badge.

### Changed
- Simplified README: removed duplicated content that lives in the documentation site.
- Simplified MkDocs config: removed Material-specific features (icons, tabs, tooltips)
  that required extra configuration. Navigation is now sidebar-only.
- Cleaned all docs: replaced `:material-*:` icons and `===` tabbed sections with
  plain markdown.
- Removed empty `docs/assets/` directory.


## [1.0.0] - 2026-07-02

### Added
- `Rule` model class for Gherkin v6 `Rule` keyword support.
- `Feature.rules` list and `Feature.all_scenarios()` now includes rule scenarios.
- `BehaveParserAdapter._adapt_rule()` to parse Behave Rule objects.
- `Visitor.visit_rule()` in base visitor, `CountingVisitor`, and `CollectingVisitor`.
- `Project` DFS/BFS traversal now includes Rule nodes.
- `DictSerializer.serialize_rule()` and rules in `serialize_feature()`.
- `PrettyPrinter._print_rule()` with proper indentation for rule scenarios.
- `Rule` exported in public API (`behave_model.Rule`).
- Example feature file `examples/rules.feature` demonstrating Gherkin v6 Rules.
- 31 new tests for Rule support in `tests/test_rules.py`.
- MkDocs Material documentation site with GitHub Pages deployment.
- CI/CD workflows: `ci.yml`, `release.yml`, `docs.yml`.
- `.gitignore`, `tox.ini`, `Makefile`, `conftest.py`.

### Changed
- Tests moved from `behave_model/tests/` to `tests/` at project root.
- `pyproject.toml` `testpaths` updated to `["tests"]`.
- `PrettyPrinter` scenario/outline/examples methods now accept `indent` parameter.
- `Project.all_scenarios()` delegates to `Feature.all_scenarios()` for rule inclusion.
- README rewritten with badges, compatibility table, and architecture overview.

### Compatibility
- Verified full compatibility with Behave 1.3.3.
- Verified Tag Expression v2 support (both v1 and v2 parsers present in Behave).
- Verified Gherkin v6 `Rule` keyword parsing and roundtrip.

## [0.1.0] - 2026-07-01

### Added
- Initial release of `behave-model`.
- Domain model: `Project`, `Feature`, `Background`, `Scenario`, `ScenarioOutline`,
  `Examples`, `Step`, `Table`, `Tag`, `DocString`, `Comment`, `Location`, `Metadata`.
- Parser adapter over Behave's built-in parser with `load_project` and `load_feature`.
- Visitor pattern with depth-first and breadth-first traversal.
- Query API: `find_feature`, `find_tag`, `find_steps`, `find_scenarios`.
- Serializers: dictionary and JSON.
- Transformations: rename tag, rename scenario, sort tags, sort features,
  normalize whitespace.
- Validation framework with pluggable rules.
- Statistics: feature count, scenario count, step count, average steps per
  scenario, tag count.
- Pretty printer that generates valid `.feature` files.
- Exception hierarchy: `BehaveModelError`, `ParseError`, `ValidationError`,
  `TransformationError`, `SerializationError`.
