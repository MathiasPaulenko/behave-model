"""Metadata model for project-level information."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Metadata:
    """Project-level metadata.

    Attributes:
        created_at: When the project model was created.
        source_path: Root path from which the project was loaded.
        tool_version: Version of behave-model that produced this metadata.
        extra: Free-form key-value pairs for extensions.
    """

    created_at: datetime = field(default_factory=datetime.now)
    source_path: str = ""
    tool_version: str = "0.1.0"
    extra: dict[str, str] = field(default_factory=dict)
