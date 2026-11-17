"""Pretty printer — generates valid ``.feature`` files from the domain model.

The printer prioritizes **correctness** over formatting quality.
The output is always semantically equivalent to the input model.
"""

from __future__ import annotations

from behave import i18n

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

_ENGLISH = {
    "feature": "Feature",
    "rule": "Rule",
    "background": "Background",
    "scenario": "Scenario",
    "scenario_outline": "Scenario Outline",
    "examples": "Examples",
}


def _keywords(language: str) -> dict[str, str]:
    """Return the canonical Gherkin keywords for ``language``.

    Falls back to English for unknown language codes.
    """
    if not language or language == "en":
        return _ENGLISH
    table = i18n.languages.get(language)
    if not table:
        return _ENGLISH
    return {key: (table.get(key) or [default])[0] for key, default in _ENGLISH.items()}


class PrettyPrinter:
    """Generates valid ``.feature`` file text from domain model objects.

    Features with a non-English ``language`` are emitted with a
    ``# language:`` header and localized keywords, so printed output
    parses back to an equivalent model.
    """

    def print_project(self, project: Project) -> str:
        """Print all features in a project, separated by blank lines."""
        parts = []
        for feature in project.features:
            parts.append(self.print_feature(feature))
        return "\n\n".join(parts)

    def print_feature(self, feature: Feature) -> str:
        """Print a single feature as valid Gherkin text."""
        language = getattr(feature, "language", "en") or "en"
        kw = _keywords(language)
        lines: list[str] = []

        if language != "en":
            lines.append(f"# language: {language}")

        # tags
        if feature.tags:
            lines.append(" ".join(t.name for t in feature.tags))

        # feature line
        feature_kw = kw["feature"]
        lines.append(f"{feature_kw}: {feature.name}" if feature.name else f"{feature_kw}:")

        # description
        if feature.description:
            for desc_line in feature.description.splitlines():
                lines.append(f"  {desc_line}" if desc_line else "")

        # background
        if feature.background is not None:
            lines.append("")
            lines.extend(self._print_background(feature.background, kw=kw))

        # scenarios
        for scenario in feature.scenarios:
            lines.append("")
            if isinstance(scenario, ScenarioOutline):
                lines.extend(self._print_scenario_outline(scenario, kw=kw))
            else:
                lines.extend(self._print_scenario(scenario, kw=kw))

        # rules (Gherkin v6)
        for rule in feature.rules:
            lines.append("")
            lines.extend(self._print_rule(rule, kw=kw))

        return "\n".join(lines)

    def _print_rule(self, rule: Rule, kw: dict[str, str] | None = None) -> list[str]:
        kw = kw or _ENGLISH
        lines: list[str] = []
        if rule.tags:
            lines.append("  " + " ".join(t.name for t in rule.tags))
        rule_kw = kw["rule"]
        header = f"{rule_kw}: {rule.name}" if rule.name else f"{rule_kw}:"
        lines.append(f"  {header}")
        if rule.description:
            for desc_line in rule.description.splitlines():
                lines.append(f"    {desc_line}" if desc_line else "")
        if rule.background is not None:
            lines.append("")
            lines.extend(self._print_background(rule.background, base_indent=4, kw=kw))
        for scenario in rule.scenarios:
            lines.append("")
            if isinstance(scenario, ScenarioOutline):
                lines.extend(self._print_scenario_outline(scenario, indent=4, kw=kw))
            else:
                lines.extend(self._print_scenario(scenario, indent=4, kw=kw))
        return lines

    def _print_background(
        self,
        background: Background,
        base_indent: int = 2,
        kw: dict[str, str] | None = None,
    ) -> list[str]:
        kw = kw or _ENGLISH
        lines: list[str] = []
        bg_kw = kw["background"]
        header = f"{bg_kw}: {background.name}" if background.name else f"{bg_kw}:"
        lines.append(f"{' ' * base_indent}{header}")
        for step in background.steps:
            lines.extend(self._print_step(step, indent=base_indent + 2))
        return lines

    def _print_scenario(
        self,
        scenario: Scenario,
        indent: int = 2,
        kw: dict[str, str] | None = None,
    ) -> list[str]:
        kw = kw or _ENGLISH
        lines: list[str] = []
        prefix = " " * indent
        if scenario.tags:
            lines.append(prefix + " ".join(t.name for t in scenario.tags))
        sc_kw = kw["scenario"]
        header = f"{sc_kw}: {scenario.name}" if scenario.name else f"{sc_kw}:"
        lines.append(f"{prefix}{header}")
        if scenario.description:
            for desc_line in scenario.description.splitlines():
                lines.append(f"{prefix}  {desc_line}" if desc_line else "")
        for step in scenario.steps:
            lines.extend(self._print_step(step, indent=indent + 2))
        return lines

    def _print_scenario_outline(
        self,
        outline: ScenarioOutline,
        indent: int = 2,
        kw: dict[str, str] | None = None,
    ) -> list[str]:
        kw = kw or _ENGLISH
        lines: list[str] = []
        prefix = " " * indent
        if outline.tags:
            lines.append(prefix + " ".join(t.name for t in outline.tags))
        so_kw = kw["scenario_outline"]
        header = f"{so_kw}: {outline.name}" if outline.name else f"{so_kw}:"
        lines.append(f"{prefix}{header}")
        if outline.description:
            for desc_line in outline.description.splitlines():
                lines.append(f"{prefix}  {desc_line}" if desc_line else "")
        for step in outline.steps:
            lines.extend(self._print_step(step, indent=indent + 2))
        for examples in outline.examples:
            lines.append("")
            lines.extend(self._print_examples(examples, indent=indent + 2, kw=kw))
        return lines

    def _print_examples(
        self,
        examples: Examples,
        indent: int = 4,
        kw: dict[str, str] | None = None,
    ) -> list[str]:
        kw = kw or _ENGLISH
        lines: list[str] = []
        prefix = " " * indent
        if examples.tags:
            lines.append(prefix + " ".join(t.name for t in examples.tags))
        ex_kw = kw["examples"]
        header = f"{ex_kw}: {examples.name}" if examples.name else f"{ex_kw}:"
        lines.append(f"{prefix}{header}")
        lines.extend(self._print_table(examples.table, indent=indent + 2))
        return lines

    def _print_step(self, step: Step, indent: int = 4) -> list[str]:
        lines: list[str] = []
        prefix = " " * indent
        lines.append(f"{prefix}{step.keyword} {step.name}".rstrip())

        if step.doc_string is not None:
            lines.extend(self._print_docstring(step.doc_string, indent))

        if step.data_table is not None:
            lines.extend(self._print_table(step.data_table, indent + 2))

        return lines

    def _print_docstring(self, docstring: DocString, indent: int) -> list[str]:
        lines: list[str] = []
        prefix = " " * (indent + 2)
        delimiter = docstring.delimiter or '"""'
        if delimiter not in ('"""', "```"):
            delimiter = '"""'
        # A content line equal to the delimiter would close the docstring
        # early; fall back to the other Gherkin delimiter in that case.
        if any(line.strip() == delimiter for line in docstring.lines):
            delimiter = "```" if delimiter == '"""' else '"""'
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

        # header row — only when the table has headers; a phantom "|  |"
        # line would re-parse as a bogus empty header.
        if table.headers:
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
