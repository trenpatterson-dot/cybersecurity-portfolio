"""Database helpers for SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from app.models import Draft


def _ensure_data_directory(database_path: Path) -> None:
    """Create the parent folder for the SQLite database if needed."""
    database_path.parent.mkdir(parents=True, exist_ok=True)


def get_connection(database_path: Path) -> sqlite3.Connection:
    """Open a SQLite connection with row access by column name."""
    _ensure_data_directory(database_path)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(database_path: Path) -> None:
    """Create the database file and required tables."""
    connection = get_connection(database_path)

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def row_to_draft(row: sqlite3.Row) -> Draft:
    """Convert a SQLite row into a Draft model."""
    return Draft(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        status=row["status"],
        created_at=row["created_at"],
    )
