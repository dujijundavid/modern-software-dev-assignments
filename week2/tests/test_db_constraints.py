"""
Test suite for database constraint validation and data integrity.

Tests NOT NULL constraints, foreign key relationships, and edge cases.
"""
import pytest
import sqlite3
from unittest.mock import patch, MagicMock

from week2.app import db


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture(autouse=True)
def setup_test_db():
    """Initialize test database before each test."""
    db.init_db()


# ============================================================================
# Foreign Key Constraint Tests
# ============================================================================

def test_insert_action_items_with_valid_note_id():
    """Test insert_action_items succeeds with valid note_id."""
    note_id = db.insert_note("Parent note")
    ids = db.insert_action_items(["Task 1", "Task 2"], note_id=note_id)

    assert len(ids) == 2

    # Verify foreign key relationship
    items = db.list_action_items(note_id=note_id)
    assert all(item["note_id"] == note_id for item in items)


def test_insert_action_items_with_null_note_id():
    """Test insert_action_items succeeds with note_id=None."""
    ids = db.insert_action_items(["Task 1"], note_id=None)

    assert len(ids) == 1

    # Verify note_id is None
    items = db.list_action_items()
    item = items[0]
    assert item["note_id"] is None


def test_mark_action_item_done_with_invalid_id():
    """Test mark_action_item_done raises NotFoundError for invalid ID."""
    db.init_db()

    with pytest.raises(db.NotFoundError) as exc_info:
        db.mark_action_item_done(999999, True)

    assert exc_info.value.resource_type == "action item"
    assert exc_info.value.resource_id == 999999


# ============================================================================
# NOT NULL Constraint Tests
# ============================================================================

@patch('week2.app.db.get_connection')
def test_insert_note_empty_content_raises_error(mock_get_conn):
    """Test that inserting note with empty content violates NOT NULL."""
    # This test verifies the schema constraint
    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.execute.side_effect = sqlite3.IntegrityError("NOT NULL constraint failed: notes.content")

    with pytest.raises(db.DatabaseError):
        db.insert_note("")


@patch('week2.app.db.get_connection')
def test_insert_action_item_empty_text_raises_error(mock_get_conn):
    """Test that inserting action item with empty text violates NOT NULL."""
    mock_conn = MagicMock()
    mock_get_conn.return_value.__enter__.return_value = mock_conn
    mock_conn.cursor.return_value.execute.side_effect = sqlite3.IntegrityError("NOT NULL constraint failed: action_items.text")

    with pytest.raises(db.DatabaseError):
        db.insert_action_items([""], note_id=None)


# ============================================================================
# Data Type Validation Tests
# ============================================================================

def test_insert_note_returns_integer_id():
    """Test that insert_note returns an integer ID."""
    note_id = db.insert_note("Test note")

    assert isinstance(note_id, int)
    assert note_id > 0


def test_insert_action_items_returns_list_of_integers():
    """Test that insert_action_items returns list of integers."""
    ids = db.insert_action_items(["Task 1", "Task 2", "Task 3"])

    assert isinstance(ids, list)
    assert all(isinstance(id_, int) for id_ in ids)
    assert all(id_ > 0 for id_ in ids)
    assert len(ids) == 3


def test_mark_action_item_done_accepts_boolean():
    """Test that mark_action_item_done accepts boolean parameter."""
    item_id = db.insert_action_items(["Test task"])[0]

    # Mark as done
    db.mark_action_item_done(item_id, True)
    items = db.list_action_items()
    assert items[0]["done"] == 1

    # Mark as undone
    db.mark_action_item_done(item_id, False)
    items = db.list_action_items()
    assert items[0]["done"] == 0


# ============================================================================
# Auto-Increment and Default Value Tests
# ============================================================================

def test_note_id_auto_increments():
    """Test that note IDs auto-increment correctly."""
    id1 = db.insert_note("Note 1")
    id2 = db.insert_note("Note 2")
    id3 = db.insert_note("Note 3")

    assert id2 == id1 + 1
    assert id3 == id2 + 1


def test_action_item_id_auto_increments():
    """Test that action item IDs auto-increment correctly."""
    ids = db.insert_action_items(["Task 1", "Task 2", "Task 3"])

    assert ids[1] == ids[0] + 1
    assert ids[2] == ids[1] + 1


def test_created_at_has_default_value():
    """Test that created_at field is automatically populated."""
    note_id = db.insert_note("Test note")
    note = db.get_note(note_id)

    assert "created_at" in note
    assert note["created_at"] is not None
    assert len(note["created_at"]) > 0  # Non-empty string


def test_action_items_created_at_has_default_value():
    """Test that action_items created_at is automatically populated."""
    item_id = db.insert_action_items(["Test task"])[0]
    items = db.list_action_items()

    assert "created_at" in items[0]
    assert items[0]["created_at"] is not None
    assert len(items[0]["created_at"]) > 0


def test_done_has_default_value():
    """Test that done field defaults to 0 (False)."""
    item_id = db.insert_action_items(["Test task"])[0]
    items = db.list_action_items()

    assert items[0]["done"] == 0


# ============================================================================
# Transaction Rollback Tests
# ============================================================================

def test_insert_action_items_partial_failure_rolls_back():
    """Test that partial insert failures are handled correctly."""
    # This test verifies error handling behavior
    db.init_db()

    note_id = db.insert_note("Test note")

    # Mock scenario: first insert succeeds, second fails
    with patch('week2.app.db.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_get_conn.return_value.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.lastrowid = 1
        mock_conn.cursor.return_value.execute.side_effect = [
            None,  # First insert succeeds
            sqlite3.Error("Connection lost"),  # Second fails
        ]

        with pytest.raises(db.DatabaseError):
            db.insert_action_items(["Task 1", "Task 2"], note_id=note_id)


# ============================================================================
# Relationship Integrity Tests
# ============================================================================

def test_note_with_multiple_action_items():
    """Test that a note can have multiple action items."""
    note_id = db.insert_note("Meeting notes")
    item_ids = db.insert_action_items(
        ["Task 1", "Task 2", "Task 3"],
        note_id=note_id
    )

    # Verify all items are associated with the note
    items = db.list_action_items(note_id=note_id)
    assert len(items) == 3
    assert all(item["note_id"] == note_id for item in items)


def test_action_items_without_note():
    """Test that action items can exist without being tied to a note."""
    # Count existing items without note
    existing_items = [i for i in db.list_action_items() if i["note_id"] is None]
    existing_count = len(existing_items)

    ids = db.insert_action_items(["Standalone task"], note_id=None)

    items = [i for i in db.list_action_items() if i["note_id"] is None]
    assert len(items) == existing_count + 1

    # Get the newly created item (should be the last one)
    standalone_item = items[-1]
    assert standalone_item["note_id"] is None


def test_multiple_notes_with_action_items():
    """Test multiple notes with their respective action items."""
    note1_id = db.insert_note("Note 1")
    note2_id = db.insert_note("Note 2")

    items1_ids = db.insert_action_items(["N1 Task 1", "N1 Task 2"], note_id=note1_id)
    items2_ids = db.insert_action_items(["N2 Task 1"], note_id=note2_id)

    # Verify items are correctly filtered by note_id
    note1_items = db.list_action_items(note_id=note1_id)
    note2_items = db.list_action_items(note_id=note2_id)

    assert len(note1_items) == 2
    assert len(note2_items) == 1
    assert all(item["note_id"] == note1_id for item in note1_items)
    assert all(item["note_id"] == note2_id for item in note2_items)


# ============================================================================
# Data Consistency Tests
# ============================================================================

def test_list_action_items_returns_dict_structure():
    """Test that list_action_items returns proper dict structure."""
    note_id = db.insert_note("Test note for dict structure")
    item_id = db.insert_action_items(["Test task for dict structure"], note_id=note_id)[0]

    items = db.list_action_items()
    # Find our newly created item
    item = next((i for i in items if i["id"] == item_id), None)
    assert item is not None

    # Verify all expected fields are present
    assert "id" in item
    assert "note_id" in item
    assert "text" in item
    assert "done" in item
    assert "created_at" in item

    # Verify field types
    assert isinstance(item["id"], int)
    assert isinstance(item["note_id"], (int, type(None)))
    assert isinstance(item["text"], str)
    assert isinstance(item["done"], int)
    assert item["done"] in [0, 1]


def test_list_notes_returns_dict_structure():
    """Test that list_notes returns proper dict structure."""
    note_id = db.insert_note("Test note for dict structure")

    notes = db.list_notes()
    # Find our newly created note
    note = next((n for n in notes if n["id"] == note_id), None)
    assert note is not None

    # Verify all expected fields are present
    assert "id" in note
    assert "content" in note
    assert "created_at" in note

    # Verify field types
    assert isinstance(note["id"], int)
    assert isinstance(note["content"], str)
    assert isinstance(note["created_at"], str)


def test_get_note_returns_dict_structure():
    """Test that get_note returns proper dict structure."""
    note_id = db.insert_note("Test note")
    note = db.get_note(note_id)

    # Verify all expected fields are present
    assert "id" in note
    assert "content" in note
    assert "created_at" in note

    # Verify field types
    assert isinstance(note["id"], int)
    assert isinstance(note["content"], str)
    assert isinstance(note["created_at"], str)


# ============================================================================
# Edge Case Tests
# ============================================================================

def test_insert_empty_action_items_list():
    """Test inserting an empty list of action items."""
    ids = db.insert_action_items([], note_id=None)

    assert ids == []


def test_insert_action_items_with_special_characters():
    """Test inserting action items with special characters."""
    special_text = "Task with 'quotes' and \"double quotes\" and \n newlines"
    ids = db.insert_action_items([special_text], note_id=None)

    assert len(ids) == 1

    items = db.list_action_items()
    assert items[0]["text"] == special_text


def test_insert_note_with_unicode():
    """Test inserting note with Unicode characters."""
    unicode_text = "Meeting notes: 议程, rendez-vous, Тест"
    note_id = db.insert_note(unicode_text)

    note = db.get_note(note_id)
    assert note["content"] == unicode_text


def test_very_long_note_content():
    """Test inserting note with very long content."""
    long_content = "A" * 10000
    note_id = db.insert_note(long_content)

    note = db.get_note(note_id)
    assert note["content"] == long_content
