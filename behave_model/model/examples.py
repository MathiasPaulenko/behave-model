"""Examples model for scenario outlines."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.location import Location
from behave_model.model.table import Table
from behave_model.model.tag import Tag

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Examples:
    """An Examples table attached to a ScenarioOutline.

    Attributes:
        name: Optional name for the examples block.
        tags: Tags on the examples block.
        table: The data table containing headers and rows.
        location: Source location.
    """

    name: str = ""
    tags: list[Tag] = field(default_factory=list)
    table: Table = field(default_factory=Table)
    location: Location = field(default_factory=Location)

    @property
    def headers(self) -> list[str]:
        """Column headers from the underlying table."""
        return self.table.headers

    @property
    def rows(self) -> list:
        """Data rows from the underlying table."""
        return self.table.rows

    def accept(self, visitor: "Visitor") -> None:
        """Accept a visitor."""
        visitor.visit_examples(self)
