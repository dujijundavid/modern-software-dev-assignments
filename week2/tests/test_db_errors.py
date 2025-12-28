"""
Test suite for database error handling and exception scenarios.

Tests database connection errors, constraint violations, and edge cases.
"""
import pytest
import sqlite3
from unittest.mock import patch, MagicMock
from pathlib import Path

from week2.app import db


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def reset_test_db():
    """Reset database before each test."""
    # Force re-initialization with clean state
    if db.DB_PATH.exists():
        db.DB_PATH.unlink()
    db.init_db()


# ============================================================================
# Database Connection Error Tests (Lines 133-135, 149-151, 172-173, 193-195, 217-219, 238-240)
# ============================================================================

@patch('week2.app.db.get_connection')
def test_insert_note_handles_connection_error(mock_get_conn):
    """Test insert_note handles connection errors gracefully (lines 133-135)."""
    mock_get_conn.side_effect = sqlite3.Error("Unable to open database file")

    with pytest.raises(db.DatabaseError) as exc_info:
        db.insert_note("Test note")

    assert "Failed to insert note" in str(exc_info.value)
    assert "Unable to open database file" in exc_info.value.message


@patch('week2.app.db.get_connection')
def test_list_notes_handles_connection_error(mock_get_conn):
    """Test list_notes handles connection errors (lines 149-151)."""
    mock_get_conn.side_effect = sqlite3.OperationalError("Database is locked")

    with pytest.raises(db.DatabaseError) as exc_info:
        db.list_notes()

    assert "Failed to list notes" in str(exc_info.value)
    assert "Database is locked" in exc_info.value.message


@patch('week2.app.db.get_connection')
def test_get_note_handles_connection_error(mock_get_conn):
    """Test get_note handles connection errors (lines 172-173)."""
    mock_get_conn.side_effect = sqlite3.DatabaseError("Connection lost")

    with pytest.raises(db.DatabaseError) as exc_info:
        db.get_note(1)

    assert "Failed to get note" in str(exc_info.value)


@patch('week2.app.db.get_connection')
def test_insert_action_items_handles_connection_error(mock_get_conn):
    """Test insert_action_items handles connection errors (lines 193-195)."""
    mock_get_conn.side_effect = sqlite3.IntegrityError("Foreign key constraint failed")

    with pytest.raises(db.DatabaseError) as exc_info:
        db.insert_action_items(["Task 1", "Task 2"], note_id=999999)

    assert "Failed to insert action items" in str(exc_info.value)


@patch('week2.app.db.get_connection')
def test_list_action_items_handles_connection_error(mock_get_conn):
    """Test list_action_items handles connection errors (lines 217-219)."""
    mock_get_conn.side_effect = sqlite3.Error("Disk I/O error")

    with pytest.raises(db.DatabaseError) as exc_info:
        db.list_action_items()

    assert "Failed to list action items" in str(exc_info.value)


@patch('week2.app.db.get_connection')
def test_mark_action_item_done_handles_connection_error(mock_get_conn):
    """Test mark_action_item_done handles connection errors (lines 238-240)."""
    mock_get_conn.side_effect = sqlite3.Error("Database corrupted")

    with pytest.raises(db.DatabaseError) as exc_info:
        db.mark_action_item_done(1, True)

    assert "Failed to mark action item" in str(exc_info.value)


# ============================================================================
# SQLite Exception Type Tests
# ============================================================================

@patch('week2.app.db.get_connection')
def test_wraps_sqlite3_operational_error(mock_get_conn):
    """Test that OperationalError is wrapped in DatabaseError."""
    mock_get_conn.side_effect = sqlite3.OperationalError("SQL logic error")

    with pytest.raises(db.DatabaseError):
        db.list_notes()


@patch('week2.app.db.get_connection')
def test_wraps_sqlite3_integrity_error(mock_get_conn):
    """Test that IntegrityError is wrapped in DatabaseError."""
    mock_get_conn.side_effect = sqlite3.IntegrityError("NOT NULL constraint failed")

    with pytest.raises(db.DatabaseError):
        db.insert_note("")


@patch('week2.app.db.get_connection')
def test_wraps_sqlite3_programming_error(mock_get_conn):
    """Test that ProgrammingError is wrapped in DatabaseError."""
    mock_get_conn.side_effect = sqlite3.ProgrammingError("Incorrect number of bindings")

    with pytest.raises(db.DatabaseError):
        db.get_note(1)


# ============================================================================
# Edge Case: Empty Result Sets
# ============================================================================

def test_list_notes_returns_empty_list_when_no_notes():
    """Test that list_notes returns empty list when database is empty."""
    # Clear database
    db.init_db()

    notes = db.list_notes()
    assert isinstance(notes, list)
    assert len(notes) == 0


def test_list_action_items_returns_empty_list_when_no_items():
    """Test that list_action_items returns empty list when no items exist."""
    db.init_db()

    items = db.list_action_items()
    assert isinstance(items, list)
    assert len(items) == 0


def test_list_action_items_filters_by_nonexistent_note_id():
    """Test list_action_items with note_id that has no items."""
    db.init_db()

    # Create a note but no action items
    note_id = db.insert_note("Note without actions")

    items = db.list_action_items(note_id=note_id)
    assert isinstance(items, list)
    assert len(items) == 0


# ============================================================================
# Data Directory Creation Tests
# ============================================================================

def test_ensure_data_directory_exists_creates_directory(tmp_path):
    """Test that ensure_data_directory_exists creates directory if missing."""
    with patch('week2.app.db.DATA_DIR', tmp_path / "new_data_dir"):
        db.ensure_data_directory_exists()

        assert db.DATA_DIR.exists()
        assert db.DATA_DIR.is_dir()


def test_init_db_creates_data_directory():
    """Test that init_db calls ensure_data_directory_exists."""
    with patch('week2.app.db.ensure_data_directory_exists') as mock_ensure:
        db.init_db()
        # Called by init_db and also by get_connection
        assert mock_ensure.call_count >= 1


def test_init_db_does_not_fail_if_directory_exists():
    """Test that init_db succeeds when directory already exists."""
    # Initialize once
    db.init_db()

    # Initialize again - should not fail
    db.init_db()


# ============================================================================
# Connection Pooling Tests
# ============================================================================

def test_get_connection_returns_connection_with_row_factory():
    """Test that get_connection sets row_factory correctly."""
    conn = db.get_connection()

    assert conn.row_factory == sqlite3.Row
    conn.close()


def test_get_connection_creates_database_file():
    """Test that get_connection creates database file."""
    # Remove existing DB
    if db.DB_PATH.exists():
        db.DB_PATH.unlink()

    conn = db.get_connection()
    conn.close()

    assert db.DB_PATH.exists()
    assert db.DB_PATH.is_file()


# ============================================================================
# Multiple Connection Tests
# ============================================================================

def test_concurrent_database_operations():
    """Test that multiple database operations work correctly."""
    # Create note and items
    note_id = db.insert_note("Test note")
    item_ids = db.insert_action_items(["Task 1", "Task 2"], note_id=note_id)

    # Verify all data is accessible
    note = db.get_note(note_id)
    assert note["content"] == "Test note"

    items = db.list_action_items(note_id=note_id)
    assert len(items) == 2
    assert all(item["note_id"] == note_id for item in items)

    # Mark as done
    db.mark_action_item_done(item_ids[0], True)

    # Verify update
    updated_items = db.list_action_items(note_id=note_id)
    marked_item = next(i for i in updated_items if i["id"] == item_ids[0])
    assert marked_item["done"] == 1


# ============================================================================
# Error Recovery Tests
# ============================================================================

def test_database_operations_after_error():
    """Test that database operations work after an error is handled."""
    # Try to get non-existent note
    try:
        db.get_note(999999)
        assert False, "Should have raised NotFoundError"
    except db.NotFoundError:
        pass  # Expected

    # Subsequent operations should work
    note_id = db.insert_note("Recovery test")
    note = db.get_note(note_id)
    assert note["content"] == "Recovery test"


def test_partial_failure_in_batch_insert():
    """Test behavior when some items in a batch fail."""
    # This is more of an integration test - the current implementation
    # will fail on the first error and roll back the transaction
    with patch('week2.app.db.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.lastrowid = 1
        mock_conn.cursor.return_value.execute.side_effect = [
            None,  # First insert succeeds
            sqlite3.Error("Connection lost"),  # Second fails
        ]

        with pytest.raises(db.DatabaseError):
            db.insert_action_items(["Task 1", "Task 2"])
