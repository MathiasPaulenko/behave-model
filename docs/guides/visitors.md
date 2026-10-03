# Visitors Guide

The visitor pattern lets you traverse the entire domain model tree without coupling traversal logic to the model classes.

## How it works

Every visitable node (Project, Feature, Rule, Background, Scenario, ScenarioOutline, Examples, Step, Tag, Table, DocString, Comment) implements `accept(visitor)`, which calls the appropriate `visit_*` method on the visitor and then descends into its children.

```mermaid
graph TD
    A[project.accept visitor] --> B[visitor.visit_project]
    B --> C[feature.accept visitor]
    C --> D[visitor.visit_feature]
    D --> E[rule.accept visitor]
    E --> F[visitor.visit_rule]
    D --> G[scenario.accept visitor]
    G --> H[visitor.visit_scenario]
    H --> I[step.accept visitor]
    I --> J[visitor.visit_step]
```

## Base Visitor class

Subclass `Visitor` and override only the `visit_*` methods you need:

```python
from behave_model import Visitor

class MyVisitor(Visitor):
    def visit_project(self, project):
        print(f"Project with {len(project.features)} features")

    def visit_feature(self, feature):
        print(f"  Feature: {feature.name}")

    def visit_scenario(self, scenario):
        print(f"    Scenario: {scenario.name}")

    def visit_step(self, step):
        print(f"      {step.full_text}")
```

## Available visit methods

| Method | Called for |
| --- | --- |
| `visit_project(project)` | Project |
| `visit_feature(feature)` | Feature |
| `visit_rule(rule)` | Rule (Gherkin v6) |
| `visit_background(background)` | Background |
| `visit_scenario(scenario)` | Scenario |
| `visit_scenario_outline(outline)` | ScenarioOutline |
| `visit_examples(examples)` | Examples block |
| `visit_step(step)` | Step |
| `visit_table(table)` | Table |
| `visit_docstring(docstring)` | DocString |
| `visit_tag(tag)` | Tag |
| `visit_comment(comment)` | Comment |

## Built-in visitors

### CountingVisitor

Counts nodes by type:

```python
from behave_model import CountingVisitor

counter = CountingVisitor()
project.accept(counter)

print(counter.counts)
# {'project': 1, 'feature': 4, 'rule': 2, 'scenario': 12, 'step': 45, ...}
```

### CollectingVisitor

Collects nodes by type into lists:

```python
from behave_model import CollectingVisitor

collector = CollectingVisitor()
project.accept(collector)

print(f"Features: {len(collector.collection['feature'])}")
print(f"Scenarios: {len(collector.collection['scenario'])}")
print(f"Steps: {len(collector.collection['step'])}")
print(f"Rules: {len(collector.collection['rule'])}")
print(f"Tags: {len(collector.collection['tag'])}")
```

## Custom visitor examples

### Step keyword counter

```python
from behave_model import Visitor

class KeywordCounter(Visitor):
    def __init__(self):
        self.given = 0
        self.when = 0
        self.then = 0
        self.and_ = 0
        self.but = 0

    def visit_step(self, step):
        kw = step.keyword.lower().strip()
        if kw == "given":
            self.given += 1
        elif kw == "when":
            self.when += 1
        elif kw == "then":
            self.then += 1
        elif kw == "and":
            self.and_ += 1
        elif kw == "but":
            self.but += 1

counter = KeywordCounter()
project.accept(counter)
print(f"Given: {counter.given}, When: {counter.when}, Then: {counter.then}")
```

### Tag usage analyzer

```python
from behave_model import Visitor
from collections import Counter

class TagAnalyzer(Visitor):
    def __init__(self):
        self.tag_counts = Counter()

    def visit_tag(self, tag):
        self.tag_counts[tag.name] += 1

analyzer = TagAnalyzer()
project.accept(analyzer)

for tag, count in analyzer.tag_counts.most_common():
    print(f"  {tag}: {count}")
```

### Feature file printer

```python
from behave_model import Visitor

class SimplePrinter(Visitor):
    """Prints a flat outline of the feature tree.

    There are no ``visit_*_end`` hooks — `accept` drives a top-down
    traversal — so track depth differently (e.g., via the parent
    relationship) if you need nested indentation.
    """

    def __init__(self):
        self.lines = []

    def visit_feature(self, feature):
        for tag in feature.tags:
            self.lines.append(tag.name)
        self.lines.append(f"Feature: {feature.name}")

    def visit_rule(self, rule):
        self.lines.append(f"  Rule: {rule.name}")

    def visit_scenario(self, scenario):
        self.lines.append(f"  Scenario: {scenario.name}")

    def visit_scenario_outline(self, outline):
        self.lines.append(f"  Scenario Outline: {outline.name}")

    def visit_step(self, step):
        self.lines.append(f"    {step.full_text}")

printer = SimplePrinter()
project.accept(printer)
print("\n".join(printer.lines))
```

## Tree walking (alternative to visitors)

For simple traversal without a visitor class, use `walk()`:

```python
# Depth-first search (default)
for node in project.walk(strategy="dfs"):
    print(type(node).__name__)

# Breadth-first search
for node in project.walk(strategy="bfs"):
    print(type(node).__name__)
```

## Next steps

- [Query API](queries.md) — High-level filtering without visitors
- [API Reference — Visitors](../api/visitors.md) — Complete visitor API
