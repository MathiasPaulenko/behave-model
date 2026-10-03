# API Reference — Visitors

## Visitor

Base class for the visitor pattern. Override `visit_*` methods for the node types you care about. Traversal is driven by each node's `accept(visitor)` method — the default `visit_*` implementations are no-ops, so only nodes you hook are acted on.

```python
from behave_model import Visitor

class MyVisitor(Visitor):
    def visit_feature(self, feature):
        print(feature.name)
```

### Visit methods

| Method | Called for |
| --- | --- |
| `visit_project(project)` | Project |
| `visit_feature(feature)` | Feature |
| `visit_rule(rule)` | Rule |
| `visit_background(background)` | Background |
| `visit_scenario(scenario)` | Scenario |
| `visit_scenario_outline(outline)` | ScenarioOutline |
| `visit_examples(examples)` | Examples |
| `visit_step(step)` | Step |
| `visit_table(table)` | Table |
| `visit_docstring(docstring)` | DocString |
| `visit_tag(tag)` | Tag |
| `visit_comment(comment)` | Comment |

All default implementations are no-ops. After the `visit_*` call,
`accept` automatically descends into the node's children (tags, steps,
tables, docstrings, comments).

---

## CountingVisitor

Counts nodes by type.

```python
from behave_model import CountingVisitor

counter = CountingVisitor()
project.accept(counter)
print(counter.counts)
# {'project': 1, 'feature': 4, 'rule': 2, 'scenario': 12, 'step': 45, ...}
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `counts` | `dict[str, int]` | Count of each node type |

---

## CollectingVisitor

Collects nodes by type into lists.

```python
from behave_model import CollectingVisitor

collector = CollectingVisitor()
project.accept(collector)
print(len(collector.collection["feature"]))
print(len(collector.collection["scenario"]))
print(len(collector.collection["step"]))
print(len(collector.collection["rule"]))
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `collection` | `dict[str, list]` | Nodes grouped by type (`"project"`, `"feature"`, `"rule"`, `"background"`, `"scenario"`, `"scenario_outline"`, `"examples"`, `"step"`, `"table"`, `"docstring"`, `"tag"`, `"comment"`) |
