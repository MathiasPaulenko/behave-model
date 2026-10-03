"""DocString (multi-line text) model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from behave_model.model.location import Location

if TYPE_CHECKING:
    from behave_model.visitors.visitor import Visitor


@dataclass
class DocString:
    """A docstring attached to a step.

    Attributes:
        content: The raw text content.
        content_type: Optional content-type hint (e.g. ``json``, ``xml``).
        delimiter: The delimiter used (``\"\"\"`` or `````).
        location: Source location.
    """

    content: str = ""
    content_type: str = ""
    delimiter: str = '"""'
    location: Location = field(default_factory=Location)

    @property
    def lines(self) -> list[str]:
        """Return the content split into lines."""
        return self.content.splitlines()

    def accept(self, visitor: Visitor) -> None:
        """Accept a visitor."""
        visitor.visit_docstring(self)
