# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-03

### Added
- `Validator.remove_rule(name)` — the counterpart to `add_rule`.

### Fixed
- Validation rules now cover scenarios, backgrounds, and tables inside
  Gherkin v6 Rules: `EmptyFeatureRule` no longer reports a false positive
  on features whose scenarios live only inside rules, and
  `DuplicateScenarioNamesRule`, `EmptyScenarioRule`, and `InvalidTableRule`
  check rule contents.
- Transformations (`rename_tag`, `remove_tag`, `sort_tags`,
  `rename_scenario`, `normalize_whitespace`, `sort_scenarios`) now apply
  inside Rules as well.
- `sort_scenarios(key=...)` no longer silently ignores its `key` argument;
  it accepts `"name"` (default) or `"line"` and raises `TransformationError`
  otherwise.
- Visitor traversal via `accept()` now reaches tags, tables, docstrings,
  and comments — `visit_tag`, `visit_table`, `visit_docstring`, and the new
  `visit_comment` are actually invoked. `CollectingVisitor` also collects
  `project`, `examples`, `table`, `docstring`, and `comment` nodes.
- `Project.walk()` now yields `Examples` tags and comments.
- `Metadata.tool_version` now defaults to the installed behave-model
  version instead of the hardcoded `"0.1.0"`.
- `find_scenarios(tag=)` and `find_scenarios_with_tag()` match inherited
  tags (feature, rule, and `Examples` tags apply to their scenarios),
  matching Behave's tag semantics. Exact `name=` matching is now
  case-insensitive, consistent with `find_feature`.
- `Tag` and `Comment` use `field(default_factory=Location)` instead of a
  shared `Location()` default.
- `load_feature` now raises `NotADirectoryError` when given a directory,
  and `load_project` when given a file — previously a file path silently
  produced an empty project and a directory raised an opaque read error.
- `Project.walk(strategy=...)` raises `ValueError` for unknown strategies
  instead of silently falling back to DFS.
- `BehaveParserAdapter` detects `ScenarioOutline` with `isinstance` instead
  of comparing class-name strings.
- `DictSerializer.serialize_project` now includes `metadata.created_at`
  and `metadata.extra`, and `serialize_table` emits a `row_locations`
  list so table-row locations are no longer dropped.

### Changed
- Duplicate-name validation is now case-insensitive.
- `add_tag_to_feature` and `rename_scenario` match names case-insensitively.

### Documentation
- Corrected multiple API inaccuracies: `ValidationIssue.rule` (was
  documented as `rule_name`), `Location.__str__` format, `statistics()`
  keys, `PrettyPrinter` public methods, `parse_project` signature,
  serializer and visitor method names, and `Metadata` fields.
- Removed the incorrect claim that all model classes are frozen
  dataclasses (only `Location` is frozen).
- Fixed the project structure listing and dev-dependency claims in the
  contributing guide.

### Build
- Added `build` and `twine` to the `dev` extra.
- `tox.ini` rewritten for tox 4 (`package = editable` + `extras = dev`).
- Pinned ruff `v0.16.10` in pre-commit and CI lint to keep them in sync.
- `release.yml`: removed `continue-on-error` on the PyPI publish job so
  publish failures fail the workflow.
- `docs.yml`: also triggers on `master` and on changes to the workflow itself.


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
