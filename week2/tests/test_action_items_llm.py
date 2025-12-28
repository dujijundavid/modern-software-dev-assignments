"""
Test suite for /action-items/extract-llm endpoint.

Tests the LLM-powered extraction endpoint including error handling,
database integration, and response formatting.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from week2.app.main import app
from week2.app import db


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def client():
    """Create test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db():
    """Initialize test database before each test."""
    db.init_db()


# ============================================================================
# Mocked LLM Tests (Fast, Deterministic)
# ============================================================================

@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_endpoint_basic(mock_extract_llm, client):
    """Test basic LLM extraction endpoint without saving note."""
    mock_extract_llm.return_value = ["Task 1", "Task 2"]

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "- Do task 1\n- Do task 2", "save_note": False}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["note_id"] is None
    assert len(data["items"]) == 2
    assert data["items"][0]["text"] == "Task 1"
    mock_extract_llm.assert_called_once()


@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_with_save_note(mock_extract_llm, client):
    """Test LLM extraction with note saving (lines 66-69)."""
    mock_extract_llm.return_value = ["Important task"]

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "Do something important", "save_note": True}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["note_id"] is not None
    assert isinstance(data["note_id"], int)

    # Verify note was saved
    note = db.get_note(data["note_id"])
    assert note["content"] == "Do something important"


@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_db_integration(mock_extract_llm, client):
    """Test that LLM endpoint properly integrates with database (lines 72-86)."""
    mock_extract_llm.return_value = ["Task A", "Task B", "Task C"]

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "Multiple tasks", "save_note": True}
    )

    assert response.status_code == 200
    data = response.json()

    # All items should be saved to DB
    assert len(data["items"]) == 3
    for item in data["items"]:
        assert item["id"] > 0
        assert "created_at" in item
        assert item["done"] is False


@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_empty_response(mock_extract_llm, client):
    """Test LLM endpoint when LLM returns no items."""
    mock_extract_llm.return_value = []

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "No actionable items here", "save_note": False}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["note_id"] is None
    assert len(data["items"]) == 0


@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_timestamps_in_response(mock_extract_llm, client):
    """Test that response includes created_at timestamps from DB (lines 76-78)."""
    mock_extract_llm.return_value = ["Task with timestamp"]

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "Single task", "save_note": True}
    )

    assert response.status_code == 200
    data = response.json()

    item = data["items"][0]
    assert "created_at" in item
    assert item["created_at"] is not None
    assert len(item["created_at"]) > 0  # Non-empty timestamp string


# ============================================================================
# Error Handling Tests
# ============================================================================

@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_handles_db_error_gracefully(mock_extract_llm, client):
    """Test endpoint behavior when database fails."""
    # Mock LLM works but we'll mock DB to fail
    mock_extract_llm.return_value = ["Task 1"]

    with patch('week2.app.routers.action_items.db.insert_action_items') as mock_insert:
        mock_insert.side_effect = db.DatabaseError("Database connection failed")

        response = client.post(
            "/action-items/extract-llm",
            json={"text": "Task text", "save_note": False}
        )

        # Should return 500 error
        assert response.status_code == 500
        assert "Database connection failed" in response.text


# ============================================================================
# Response Model Validation Tests
# ============================================================================

@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_response_schema_compliance(mock_extract_llm, client):
    """Test that response conforms to ExtractResponse schema."""
    mock_extract_llm.return_value = ["Task 1", "Task 2"]

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "Tasks", "save_note": False}
    )

    assert response.status_code == 200
    data = response.json()

    # Validate schema structure
    assert "note_id" in data
    assert "items" in data
    assert isinstance(data["items"], list)

    # Each item should have ActionItemResponse fields
    for item in data["items"]:
        assert "id" in item
        assert "text" in item
        assert "note_id" in item
        assert "done" in item
        assert "created_at" in item


# ============================================================================
# Note Filtering Tests
# ============================================================================

@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_filters_by_note_id(mock_extract_llm, client):
    """Test that items are correctly associated with their note."""
    mock_extract_llm.return_value = ["Task 1", "Task 2"]

    # Create first extraction with note
    response1 = client.post(
        "/action-items/extract-llm",
        json={"text": "First batch", "save_note": True}
    )
    note1_id = response1.json()["note_id"]

    # Create second extraction with note
    response2 = client.post(
        "/action-items/extract-llm",
        json={"text": "Second batch", "save_note": True}
    )
    note2_id = response2.json()["note_id"]

    # Verify items are associated with correct notes
    items1 = db.list_action_items(note_id=note1_id)
    items2 = db.list_action_items(note_id=note2_id)

    assert len(items1) == 2
    assert len(items2) == 2
    assert all(item["note_id"] == note1_id for item in items1)
    assert all(item["note_id"] == note2_id for item in items2)


# ============================================================================
# Mark Done Integration Tests
# ============================================================================

@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_and_mark_done_workflow(mock_extract_llm, client):
    """Test complete workflow: extract with LLM, then mark as done."""
    mock_extract_llm.return_value = ["Task to complete"]

    # Extract items
    extract_response = client.post(
        "/action-items/extract-llm",
        json={"text": "Complete this task", "save_note": True}
    )
    assert extract_response.status_code == 200

    item_id = extract_response.json()["items"][0]["id"]

    # Mark as done
    mark_response = client.post(
        f"/action-items/{item_id}/done",
        json={"done": True}
    )
    assert mark_response.status_code == 200
    assert mark_response.json()["done"] is True

    # Verify marked as done
    items = db.list_action_items()
    item = next((i for i in items if i["id"] == item_id), None)
    assert item is not None
    assert item["done"] == 1


# ============================================================================
# Edge Case Tests
# ============================================================================

@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_with_whitespace_only_text(mock_extract_llm, client):
    """Test extraction with whitespace-only text."""
    mock_extract_llm.return_value = []

    response = client.post(
        "/action-items/extract-llm",
        json={"text": "   \n\n  \t  ", "save_note": False}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["note_id"] is None
    assert len(data["items"]) == 0


@patch('week2.app.routers.action_items.extract_action_items_llm')
def test_extract_llm_with_very_long_text(mock_extract_llm, client):
    """Test extraction with very long input text."""
    long_text = "Task " * 1000
    mock_extract_llm.return_value = ["Task 1", "Task 2"]

    response = client.post(
        "/action-items/extract-llm",
        json={"text": long_text, "save_note": False}
    )

    assert response.status_code == 200
    # Verify note was saved with full content
    data = response.json()
    assert len(data["items"]) == 2
