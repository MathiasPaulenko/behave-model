# First Project Walkthrough

This guide walks through a complete example: loading feature files, exploring the model, querying, validating, and serializing.

## The feature files

We'll use the example features that ship with `behave-model`. Suppose you have this structure:

```text
features/
├── login.feature
├── shopping_cart.feature
├── data_tables.feature
└── rules.feature
```

### login.feature

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

  @api
  Scenario Outline: Login with role <role>
    Given the user is a <role>
    When the user logs in with <password>
    Then access should be <result>

    Examples:
      | role  | password | result  |
      | admin | secret   | granted |
      | guest | unknown  | denied  |
```

### rules.feature (Gherkin v6)

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

  Rule: Password management
    @security
    Scenario: Change password
      When the user changes their password
      Then the password should be updated
```

## Step 1: Load the project

```python
from behave_model import load_project

project = load_project("features/")
print(f"Loaded {len(project.features)} features")
```

Output:

```text
Loaded 4 features
```

## Step 2: Explore features and rules

```python
for feature in project.features:
    print(f"\nFeature: {feature.name}")
    print(f"  Tags: {feature.tag_names}")
    print(f"  Scenarios: {len(feature.scenarios)}")
    print(f"  Rules: {len(feature.rules)}")

    for rule in feature.rules:
        print(f"\n  Rule: {rule.name}")
        print(f"    Scenarios: {len(rule.scenarios)}")
        if rule.background:
            print(f"    Background: {rule.background.steps[0].full_text}")
```

## Step 3: Query by tag

```python
# Find all scenarios tagged @smoke
print("Smoke scenarios:")
for s in project.find_scenarios(tag="@smoke"):
    print(f"  {s.name}")

# Find all scenarios tagged @api
print("\nAPI scenarios:")
for s in project.find_scenarios(tag="@api"):
    print(f"  {s.name}")
```

Output:

```text
Smoke scenarios:
  Successful login

API scenarios:
  Login with role <role>
```

## Step 4: Access steps and tables

```python
for scenario in project.all_scenarios():
    if scenario.steps:
        first_step = scenario.steps[0]
        print(f"{scenario.name}: {first_step.full_text}")

        if first_step.data_table:
            print(f"  Table headers: {first_step.data_table.headers}")
            for row in first_step.data_table.iter_dicts():
                print(f"    {row}")
```

## Step 5: Validate

```python
from behave_model import Validator

validator = Validator()
issues = validator.validate(project)

if issues:
    for issue in issues:
        print(f"[{issue.severity}] {issue.rule_name}: {issue.message}")
else:
    print("No issues found!")
```

## Step 6: Serialize to JSON

```python
from behave_model import JsonSerializer
import json

serializer = JsonSerializer()
json_text = serializer.serialize_project(project)
data = json.loads(json_text)

print(f"Features in JSON: {len(data['features'])}")
print(f"First feature: {data['features'][0]['name']}")
```

## Step 7: Pretty print (roundtrip)

```python
from behave_model import PrettyPrinter

printer = PrettyPrinter()
for feature in project.features:
    text = printer.print_feature(feature)
    print(text[:200])
    print("...")
```

## Step 8: Statistics

```python
stats = project.statistics()

print(f"Features:     {stats['features']}")
print(f"Scenarios:    {stats['scenarios']}")
print(f"Steps:        {stats['steps']}")
print(f"Avg steps:    {stats['average_steps_per_scenario']:.1f}")
print(f"Tags:         {stats['tags']}")
```

## Next steps

- [Domain Model Guide](../guides/domain_model.md) — Understand every class and property
- [Gherkin v6 Rules](../guides/rules.md) — Deep dive into Rule support
- [API Reference](../api/overview.md) — Complete reference
