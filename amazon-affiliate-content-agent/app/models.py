"""Simple data models used by the application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Draft:
    """A basic draft record.

    This mirrors the structure of the `drafts` table in SQLite.
    """

    id: int | None
    title: str
    content: str
    status: str = "pending"
    created_at: datetime | None = None
