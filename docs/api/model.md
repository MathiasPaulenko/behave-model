# API Reference — Model Classes

## Project

Root container for a parsed Behave project.

```python
from behave_model import Project, Feature
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `features` | `list[Feature]` | All features in the project |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `all_scenarios()` | `list[Scenario \| ScenarioOutline]` | Every scenario across all features (including those in Rules) |
| `all_steps()` | `list[Step]` | Every step across all features |
| `all_tags()` | `list[Tag]` | Every tag in the project |
| `statistics()` | `dict` | Project metrics |
| `walk(strategy="dfs")` | `Iterator` | Traverse the entire tree (DFS or BFS) |
| `accept(visitor)` | `None` | Accept a visitor |
| `find_feature(name)` | `Feature \| None` | Find feature by exact name |
| `find_tag(name)` | `Tag \| None` | Find tag by exact name |
| `find_scenarios(tag=, name=, name_contains=)` | `list` | Filter scenarios (tag matches inherited feature/rule/examples tags; name matching is case-insensitive) |
| `find_steps(keyword=, text_contains=)` | `list[Step]` | Filter steps |
| `find_features_with_tag(tag)` | `list[Feature]` | Features with a given tag |
| `find_scenarios_with_tag(tag)` | `list` | Scenarios with a given tag (including inherited) |
| `find_outlines()` | `list[ScenarioOutline]` | All Scenario Outlines |
| `find_plain_scenarios()` | `list[Scenario]` | All plain Scenarios |

### Container protocol

```python
len(project)        # number of features
project[0]          # first feature
for f in project:   # iterate features
    pass
```

---

## Feature

Represents a single `.feature` file.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Feature name |
| `description` | `str` | Multi-line description text |
| `tags` | `list[Tag]` | Feature-level tags |
| `tag_names` | `list[str]` | Tag names as strings (with `@`) |
| `background` | `Background \| None` | Feature-level background |
| `scenarios` | `list[Scenario \| ScenarioOutline]` | Scenarios not inside any Rule |
| `rules` | `list[Rule]` | Gherkin v6 Rule blocks |
| `language` | `str` | Language code (default `"en"`) |
| `location` | `Location` | Source location |
| `comments` | `list[Comment]` | Comments (reserved — not populated by the parser yet) |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `all_scenarios()` | `list` | All scenarios including those in Rules |
| `all_steps()` | `list[Step]` | All steps in the feature |
| `all_tags()` | `list[Tag]` | All tags (feature, rules, scenarios, examples) |
| `outlines()` | `list[ScenarioOutline]` | Scenario Outlines (including those in Rules) |
| `plain_scenarios()` | `list[Scenario]` | Plain Scenarios (including those in Rules) |
| `has_tag(name)` | `bool` | Check if feature has a tag |
| `accept(visitor)` | `None` | Accept a visitor |

---

## Rule

A Gherkin v6 `Rule` block within a Feature.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Rule name |
| `description` | `str` | Description text |
| `tags` | `list[Tag]` | Rule-level tags |
| `tag_names` | `list[str]` | Tag names as strings |
| `background` | `Background \| None` | Rule-specific background |
| `scenarios` | `list[Scenario \| ScenarioOutline]` | Scenarios inside the rule |
| `location` | `Location` | Source location |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `all_steps()` | `list[Step]` | All steps in the rule (including background) |
| `all_scenarios()` | `list` | All scenario-like elements |
| `has_tag(name)` | `bool` | Check if rule has a tag |
| `accept(visitor)` | `None` | Accept a visitor |

---

## Background

Shared steps that run before each scenario in the containing scope.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Background name (usually `"Background"`) |
| `steps` | `list[Step]` | Background steps |
| `location` | `Location` | Source location |

---

## Scenario

A concrete scenario with steps.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Scenario name |
| `description` | `str` | Description text |
| `tags` | `list[Tag]` | Scenario tags |
| `tag_names` | `list[str]` | Tag names as strings |
| `steps` | `list[Step]` | Steps |
| `location` | `Location` | Source location |
| `comments` | `list[Comment]` | Comments (reserved — not populated by the parser yet) |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `has_tag(name)` | `bool` | Check if scenario has a tag |
| `accept(visitor)` | `None` | Accept a visitor |

---

## ScenarioOutline

A scenario template with `Examples` for data-driven testing. It shares
`Scenario`'s attributes but is a sibling class, not a subclass.

### Additional properties

| Property | Type | Description |
| --- | --- | --- |
| `examples` | `list[Examples]` | Examples blocks |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `expand()` | `list[Scenario]` | One `Scenario` per example row |

---

## Examples

A data table attached to a ScenarioOutline.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Optional name (`""` if unnamed) |
| `tags` | `list[Tag]` | Examples-level tags |
| `table` | `Table` | Data table with example rows |
| `location` | `Location` | Source location |
| `headers` | `list[str]` | Shortcut to `table.headers` |
| `rows` | `list[TableRow]` | Shortcut to `table.rows` |

---

## Step

A single Given/When/Then step.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `keyword` | `str` | Step keyword (Given, When, Then, And, But) |
| `name` | `str` | Step text |
| `text` | `str` | Alias for `name` |
| `full_text` | `str` | `keyword + " " + name` |
| `doc_string` | `DocString \| None` | Multi-line text block |
| `data_table` | `Table \| None` | Data table |
| `location` | `Location` | Source location |

---

## Table

Structured data attached to a step.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `headers` | `list[str]` | Column headers |
| `rows` | `list[TableRow]` | Data rows |
| `num_rows` | `int` | Row count |
| `num_columns` | `int` | Column count |

### Methods

| Method | Returns | Description |
| --- | --- | --- |
| `column_widths()` | `list[int]` | Max width per column |
| `iter_dicts()` | `Iterator[dict]` | Rows as dicts keyed by headers |

---

## TableRow

A single row in a Table.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `cells` | `list[str]` | Cell values |
| `location` | `Location` | Source location |

---

## Tag

A label applied to features, rules, or scenarios.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `name` | `str` | Tag name (with `@`) |
| `location` | `Location` | Source location |

---

## DocString

A multi-line text block attached to a step.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `content` | `str` | Raw text content |
| `content_type` | `str` | Content type hint (e.g. `""`, `"json"`) |
| `delimiter` | `str` | Delimiter used (`'"""'` by default) |
| `location` | `Location` | Source location |
| `lines` | `list[str]` | Content split into lines |

---

## Location

Source location for traceability.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `filename` | `str` | Source file path |
| `line` | `int` | Line number |
| `column` | `int` | Column number |

### String representation

```python
str(Location(filename="login.feature", line=12))
# "login.feature, line 12"
```

---

## Comment

A comment line in a feature file.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `text` | `str` | Comment text (including `#`) |
| `location` | `Location` | Source location |

---

## Metadata

Project-level metadata.

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `created_at` | `datetime` | When the project model was created |
| `source_path` | `str` | Root path from which the project was loaded |
| `tool_version` | `str` | Version of behave-model that produced this metadata |
| `extra` | `dict[str, str]` | Free-form key-value pairs for extensions |
