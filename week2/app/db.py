from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional
import logging

# TODO 3: Added logging for better error tracking
logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


class DatabaseError(Exception):
    """Custom exception for database operations."""
    pass


class NotFoundError(Exception):
    """Exception for resource not found errors."""
    pass


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


def get_note(note_id: int) -> Optional[dict]:
    """Get a single note by ID, returning dict or None.
    
    TODO 3: Changed return type from Optional[sqlite3.Row] to Optional[dict].
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            return dict(row) if row else None
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
    
    TODO 3: Added error handling.
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to mark action item {action_item_id}: {e}")
        raise DatabaseError(f"Failed to mark action item: {e}") from e


