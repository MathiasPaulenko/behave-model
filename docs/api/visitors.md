# API Reference — Visitors

## Visitor

Base class for the visitor pattern. Override `visit_*` methods for the node types you care about.

```python
from behave_model import Visitor

class MyVisitor(Visitor):
    def visit_feature(self, feature):
        print(feature.name)
```

### Visit methods

| Method | Called for | Default behavior |
| --- | --- | --- |
| `visit_project(project)` | Project | Visits all features |
| `visit_feature(feature)` | Feature | Visits tags, background, scenarios, rules |
| `visit_rule(rule)` | Rule | Visits tags, background, scenarios |
| `visit_background(background)` | Background | Visits steps |
| `visit_scenario(scenario)` | Scenario | Visits tags and steps |
| `visit_scenario_outline(outline)` | ScenarioOutline | Visits tags, steps, examples |
| `visit_examples(examples)` | Examples | Visits table |
| `visit_step(step)` | Step | Visits table, doc_string |
| `visit_table(table)` | Table | No-op |
| `visit_table_row(row)` | TableRow | No-op |
| `visit_doc_string(doc_string)` | DocString | No-op |
| `visit_tag(tag)` | Tag | No-op |

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
print(len(collector.features))
print(len(collector.scenarios))
print(len(collector.steps))
print(len(collector.rules))
```

### Properties

| Property | Type | Description |
| --- | --- | --- |
| `features` | `list[Feature]` | All features |
| `scenarios` | `list[Scenario]` | All scenarios |
| `steps` | `list[Step]` | All steps |
| `rules` | `list[Rule]` | All rules |
| `tags` | `list[Tag]` | All tags |
| `tables` | `list[Table]` | All tables |
| `backgrounds` | `list[Background]` | All backgrounds |
