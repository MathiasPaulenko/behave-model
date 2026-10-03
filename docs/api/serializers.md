# API Reference — Serializers

## DictSerializer

Converts model objects to plain Python dictionaries.

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `serialize_project(project)` | `dict` | Full project as dict |
| `serialize_feature(feature)` | `dict` | Feature as dict |
| `serialize_rule(rule)` | `dict` | Rule as dict |
| `serialize_scenario(scenario)` | `dict` | Scenario as dict |
| `serialize_scenario_outline(outline)` | `dict` | ScenarioOutline as dict |
| `serialize_step(step)` | `dict` | Step as dict |
| `serialize_background(background)` | `dict` | Background as dict |
| `serialize_table(table)` | `dict` | Table as dict |
| `serialize_tag(tag)` | `dict` | Tag as dict |
| `serialize_examples(examples)` | `dict` | Examples as dict |
| `serialize_docstring(doc_string)` | `dict` | DocString as dict |
| `serialize_comment(comment)` | `dict` | Comment as dict |
| `serialize_location(location)` | `dict` | Location as dict |

---

## JsonSerializer

Wraps `DictSerializer` and outputs JSON strings.

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `serialize_project(project)` | `str` | Full project as JSON |
| `serialize_feature(feature)` | `str` | Feature as JSON |
| `to_dict(obj)` | `dict` | Convert a `Project` or `Feature` to dict |

---

## PrettyPrinter

Generates valid Gherkin `.feature` file text.

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `print_project(project)` | `str` | All features as Gherkin text |
| `print_feature(feature)` | `str` | Single feature as Gherkin text |

Per-element helpers (`_print_scenario`, `_print_rule`, `_print_step`,
`_print_table`, `_print_examples`) are private and called by
`print_feature`.
