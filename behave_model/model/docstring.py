"""DocString (multi-line text) model."""

from __future__ import annotations

from dataclasses import dataclass, field

from behave_model.model.location import Location


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
