# Architecture Guide

## Overview

`behave-model` is built in layers, each with a single responsibility:

```text
Feature File
    ↓
Parser Adapter      (behave_model.parser)
    ↓
Domain Model        (behave_model.model)
    ↓
Visitors            (behave_model.visitors)
    ↓
Queries             (behave_model.queries)
    ↓
Transformations     (behave_model.transformations)
    ↓
Serializers         (behave_model.serializers)
```

## Layer Details

### Parser Adapter

Wraps Behave's built-in parser (`behave.parser.parse_feature`) and converts
the result into behave-model domain objects via `BehaveParserAdapter`.

- `parser.py` — low-level parse functions
- `adapter.py` — converts behave.model objects → behave_model objects
- `loader.py` — file/directory loading (`load_feature`, `load_project`)

### Domain Model

Pure data classes with no external dependencies. Every node has:

- A `Location` (filename, line, column)
- An `accept(visitor)` method (for visitable nodes)
- Container protocol support (`__len__`, `__iter__`, `__getitem__`)

### Visitors

Generic visitor pattern with `Visitor` base class. Override `visit_*` methods
for the node types you care about. Built-in visitors: `CountingVisitor`,
`CollectingVisitor`.

### Queries

High-level filtering functions mixed into `Project`:

- `find_feature(name)`
- `find_tag(name)`
- `find_scenarios(tag=, name=, name_contains=)`
- `find_steps(keyword=, text_contains=)`

### Transformations

Safe, in-place mutations that preserve semantic meaning:

- `rename_tag`, `rename_scenario`
- `sort_tags`, `sort_features`, `sort_scenarios`
- `normalize_whitespace`
- `remove_tag`, `add_tag_to_feature`

### Serializers

- `DictSerializer` — plain Python dicts
- `JsonSerializer` — JSON strings
- `PrettyPrinter` — valid `.feature` file text

### Validation

Pluggable rule framework. Built-in rules:

- `DuplicateScenarioNamesRule`
- `DuplicateFeatureNamesRule`
- `EmptyScenarioRule`
- `EmptyFeatureRule`
- `InvalidTableRule`

Custom rules extend `ValidationRule` and implement `check(project)`.

## Design Decisions

- **Composition over inheritance**: Model classes are dataclasses, not deeply nested hierarchies.
- **Behave parser reuse**: We don't reimplement Gherkin parsing — we wrap Behave's parser.
- **Mutable model**: Transformations modify in place for performance. Use `copy.deepcopy` if you need immutability.
- **Future-proof**: The visitor/serializer/validation patterns allow extensions without API changes.
