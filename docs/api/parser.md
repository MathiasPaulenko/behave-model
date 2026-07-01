# API Reference — Parser

## Functions

### `load_project(path)`

Load all `.feature` files from a directory into a `Project`.

```python
from behave_model import load_project

project = load_project("features/")
```

| Parameter | Type | Description |
| --- | --- | --- |
| `path` | `str \| Path` | Directory containing `.feature` files |

| Returns | Description |
| --- | --- |
| `Project` | Root container with all parsed features |

---

### `load_feature(path)`

Load a single `.feature` file into a `Feature`.

```python
from behave_model import load_feature

feature = load_feature("features/login.feature")
```

| Parameter | Type | Description |
| --- | --- | --- |
| `path` | `str \| Path` | Path to a `.feature` file |

| Returns | Description |
| --- | --- |
| `Feature` | Parsed feature |

---

### `parse_feature(text, filename=None)`

Parse raw Gherkin text using Behave's parser. Returns a `behave.model.Feature`, not a `behave_model.Feature`.

```python
from behave_model import parse_feature

bf = parse_feature('Feature: Test\n  Scenario: S1\n    Given a step\n')
```

| Parameter | Type | Description |
| --- | --- | --- |
| `text` | `str` | Raw Gherkin text |
| `filename` | `str \| None` | Optional filename for location info |

| Returns | Description |
| --- | --- |
| `behave.model.Feature` | Behave's native feature object |

---

### `parse_project(path)`

Parse all `.feature` files from a directory. Returns a `Project` with adapted domain objects.

```python
from behave_model import parse_project

project = parse_project("features/")
```

---

## BehaveParserAdapter

Converts Behave's native model objects into `behave_model` domain objects.

```python
from behave_model import BehaveParserAdapter, parse_feature

bf = parse_feature('Feature: Test\n  Scenario: S1\n    Given a step\n')
adapter = BehaveParserAdapter()
feature = adapter.adapt_feature(bf, filename="test.feature")
```

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `adapt_feature(bf, filename=)` | `Feature` | Convert a Behave Feature to behave_model Feature |
| `adapt_scenario(bs)` | `Scenario \| ScenarioOutline` | Convert a Behave Scenario |
| `adapt_step(bs)` | `Step` | Convert a Behave Step |
| `adapt_background(bb)` | `Background` | Convert a Behave Background |
| `adapt_rule(br)` | `Rule` | Convert a Behave Rule (Gherkin v6) |
| `adapt_tag(bt)` | `Tag` | Convert a Behave Tag |
| `adapt_table(bt)` | `Table` | Convert a Behave Table |
| `adapt_examples(be)` | `Examples` | Convert Behave Examples |
