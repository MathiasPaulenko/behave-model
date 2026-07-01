"""Table (data table) model with helper methods."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field

from behave_model.model.location import Location


@dataclass
class TableRow:
    """A single row in a data table.

    Attributes:
        cells: List of cell values.
        location: Source location.
    """

    cells: list[str] = field(default_factory=list)
    location: Location = field(default_factory=Location)

    def __iter__(self) -> Iterator[str]:
        return iter(self.cells)

    def __len__(self) -> int:
        return len(self.cells)

    def __getitem__(self, index: int) -> str:
        return self.cells[index]

    def as_dict(self, headers: list[str] | None = None) -> dict[str, str]:
        """Return the row as a mapping of header -> cell value."""
        keys = headers if headers is not None else [f"col{i}" for i in range(len(self.cells))]
        return dict(zip(keys, self.cells, strict=False))


@dataclass
class Table:
    """A data table attached to a step or an Examples block.

    Attributes:
        headers: Column header names.
        rows: List of TableRow objects.
        location: Source location.
    """

    headers: list[str] = field(default_factory=list)
    rows: list[TableRow] = field(default_factory=list)
    location: Location = field(default_factory=Location)

    # -- traversal -----------------------------------------------------------

    def __iter__(self) -> Iterator[TableRow]:
        return iter(self.rows)

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> TableRow:
        return self.rows[index]

    # -- helpers -------------------------------------------------------------

    @property
    def num_columns(self) -> int:
        """Number of columns (based on headers)."""
        return len(self.headers)

    @property
    def num_rows(self) -> int:
        """Number of data rows."""
        return len(self.rows)

    def column_widths(self) -> list[int]:
        """Return the maximum width needed for each column."""
        widths = [len(h) for h in self.headers]
        for row in self.rows:
            for i, cell in enumerate(row.cells):
                if i < len(widths):
                    widths[i] = max(widths[i], len(cell))
                else:
                    widths.append(len(cell))
        return widths

    def iter_dicts(self) -> Iterator[dict[str, str]]:
        """Yield each row as a dict keyed by headers."""
        for row in self.rows:
            yield row.as_dict(self.headers)

    def to_list_of_dicts(self) -> list[dict[str, str]]:
        """Return all rows as a list of dicts."""
        return list(self.iter_dicts())
