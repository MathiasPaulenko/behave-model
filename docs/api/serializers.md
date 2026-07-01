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
| `serialize_doc_string(doc_string)` | `dict` | DocString as dict |

---

## JsonSerializer

Wraps `DictSerializer` and outputs JSON strings.

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `serialize_project(project)` | `str` | Full project as JSON |
| `serialize_feature(feature)` | `str` | Feature as JSON |

---

## PrettyPrinter

Generates valid Gherkin `.feature` file text.

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `print_project(project)` | `str` | All features as Gherkin text |
| `print_feature(feature)` | `str` | Single feature as Gherkin text |
| `print_scenario(scenario)` | `str` | Single scenario as Gherkin text |
| `print_rule(rule)` | `str` | Single rule as Gherkin text |
