# Design Decisions

## 1. Behave parser reuse

**Decision**: Wrap Behave's parser instead of reimplementing Gherkin parsing.

**Rationale**: Behave's parser is battle-tested, handles edge cases, supports multiple languages, and is compatible with Tag Expression v2. Reimplementing Gherkin parsing would be a massive effort and would inevitably lag behind Behave's updates.

**Trade-off**: We depend on `behave` as a runtime dependency. This is acceptable since `behave-model` is designed for Behave projects.

---

## 2. Frozen dataclasses

**Decision**: All model classes are frozen dataclasses.

**Rationale**: Immutability prevents accidental modifications and makes the model safer to share between functions. The `Location` class is also frozen for the same reason.

**Trade-off**: Transformations need `object.__setattr__` to modify frozen fields. This is an internal implementation detail that users don't see.

---

## 3. Composition over inheritance

**Decision**: Model classes are flat dataclasses, not a deep inheritance hierarchy.

**Rationale**: `ScenarioOutline` extends `Scenario` because they share the same interface. Everything else uses composition (e.g., `Feature` has `rules`, `scenarios`, `tags` — it doesn't inherit from them).

**Trade-off**: Some code duplication between `Feature` and `Rule` (both have `background`, `scenarios`, `tags`). This is preferable to a shared base class that would couple them.

---

## 4. Visitor pattern

**Decision**: Use the visitor pattern for tree traversal.

**Rationale**: Visitors decouple traversal logic from the model. You can add new operations (counting, collecting, analysis) without modifying model classes. The model just calls `visitor.visit_*` and the visitor decides what to do.

**Trade-off**: Adding a new model class requires adding a `visit_*` method to the base `Visitor`. This is a small, well-contained change.

---

## 5. In-place transformations

**Decision**: Transformations modify the model in place.

**Rationale**: Copying the entire model for every transformation would be expensive for large projects. Users who need immutability can `copy.deepcopy` before transforming.

**Trade-off**: Users must be aware that transformations are destructive. This is documented in the docstrings and guides.

---

## 6. Query mixin pattern

**Decision**: Query functions are mixed into `Project` and also available as standalone functions.

**Rationale**: `project.find_scenarios(tag="@smoke")` is more ergonomic than `find_scenarios(project, tag="@smoke")`. But standalone functions are useful for functional programming and composition.

**Trade-off**: The `Project` class has many methods. This is acceptable since they're all query-related and well-organized.

---

## 7. Gherkin v6 Rules as first-class objects

**Decision**: `Rule` is a first-class domain object, not just a grouping mechanism.

**Rationale**: Rules have their own background, tags, and scenarios. Treating them as first-class objects makes the model more accurate and enables Rule-specific queries, validation, and serialization.

**Trade-off**: `feature.scenarios` only returns scenarios not inside any Rule. Users must use `project.all_scenarios()` to get everything. This is documented clearly.

---

## 8. No external dependencies beyond Behave

**Decision**: `behave-model` only depends on `behave` at runtime.

**Rationale**: Minimizing dependencies makes the library easier to install and use in any environment. All dev dependencies (pytest, ruff, mkdocs) are optional.

**Trade-off**: We don't use libraries like `pydantic` for validation or `rich` for pretty printing. Our implementations are minimal but sufficient.
