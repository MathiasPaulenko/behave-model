"""Pretty printer — generates valid ``.feature`` files from the domain model.

The printer prioritizes **correctness** over formatting quality.
The output is always semantically equivalent to the input model.
"""

from __future__ import annotations

from behave_model.model.background import Background
from behave_model.model.docstring import DocString
from behave_model.model.examples import Examples
from behave_model.model.feature import Feature
from behave_model.model.project import Project
from behave_model.model.rule import Rule
from behave_model.model.scenario import Scenario
from behave_model.model.scenario_outline import ScenarioOutline
from behave_model.model.step import Step
from behave_model.model.table import Table


class PrettyPrinter:
    """Generates valid ``.feature`` file text from domain model objects."""

    def print_project(self, project: Project) -> str:
        """Print all features in a project, separated by blank lines."""
        parts = []
        for feature in project.features:
            parts.append(self.print_feature(feature))
        return "\n\n".join(parts)

    def print_feature(self, feature: Feature) -> str:
        """Print a single feature as valid Gherkin text."""
        lines: list[str] = []

        # tags
        if feature.tags:
            lines.append(" ".join(t.name for t in feature.tags))

        # feature line
        lines.append(f"Feature: {feature.name}" if feature.name else "Feature:")

        # description
        if feature.description:
            for desc_line in feature.description.splitlines():
                lines.append(f"  {desc_line}" if desc_line else "")

        # background
        if feature.background:
            lines.append("")
            lines.extend(self._print_background(feature.background))

        # scenarios
        for scenario in feature.scenarios:
            lines.append("")
            if isinstance(scenario, ScenarioOutline):
                lines.extend(self._print_scenario_outline(scenario))
            else:
                lines.extend(self._print_scenario(scenario))

        # rules (Gherkin v6)
        for rule in feature.rules:
            lines.append("")
            lines.extend(self._print_rule(rule))

        return "\n".join(lines)

    def _print_rule(self, rule: Rule) -> list[str]:
        lines: list[str] = []
        if rule.tags:
            lines.append("  " + " ".join(t.name for t in rule.tags))
        header = f"Rule: {rule.name}" if rule.name else "Rule:"
        lines.append(f"  {header}")
        if rule.description:
            for desc_line in rule.description.splitlines():
                lines.append(f"    {desc_line}" if desc_line else "")
        if rule.background:
            lines.append("")
            lines.extend(self._print_background(rule.background, base_indent=4))
        for scenario in rule.scenarios:
            lines.append("")
            if isinstance(scenario, ScenarioOutline):
                lines.extend(self._print_scenario_outline(scenario, indent=4))
            else:
                lines.extend(self._print_scenario(scenario, indent=4))
        return lines

    def _print_background(self, background: Background, base_indent: int = 2) -> list[str]:
        lines: list[str] = []
        header = "Background:"
        if background.name:
            header = f"Background: {background.name}"
        lines.append(f"{' ' * base_indent}{header}")
        for step in background.steps:
            lines.extend(self._print_step(step, indent=base_indent + 2))
        return lines

    def _print_scenario(self, scenario: Scenario, indent: int = 2) -> list[str]:
        lines: list[str] = []
        prefix = " " * indent
        if scenario.tags:
            lines.append(prefix + " ".join(t.name for t in scenario.tags))
        header = f"Scenario: {scenario.name}" if scenario.name else "Scenario:"
        lines.append(f"{prefix}{header}")
        if scenario.description:
            for desc_line in scenario.description.splitlines():
                lines.append(f"{prefix}  {desc_line}" if desc_line else "")
        for step in scenario.steps:
            lines.extend(self._print_step(step, indent=indent + 2))
        return lines

    def _print_scenario_outline(self, outline: ScenarioOutline, indent: int = 2) -> list[str]:
        lines: list[str] = []
        prefix = " " * indent
        if outline.tags:
            lines.append(prefix + " ".join(t.name for t in outline.tags))
        header = f"Scenario Outline: {outline.name}" if outline.name else "Scenario Outline:"
        lines.append(f"{prefix}{header}")
        if outline.description:
            for desc_line in outline.description.splitlines():
                lines.append(f"{prefix}  {desc_line}" if desc_line else "")
        for step in outline.steps:
            lines.extend(self._print_step(step, indent=indent + 2))
        for examples in outline.examples:
            lines.append("")
            lines.extend(self._print_examples(examples, indent=indent + 2))
        return lines

    def _print_examples(self, examples: Examples, indent: int = 4) -> list[str]:
        lines: list[str] = []
        prefix = " " * indent
        if examples.tags:
            lines.append(prefix + " ".join(t.name for t in examples.tags))
        header = "Examples:"
        if examples.name:
            header = f"Examples: {examples.name}"
        lines.append(f"{prefix}{header}")
        lines.extend(self._print_table(examples.table, indent=indent + 2))
        return lines

    def _print_step(self, step: Step, indent: int = 4) -> list[str]:
        lines: list[str] = []
        prefix = " " * indent
        lines.append(f"{prefix}{step.keyword} {step.name}".rstrip())

        if step.doc_string:
            lines.extend(self._print_docstring(step.doc_string, indent))

        if step.data_table:
            lines.extend(self._print_table(step.data_table, indent + 2))

        return lines

    def _print_docstring(self, docstring: DocString, indent: int) -> list[str]:
        lines: list[str] = []
        prefix = " " * (indent + 2)
        delimiter = docstring.delimiter or '"""'
        content_type = docstring.content_type or ""
        header = f"{prefix}{delimiter}"
        if content_type:
            header += content_type
        lines.append(header)
        for content_line in docstring.lines:
            lines.append(f"{prefix}{content_line}")
        lines.append(f"{prefix}{delimiter}")
        return lines

    def _print_table(self, table: Table, indent: int) -> list[str]:
        if not table.headers and not table.rows:
            return []

        widths = table.column_widths()
        prefix = " " * indent

        lines: list[str] = []

        # header row
        header_cells = []
        for i, h in enumerate(table.headers):
            w = widths[i] if i < len(widths) else len(h)
            header_cells.append(h.ljust(w))
        lines.append(f"{prefix}| {' | '.join(header_cells)} |")

        # data rows
        for row in table.rows:
            row_cells = []
            for i, cell in enumerate(row.cells):
                w = widths[i] if i < len(widths) else len(cell)
                row_cells.append(cell.ljust(w))
            lines.append(f"{prefix}| {' | '.join(row_cells)} |")

        return lines
