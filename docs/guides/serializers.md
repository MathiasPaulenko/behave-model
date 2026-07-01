# Serializers Guide

Serializers convert the domain model into different output formats: JSON, Python dicts, and pretty-printed Gherkin text.

## Available serializers

| Serializer | Output | Use case |
| --- | --- | --- |
| `DictSerializer` | `dict` | Programmatic access, custom processing |
| `JsonSerializer` | `str` (JSON) | API responses, file export, data exchange |
| `PrettyPrinter` | `str` (Gherkin) | Round-trip printing, file regeneration |

## DictSerializer

Converts model objects to plain Python dictionaries.

```python
from behave_model import DictSerializer

serializer = DictSerializer()

# Serialize entire project
data = serializer.serialize_project(project)
print(data["type"])           # "project"
print(len(data["features"]))  # number of features

# Serialize single feature
fdata = serializer.serialize_feature(feature)
print(fdata["name"])
print(fdata["tags"])
print(fdata["scenarios"])
print(fdata.get("rules", []))

# Serialize single scenario
sdata = serializer.serialize_scenario(scenario)
print(sdata["name"])
print(sdata["steps"])
```

### Dict structure

```python
{
    "type": "project",
    "features": [
        {
            "type": "feature",
            "name": "Login",
            "description": "As a user...",
            "language": "en",
            "tags": [{"name": "@smoke"}, {"name": "@auth"}],
            "background": {
                "type": "background",
                "steps": [{"keyword": "Given", "name": "a database connection", ...}]
            },
            "scenarios": [
                {
                    "type": "scenario",
                    "name": "Successful login",
                    "tags": [{"name": "@happy"}],
                    "steps": [
                        {"keyword": "Given", "name": "the user is on the login page", ...},
                        {"keyword": "When", "name": "the user enters ...", ...},
                    ]
                }
            ],
            "rules": [
                {
                    "type": "rule",
                    "name": "Profile updates",
                    "tags": [],
                    "background": {...},
                    "scenarios": [...]
                }
            ]
        }
    ]
}
```

## JsonSerializer

Wraps `DictSerializer` and outputs JSON strings.

```python
from behave_model import JsonSerializer

serializer = JsonSerializer()

# Serialize to JSON string
json_text = serializer.serialize_project(project)

# Write to file
with open("project.json", "w") as f:
    f.write(json_text)

# Serialize single feature
feature_json = serializer.serialize_feature(feature)
```

### JSON output

```json
{
  "type": "project",
  "features": [
    {
      "type": "feature",
      "name": "Login",
      "tags": [{"name": "@smoke"}, {"name": "@auth"}],
      "scenarios": [...]
    }
  ]
}
```

## PrettyPrinter

Generates valid Gherkin `.feature` file text from the domain model.

```python
from behave_model import PrettyPrinter

printer = PrettyPrinter()

# Print entire project
text = printer.print_project(project)
print(text)

# Print single feature
feature_text = printer.print_feature(feature)
print(feature_text)

# Print single scenario
scenario_text = printer.print_scenario(scenario)
print(scenario_text)
```

### Output example

```gherkin
@smoke @auth
Feature: Login
  As a user
  I want to log in
  So that I can access the system

  Background:
    Given a database connection
    And the web server is running

  @happy
  Scenario: Successful login
    Given the user is on the login page
    When the user enters "admin" and "password"
    Then the user should be logged in
    And the dashboard should be visible
```

### Pretty printing with Rules

Rules are printed with proper indentation:

```gherkin
@auth
Feature: User Account Management

  Background:
    Given the user is logged in

  Rule: Profile updates
    Background:
      Given the user has a profile

    Scenario: Update display name
      When the user changes their display name to "Alice"
      Then the profile should show "Alice"
```

## Round-trip: Parse → Print → Parse

```python
from behave_model import load_project, PrettyPrinter, BehaveParserAdapter, parse_feature

# Load original
project = load_project("features/")
printer = PrettyPrinter()

for feature in project.features:
    # Print to text
    text = printer.print_feature(feature)

    # Re-parse
    bf = parse_feature(text, filename=feature.location.filename)
    adapter = BehaveParserAdapter()
    f2 = adapter.adapt_feature(bf, filename=feature.location.filename)

    # Verify
    assert f2.name == feature.name
    assert len(f2.scenarios) == len(feature.scenarios)
    print(f"Round-trip OK: {feature.name}")
```

## Next steps

- [Transformations](transformations.md) — Modify the model before serializing
- [API Reference — Serializers](../api/serializers.md) — Complete API
