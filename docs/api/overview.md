# API Overview

The `behave-model` public API is organized into subsystems:

| Subsystem | Module | Description |
| --- | --- | --- |
| Model | `behave_model.model` | Domain classes (Project, Feature, Rule, Scenario, Step, ...) |
| Parser | `behave_model.parser` | Feature file loading and parsing |
| Visitors | `behave_model.visitors` | Visitor pattern for tree traversal |
| Queries | `behave_model.queries` | High-level filtering functions |
| Serializers | `behave_model.serializers` | Dict, JSON, and Gherkin output |
| Transformations | `behave_model.transformations` | In-place model modifications |
| Validation | `behave_model.validation` | Pluggable validation rules |
| Exceptions | `behave_model.exceptions` | Exception hierarchy |

## Public API

All public classes and functions are re-exported from `behave_model`:

```python
from behave_model import (
    # Model
    Project, Feature, Rule, Scenario, ScenarioOutline,
    Step, Table, TableRow, Tag, Background, Examples,
    DocString, Comment, Location, Metadata,
    # Parser
    load_project, load_feature, parse_feature, parse_project,
    BehaveParserAdapter,
    # Queries
    find_feature, find_features_with_tag, find_scenarios,
    find_scenarios_with_tag, find_steps, find_tag,
    find_outlines, find_plain_scenarios,
    # Visitors
    Visitor, CountingVisitor, CollectingVisitor,
    # Serializers
    DictSerializer, JsonSerializer, PrettyPrinter,
    # Transformations
    rename_tag, rename_scenario, sort_tags, sort_features,
    sort_scenarios, normalize_whitespace, remove_tag,
    add_tag_to_feature,
    # Validation
    Validator, ValidationRule, ValidationIssue,
    DuplicateScenarioNamesRule, DuplicateFeatureNamesRule,
    EmptyScenarioRule, EmptyFeatureRule, InvalidTableRule,
    # Exceptions
    BehaveModelError, ParseError, ValidationError,
    TransformationError, SerializationError,
)
```

## Subsystem pages

- [Model Classes](model.md) — Project, Feature, Rule, Scenario, Step, Table, Tag, Location
- [Parser](parser.md) — load_project, load_feature, parse_feature, BehaveParserAdapter
- [Visitors](visitors.md) — Visitor, CountingVisitor, CollectingVisitor
- [Serializers](serializers.md) — DictSerializer, JsonSerializer, PrettyPrinter
- [Transformations](transformations.md) — All transformation functions
- [Validation](validation.md) — Validator, ValidationRule, ValidationIssue, built-in rules
- [Exceptions](exceptions.md) — Exception hierarchy
