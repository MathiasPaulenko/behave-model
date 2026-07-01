# API Reference — Transformations

All transformations modify the model **in place**. Use `copy.deepcopy` if you need to preserve the original.

## Functions

### `rename_tag(project, old_name, new_name)`

Rename a tag across all features, rules, and scenarios.

```python
from behave_model import rename_tag
rename_tag(project, "@smoke", "@critical")
```

| Parameter | Type | Description |
| --- | --- | --- |
| `project` | `Project` | The project to modify |
| `old_name` | `str` | Current tag name (with `@`) |
| `new_name` | `str` | New tag name (with `@`) |

---

### `rename_scenario(project, old_name, new_name)`

Rename a scenario by exact name match.

```python
from behave_model import rename_scenario
rename_scenario(project, "Successful login", "User logs in successfully")
```

---

### `sort_tags(project)`

Sort tags alphabetically in all features, rules, and scenarios.

```python
from behave_model import sort_tags
sort_tags(project)
```

---

### `sort_features(project, key=None)`

Sort features by name (default) or a custom key function.

```python
from behave_model import sort_features

# Sort by name
sort_features(project)

# Sort by filename
sort_features(project, key=lambda f: f.location.filename)
```

| Parameter | Type | Description |
| --- | --- | --- |
| `project` | `Project` | The project to modify |
| `key` | `Callable \| None` | Sort key function (default: feature name) |

---

### `sort_scenarios(project)`

Sort scenarios alphabetically within each feature and rule.

```python
from behave_model import sort_scenarios
sort_scenarios(project)
```

---

### `normalize_whitespace(project)`

Normalize whitespace in all names, descriptions, and step text.

```python
from behave_model import normalize_whitespace
normalize_whitespace(project)
```

---

### `remove_tag(project, name)`

Remove a tag from all features, rules, and scenarios.

```python
from behave_model import remove_tag
remove_tag(project, "@deprecated")
```

---

### `add_tag_to_feature(project, feature_name, tag_name)`

Add a tag to a specific feature by name.

```python
from behave_model import add_tag_to_feature
add_tag_to_feature(project, "Login", "@regression")
```

| Parameter | Type | Description |
| --- | --- | --- |
| `project` | `Project` | The project to modify |
| `feature_name` | `str` | Exact feature name |
| `tag_name` | `str` | Tag to add (with `@`) |
