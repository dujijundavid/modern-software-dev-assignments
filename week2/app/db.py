"""Database layer for the Action Item Extractor application.

This module provides a low-level interface to SQLite database operations,
including custom exceptions for error handling and automatic mapping between
database rows and Python dictionaries.

Exception Handling:
    - DatabaseError: Wrapped sqlite3.Error with contextual message
    - NotFoundError: Raised when a requested resource doesn't exist

All functions that perform database operations include proper error handling
and logging. Database results are returned as dicts for better decoupling
from the sqlite3.Row type.

Example:
    >>> from week2.app import db
    >>> db.init_db()  # Initialize database tables
    >>> note_id = db.insert_note("Buy groceries")
    >>> note = db.get_note(note_id)
    >>> print(note['content'])  # 'Buy groceries'
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


class DatabaseError(Exception):
    """Exception raised for database operation failures.

    This exception wraps low-level sqlite3.Error exceptions with
    contextual error messages for better error handling at the API layer.

    Attributes:
        message: Human-readable error description

    Example:
        >>> try:
        ...     db.insert_note("")
        ... except db.DatabaseError as e:
        ...     print(e.message)
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(Exception):
    """Exception raised when a requested resource doesn't exist.

    This exception is raised by get_note() and mark_action_item_done()
    when the specified ID cannot be found in the database.

    Attributes:
        resource_type: Type of resource (e.g., "note", "action item")
        resource_id: ID of the resource that was not found

    Example:
        >>> try:
        ...     db.get_note(999)
        ... except db.NotFoundError as e:
        ...     print(f"Resource: {e.resource_type}, ID: {e.resource_id}")
    """

    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message)


def ensure_data_directory_exists() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_data_directory_exists()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    ensure_data_directory_exists()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
        connection.commit()


def insert_note(content: str) -> int:
    """Insert a new note and return its ID.
    
    TODO 3: Added error handling for database operations.
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            connection.commit()
            return int(cursor.lastrowid)
    except sqlite3.Error as e:
        logger.error(f"Failed to insert note: {e}")
        raise DatabaseError(f"Failed to insert note: {e}") from e


def list_notes() -> list[dict]:
    """List all notes, returning dicts instead of sqlite3.Row.
    
    TODO 3: Changed return type from list[sqlite3.Row] to list[dict] for better decoupling.
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to list notes: {e}")
        raise DatabaseError(f"Failed to list notes: {e}") from e


def get_note(note_id: int) -> dict:
    """Get a single note by ID.

    Raises:
        NotFoundError: If note with given ID doesn't exist
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            if row is None:
                raise NotFoundError("note", note_id)
            return dict(row)
    except sqlite3.Error as e:
        logger.error(f"Failed to get note {note_id}: {e}")
        raise DatabaseError(f"Failed to get note: {e}") from e


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    """Insert multiple action items and return their IDs.
    
    TODO 3: Added error handling.
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            ids: list[int] = []
            for item in items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                ids.append(int(cursor.lastrowid))
            connection.commit()
            return ids
    except sqlite3.Error as e:
        logger.error(f"Failed to insert action items: {e}")
        raise DatabaseError(f"Failed to insert action items: {e}") from e


def list_action_items(note_id: Optional[int] = None) -> list[dict]:
    """List action items, optionally filtered by note_id. Returns dicts.
    
    TODO 3: Changed return type from list[sqlite3.Row] to list[dict].
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
                )
            else:
                cursor.execute(
                    "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                    (note_id,),
                )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to list action items: {e}")
        raise DatabaseError(f"Failed to list action items: {e}") from e


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """Mark an action item as done or undone.

    Raises:
        NotFoundError: If action item with given ID doesn't exist
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            if cursor.rowcount == 0:
                raise NotFoundError("action item", action_item_id)
            connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to mark action item {action_item_id}: {e}")
        raise DatabaseError(f"Failed to mark action item: {e}") from e


