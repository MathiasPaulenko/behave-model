# API Reference

## Model Classes

### `Project`
Root container for a parsed Behave project.

| Method | Returns | Description |
|--------|---------|-------------|
| `features` | `list[Feature]` | All features in the project |
| `all_scenarios()` | `list[Scenario \| ScenarioOutline]` | Every scenario across all features |
| `all_steps()` | `list[Step]` | Every step across all features |
| `all_tags()` | `list[Tag]` | Every tag in the project |
| `statistics()` | `dict` | Project metrics |
| `walk(strategy="dfs")` | `Iterator` | Traverse the entire tree |
| `accept(visitor)` | `None` | Accept a visitor |
| `find_feature(name)` | `Feature \| None` | Find feature by name |
| `find_tag(name)` | `Tag \| None` | Find tag by name |
| `find_scenarios(...)` | `list` | Filter scenarios by tag/name |
| `find_steps(...)` | `list[Step]` | Filter steps by keyword/text |

### `Feature`
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Feature name |
| `description` | `str` | Description text |
| `tags` | `list[Tag]` | Feature-level tags |
| `background` | `Background \| None` | Background block |
| `scenarios` | `list[Scenario \| ScenarioOutline]` | All scenarios |
| `location` | `Location` | Source location |
| `language` | `str` | Language code |

### `Rule` (Gherkin v6)
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Rule name |
| `description` | `str` | Description text |
| `tags` | `list[Tag]` | Rule-level tags |
| `background` | `Background \| None` | Rule-specific background |
| `scenarios` | `list[Scenario \| ScenarioOutline]` | Scenarios inside the rule |
| `location` | `Location` | Source location |
| `all_steps()` | `list[Step]` | All steps in the rule |
| `all_scenarios()` | `list` | All scenario-like elements |
| `has_tag(name)` | `bool` | Check if rule has a tag |
| `accept(visitor)` | `None` | Accept a visitor |

### `Scenario`
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Scenario name |
| `description` | `str` | Description text |
| `tags` | `list[Tag]` | Scenario tags |
| `steps` | `list[Step]` | Steps |
| `location` | `Location` | Source location |

### `ScenarioOutline`
Extends `Scenario` with `examples: list[Examples]`.

### `Step`
| Property | Type | Description |
|----------|------|-------------|
| `keyword` | `str` | Step keyword (Given, When, Then, etc.) |
| `name` | `str` | Step text |
| `text` | `str` | Alias for `name` |
| `full_text` | `str` | `keyword + " " + name` |
| `doc_string` | `DocString \| None` | Multi-line text |
| `data_table` | `Table \| None` | Data table |
| `location` | `Location` | Source location |

### `Table`
| Property/Method | Returns | Description |
|-----------------|---------|-------------|
| `headers` | `list[str]` | Column headers |
| `rows` | `list[TableRow]` | Data rows |
| `num_rows` | `int` | Row count |
| `num_columns` | `int` | Column count |
| `column_widths()` | `list[int]` | Max width per column |
| `iter_dicts()` | `Iterator[dict]` | Rows as dicts |

### `Tag`
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Tag name (with `@`) |
| `location` | `Location` | Source location |

### `Location`
| Property | Type | Description |
|----------|------|-------------|
| `filename` | `str` | Source file path |
| `line` | `int` | Line number |
| `column` | `int` | Column number |

## Parser Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `load_project(path)` | `Project` | Load all `.feature` files from a directory |
| `load_feature(path)` | `Feature` | Load a single `.feature` file |
| `parse_feature(text, filename=)` | `behave.model.Feature` | Parse raw text (low-level) |

## Visitor Classes

| Class | Description |
|-------|-------------|
| `Visitor` | Base class — override `visit_*` methods |
| `CountingVisitor` | Counts nodes by type |
| `CollectingVisitor` | Collects nodes by type |

## Serializer Classes

| Class | Methods | Description |
|-------|---------|-------------|
| `DictSerializer` | `serialize_project`, `serialize_feature`, ... | Converts to dicts |
| `JsonSerializer` | `serialize_project`, `serialize_feature` | Converts to JSON strings |
| `PrettyPrinter` | `print_project`, `print_feature` | Generates `.feature` text |

## Transformation Functions

| Function | Description |
|----------|-------------|
| `rename_tag(project, old, new)` | Rename a tag project-wide |
| `rename_scenario(project, old, new)` | Rename a scenario |
| `sort_tags(project)` | Sort tags alphabetically |
| `sort_features(project, key=)` | Sort features by name or filename |
| `sort_scenarios(project)` | Sort scenarios within features |
| `normalize_whitespace(project)` | Normalize whitespace in names/steps |
| `remove_tag(project, name)` | Remove a tag project-wide |
| `add_tag_to_feature(project, feature_name, tag)` | Add tag to a feature |

## Validation Classes

| Class | Description |
|-------|-------------|
| `Validator` | Runs all validation rules |
| `ValidationRule` | Base class for custom rules |
| `ValidationIssue` | A single validation finding |

## Exceptions

| Exception | Description |
|-----------|-------------|
| `BehaveModelError` | Base exception |
| `ParseError` | Parsing failure |
| `ValidationError` | Validation failure |
| `TransformationError` | Transformation failure |
| `SerializationError` | Serialization failure |
