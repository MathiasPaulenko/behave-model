"""Step model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.comment import Comment
from behave_model.model.docstring import DocString
from behave_model.model.location import Location
from behave_model.model.table import Table

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class Step:
    """A single step inside a background, scenario, or scenario outline.

    Attributes:
        keyword: The keyword as written (``Given``, ``When``, ``Then``, etc.).
        name: The step text after the keyword.
        text: Convenience alias for ``name``.
        doc_string: Optional DocString attached to the step.
        data_table: Optional data table attached to the step.
        comments: Comments associated with the step.
        location: Source location.
    """

    keyword: str = ""
    name: str = ""
    doc_string: DocString | None = None
    data_table: Table | None = None
    comments: list[Comment] = field(default_factory=list)
    location: Location = field(default_factory=Location)

    @property
    def text(self) -> str:
        """Alias for ``name``."""
        return self.name

    @text.setter
    def text(self, value: str) -> None:
        self.name = value

    @property
    def full_text(self) -> str:
        """The keyword and name combined."""
        return f"{self.keyword} {self.name}".strip()

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_step(self)

    def __str__(self) -> str:
        return self.full_text
