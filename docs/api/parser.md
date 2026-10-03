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

### `parse_project(texts)`

Parse a mapping of `filename → Gherkin text` using Behave's parser.
Returns a list of `behave.model.Feature` objects — the raw Behave model,
not the `behave_model` domain model. To load a directory into the domain
model, use `load_project` instead.

```python
from behave_model import parse_project

behave_features = parse_project({"login.feature": "Feature: ..."})
```

| Parameter | Type | Description |
| --- | --- | --- |
| `texts` | `dict[str, str]` | Mapping of filename to Gherkin text |

| Returns | Description |
| --- | --- |
| `list[behave.model.Feature]` | Behave's native feature objects |

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
| `adapt_feature(bf, filename="")` | `Feature` | Convert a Behave Feature to behave_model Feature |
| `adapt_project(behave_features)` | `list[Feature]` | Convert a list of Behave Features |

The remaining converters (`_adapt_scenario`, `_adapt_step`,
`_adapt_background`, `_adapt_rule`, `_adapt_tag`, `_adapt_table`,
`_adapt_examples`) are internal helpers called by `adapt_feature`.
