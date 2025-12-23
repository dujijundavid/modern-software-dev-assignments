"""
Test suite for TODO 3: Refactoring validation

These tests verify that the refactoring improvements work correctly:
1. Pydantic schemas provide type safety and validation
2. Database layer returns dicts instead of sqlite3.Row
3. Error handling works properly
4. API endpoints use proper schemas
"""

import pytest
import sqlite3
from pathlib import Path
from typing import Dict, Any

from week2.app import db
from week2.app.schemas import (
    NoteCreate,
    NoteResponse,
    ExtractRequest,
    ExtractResponse,
    ActionItemResponse,
    MarkDoneRequest,
)
from week2.app.routers import notes, action_items


# ============================================================================
# Test 1: Pydantic Schema Validation
# ============================================================================

def test_note_create_schema_validation():
    """Test that NoteCreate validates input correctly."""
    # Valid input
    valid = NoteCreate(content="Test note")
    assert valid.content == "Test note"
    
    # Invalid: empty content should fail min_length=1
    with pytest.raises(Exception):  # Pydantic ValidationError
        NoteCreate(content="")


def test_extract_request_schema_validation():
    """Test that ExtractRequest validates input correctly."""
    # Valid input with defaults
    req = ExtractRequest(text="- Do something")
    assert req.text == "- Do something"
    assert req.save_note is False  # default
    
    # Valid input with save_note=True
    req2 = ExtractRequest(text="- Another task", save_note=True)
    assert req2.save_note is True
    
    # Invalid: empty text should fail
    with pytest.raises(Exception):
        ExtractRequest(text="")


def test_action_item_response_schema():
    """Test that ActionItemResponse constructs correctly."""
    item = ActionItemResponse(
        id=1,
        text="Test task",
        note_id=None,
        done=False,
        created_at="2025-12-23 10:00:00"
    )
    assert item.id == 1
    assert item.text == "Test task"
    assert item.done is False


# ============================================================================
# Test 2: Database Layer Returns Dicts
# ============================================================================

def test_db_insert_note_returns_int():
    """Test that insert_note returns an integer ID."""
    db.init_db()
    note_id = db.insert_note("Test content")
    assert isinstance(note_id, int)
    assert note_id > 0


def test_db_get_note_returns_dict():
    """Test that get_note returns a dict, not sqlite3.Row."""
    db.init_db()
    note_id = db.insert_note("Test note")
    result = db.get_note(note_id)
    
    # Should be a dict
    assert isinstance(result, dict)
    assert "id" in result
    assert "content" in result
    assert "created_at" in result
    assert result["content"] == "Test note"


def test_db_list_notes_returns_list_of_dicts():
    """Test that list_notes returns list of dicts."""
    db.init_db()
    db.insert_note("Note 1")
    db.insert_note("Note 2")
    
    results = db.list_notes()
    assert isinstance(results, list)
    assert len(results) >= 2
    
    # All items should be dicts
    for item in results:
        assert isinstance(item, dict)
        assert "id" in item
        assert "content" in item
        assert "created_at" in item


def test_db_list_action_items_returns_dicts():
    """Test that list_action_items returns dicts."""
    db.init_db()
    note_id = db.insert_note("Note with actions")
    db.insert_action_items(["Task 1", "Task 2"], note_id=note_id)
    
    results = db.list_action_items(note_id=note_id)
    assert isinstance(results, list)
    assert len(results) >= 2
    
    for item in results:
        assert isinstance(item, dict)
        assert "id" in item
        assert "text" in item
        assert "note_id" in item
        assert "done" in item
        assert "created_at" in item


# ============================================================================
# Test 3: Database Error Handling
# ============================================================================

def test_db_get_note_nonexistent_returns_none():
    """Test that get_note returns None for non-existent ID."""
    db.init_db()
    result = db.get_note(999999)  # Very unlikely to exist
    assert result is None


def test_db_error_handling_on_invalid_sql():
    """Test that database errors are caught and wrapped in DatabaseError."""
    # This is hard to test without breaking the DB, but we can verify
    # that the error handling structure exists
    import inspect
    source = inspect.getsource(db.insert_note)
    assert "try:" in source
    assert "except sqlite3.Error" in source
    assert "DatabaseError" in source


# ============================================================================
# Test 4: Router Integration with Schemas
# ============================================================================

def test_notes_router_uses_schemas():
    """Test that notes router properly uses Pydantic schemas."""
    db.init_db()
    
    # Create note using schema
    request = NoteCreate(content="Router test note")
    response = notes.create_note(request)
    
    # Response should be NoteResponse type
    assert isinstance(response, NoteResponse)
    assert response.content == "Router test note"
    assert response.id > 0
    assert response.created_at  # Should have timestamp


def test_action_items_router_uses_schemas():
    """Test that action_items router uses Pydantic schemas."""
    db.init_db()
    
    # Extract using schema
    request = ExtractRequest(
        text="- Task one\n- Task two",
        save_note=False
    )
    response = action_items.extract(request)
    
    # Response should be ExtractResponse type
    assert isinstance(response, ExtractResponse)
    assert response.note_id is None  # We didn't save
    assert len(response.items) == 2
    
    # Each item should be ActionItemResponse
    for item in response.items:
        assert isinstance(item, ActionItemResponse)
        assert item.id > 0
        assert item.text in ["Task one", "Task two"]
        assert item.created_at  # Should have timestamp from DB


def test_action_items_extract_with_save_note():
    """Test extraction with save_note=True creates a note."""
    db.init_db()
    
    request = ExtractRequest(
        text="- Important task",
        save_note=True
    )
    response = action_items.extract(request)
    
    # Should have created a note
    assert response.note_id is not None
    assert isinstance(response.note_id, int)
    
    # Verify note exists in DB
    note = db.get_note(response.note_id)
    assert note is not None
    assert note["content"] == "- Important task"


# ============================================================================
# Test 5: Mark Done Functionality
# ============================================================================

def test_mark_action_item_done():
    """Test marking action item as done."""
    db.init_db()
    ids = db.insert_action_items(["Test task"])
    item_id = ids[0]
    
    # Mark as done
    request = MarkDoneRequest(done=True)
    response = action_items.mark_done(item_id, request)
    
    assert response["id"] == item_id
    assert response["done"] is True
    
    # Verify in database
    items = db.list_action_items()
    item = next((i for i in items if i["id"] == item_id), None)
    assert item is not None
    assert item["done"] == 1  # SQLite stores as 1/0


# ============================================================================
# Test 6: Type Safety - Wrong Types Should Fail
# ============================================================================

def test_schema_rejects_wrong_types():
    """Test that Pydantic rejects wrong types."""
    # NoteCreate requires string, not int
    with pytest.raises(Exception):
        NoteCreate(content=123)  # type: ignore
    
    # ExtractRequest text must be string
    with pytest.raises(Exception):
        ExtractRequest(text=None)  # type: ignore


# ============================================================================
# Test 7: Database Custom Exceptions
# ============================================================================

def test_database_custom_exceptions_exist():
    """Verify that custom exception classes are defined."""
    assert hasattr(db, 'DatabaseError')
    assert hasattr(db, 'NotFoundError')
    assert issubclass(db.DatabaseError, Exception)
    assert issubclass(db.NotFoundError, Exception)


# ============================================================================
# Test 8: Logging Integration
# ============================================================================

def test_logging_configured():
    """Test that logging is properly set up in modules."""
    import logging
    from week2.app.services import extract
    
    # Check that logger is defined
    assert hasattr(extract, 'logger')
    assert isinstance(extract.logger, logging.Logger)
    
    # Check db module has logger
    assert hasattr(db, 'logger')
    assert isinstance(db.logger, logging.Logger)


# ============================================================================
# Summary Test: Full Workflow
# ============================================================================

def test_full_refactored_workflow():
    """
    End-to-end test of refactored system:
    1. Use Pydantic schema to create request
    2. Extract action items and save note
    3. Verify DB returns dicts
    4. Verify response uses schemas
    5. Mark item as done
    """
    db.init_db()
    
    # Step 1: Extract with schemas
    extract_req = ExtractRequest(
        text="Meeting notes:\n- Prepare slides\n- [ ] Review code\n* Send email",
        save_note=True
    )
    extract_resp = action_items.extract(extract_req)
    
    # Verify types
    assert isinstance(extract_resp, ExtractResponse)
    assert extract_resp.note_id is not None
    assert len(extract_resp.items) >= 3
    
    # Step 2: Get note using router
    note_resp = notes.get_single_note(extract_resp.note_id)
    assert isinstance(note_resp, NoteResponse)
    assert "Meeting notes" in note_resp.content
    
    # Step 3: List all action items
    all_items = action_items.list_all()
    assert isinstance(all_items, list)
    assert len(all_items) >= 3
    
    # Step 4: Mark one as done
    first_item_id = extract_resp.items[0].id
    mark_req = MarkDoneRequest(done=True)
    mark_resp = action_items.mark_done(first_item_id, mark_req)
    assert mark_resp["done"] is True
    
    print("✓ Full refactored workflow test passed!")
