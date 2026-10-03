# Transformations Guide

Transformations are safe, in-place mutations that preserve the semantic meaning of your feature files.

## Available transformations

| Function | Description |
| --- | --- |
| `rename_tag(project, old, new)` | Rename a tag project-wide |
| `rename_scenario(project, old, new)` | Rename a scenario |
| `sort_tags(project)` | Sort tags alphabetically in all elements |
| `sort_features(project, key=)` | Sort features by `key="name"` or `key="filename"` |
| `sort_scenarios(project, key=)` | Sort scenarios within features and rules (`key="name"` or `key="line"`) |
| `normalize_whitespace(project)` | Normalize whitespace in names and steps |
| `remove_tag(project, name)` | Remove a tag project-wide |
| `add_tag_to_feature(project, feature_name, tag)` | Add a tag to a specific feature |

## Renaming tags

```python
from behave_model import load_project, rename_tag

project = load_project("features/")

# Rename @smoke to @critical everywhere
rename_tag(project, "@smoke", "@critical")

# Verify
for tag in project.all_tags():
    print(tag.name)
```

## Removing tags

```python
from behave_model import remove_tag

# Remove @deprecated tag everywhere
remove_tag(project, "@deprecated")
```

## Adding tags

```python
from behave_model import add_tag_to_feature

# Add @regression tag to the Login feature
add_tag_to_feature(project, "Login", "@regression")
```

## Sorting

**Tags:**

```python
from behave_model import sort_tags

sort_tags(project)
# Tags are now alphabetically sorted in all features, rules, and scenarios
```

**Features:**

```python
from behave_model import sort_features

# Sort by name (default)
sort_features(project)

# Sort by filename
sort_features(project, key="filename")
```

**Scenarios:**

```python
from behave_model import sort_scenarios

sort_scenarios(project)
# Scenarios are now sorted within each feature and rule
```

## Normalizing whitespace

```python
from behave_model import normalize_whitespace

normalize_whitespace(project)
# Removes extra spaces, tabs, and normalizes newlines in:
# - Feature names and descriptions
# - Scenario names and descriptions
# - Step names
```

## Renaming scenarios

```python
from behave_model import rename_scenario

rename_scenario(project, "Successful login", "User logs in successfully")
```

## Combining transformations

```python
from behave_model import (
    load_project,
    rename_tag,
    remove_tag,
    sort_tags,
    sort_features,
    sort_scenarios,
    normalize_whitespace,
    PrettyPrinter,
)

project = load_project("features/")

# Clean up the project
rename_tag(project, "@smoke", "@critical")
remove_tag(project, "@deprecated")
normalize_whitespace(project)
sort_tags(project)
sort_features(project)
sort_scenarios(project)

# Export cleaned features
printer = PrettyPrinter()
for feature in project.features:
    text = printer.print_feature(feature)
    filename = feature.location.filename
    with open(filename, "w") as f:
        f.write(text)
    print(f"Updated: {filename}")
```

## Important notes

!!! warning "In-place mutations"
    Transformations modify the model in place. If you need to preserve the original, use `copy.deepcopy`:

    ```python
    import copy
    original = copy.deepcopy(project)
    rename_tag(project, "@smoke", "@critical")
    # `original` still has the old tag names
    ```

!!! info "Mutable model"
    Model objects are plain (mutable) dataclasses, so transformations assign
    attributes directly. Prefer the transformation functions over manual edits
    so invariants (e.g. rule-scoped scenarios) are respected.

## Next steps

- [Validation](validation.md) — Validate after transforming
- [Serializers](serializers.md) — Export after transforming
- [API Reference — Transformations](../api/transformations.md) — Complete API
