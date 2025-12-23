import os
import pytest
from unittest.mock import patch

from ..app.services.extract import extract_action_items, extract_action_items_llm


# ============================================================================
# EXISTING TEST: Heuristic-based extraction
# ============================================================================
def test_extract_bullets_and_checkboxes():
    """Test original heuristic-based extraction with bullets and checkboxes."""
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ============================================================================
# UNIT TESTS (MOCKED): Fast, deterministic, test logic not LLM
# ============================================================================

@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_success(mock_chat):
    """
    Test that the function correctly parses a valid LLM response.
    
    This tests:
    - JSON parsing logic
    - List extraction from 'action_items' key
    - Basic return type
    """
    # Arrange: Mock LLM to return valid JSON
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["Fix bug #123", "Write unit tests"]}'
        }
    }
    
    # Act: Call function with any input (doesn't matter, LLM is mocked)
    result = extract_action_items_llm("Meeting notes: - Fix bug\n- Write tests")
    
    # Assert: Verify correct parsing
    assert isinstance(result, list), "Result should be a list"
    assert len(result) == 2, f"Expected 2 items, got {len(result)}"
    assert result == ["Fix bug #123", "Write unit tests"]
    
    # Verify LLM was called once
    mock_chat.assert_called_once()


@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_post_processing(mock_chat):
    """
    Test post-processing logic: whitespace cleaning, deduplication, empty filtering.
    
    This tests:
    - Leading/trailing whitespace removal
    - Case-insensitive deduplication
    - Empty string filtering
    """
    # Arrange: Mock LLM returns messy data
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["  Fix bug  ", "fix bug", "", "Write tests", "  "]}'
        }
    }
    
    # Act
    result = extract_action_items_llm("test input")
    
    # Assert: Should deduplicate and clean
    assert len(result) == 2, f"Expected 2 unique items after dedup, got {len(result)}: {result}"
    assert "Fix bug" in result, "Should keep first occurrence with cleaned whitespace"
    assert "Write tests" in result
    assert "" not in result, "Empty strings should be filtered"
    
    # Verify no leading/trailing whitespace
    for item in result:
        assert item == item.strip(), f"Item '{item}' has leading/trailing whitespace"


@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_api_error(mock_chat):
    """
    Test graceful error handling when Ollama API fails.
    
    This tests:
    - Exception handling
    - Graceful degradation (returns empty list, not crash)
    """
    # Arrange: Mock LLM to raise exception (simulating network error, Ollama down, etc.)
    mock_chat.side_effect = Exception("Connection refused: Ollama service not running")
    
    # Act: Should not crash
    result = extract_action_items_llm("test input")
    
    # Assert: Returns empty list gracefully
    assert result == [], f"Expected empty list on error, got {result}"
    assert isinstance(result, list), "Should still return a list type"


@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_invalid_json(mock_chat):
    """
    Test handling of invalid JSON response from LLM.
    
    This tests:
    - JSON parsing error handling
    - Graceful fallback when LLM returns malformed data
    """
    # Arrange: Mock LLM returns invalid JSON
    mock_chat.return_value = {
        "message": {
            "content": 'This is not valid JSON at all!'
        }
    }
    
    # Act: Should handle JSON decode error
    result = extract_action_items_llm("test input")
    
    # Assert: Returns empty list (graceful degradation)
    assert result == [], f"Expected empty list for invalid JSON, got {result}"


@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_custom_model(mock_chat):
    """
    Test that custom model parameter is correctly passed to Ollama API.
    
    This tests:
    - Parameter passing
    - Function signature flexibility
    """
    # Arrange: Mock LLM
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["Task 1"]}'
        }
    }
    
    # Act: Call with custom model
    custom_model = "mistral-nemo:12b"
    result = extract_action_items_llm("test input", model=custom_model)
    
    # Assert: Verify model parameter was passed correctly
    mock_chat.assert_called_once()
    call_kwargs = mock_chat.call_args[1]  # Get keyword arguments
    assert call_kwargs['model'] == custom_model, f"Expected model '{custom_model}', got '{call_kwargs['model']}'"
    
    # Verify function still works
    assert isinstance(result, list)


# ============================================================================
# INTEGRATION TESTS (REAL LLM): Slow, validates actual Ollama integration
# ============================================================================

@pytest.mark.slow
def test_llm_extract_real_basic():
    """
    Integration test with real LLM: Test basic extraction from bullets and keywords.
    
    NOTE: This test calls real Ollama API (slow, requires Ollama running).
    Use semantic assertions (not exact string matching) due to LLM non-determinism.
    """
    # Arrange: Input with clear action items
    text = """
    Project meeting notes:
    - Fix bug #123 in authentication module
    * Implement new API endpoint for user profiles
    TODO: Review pull requests by end of week
    action: Deploy changes to staging environment
    """
    
    # Act: Call real LLM
    result = extract_action_items_llm(text)
    
    # Assert: Semantic checks (not exact matches)
    assert isinstance(result, list), "Result should be a list"
    assert len(result) >= 3, f"Expected at least 3 action items, got {len(result)}: {result}"
    
    # Check that key concepts are captured (flexible matching)
    result_lower = [item.lower() for item in result]
    result_text = " ".join(result_lower)
    
    assert any("bug" in item and "123" in item for item in result_lower), \
        f"Should extract bug fix task. Got: {result}"
    assert any("api" in item or "endpoint" in item for item in result_lower), \
        f"Should extract API endpoint task. Got: {result}"
    assert any("review" in item and "pull" in item for item in result_lower), \
        f"Should extract PR review task. Got: {result}"
    
    # Verify all items are non-empty strings
    assert all(isinstance(item, str) and len(item.strip()) > 0 for item in result), \
        "All items should be non-empty strings"
    
    # Verify no formatting markers remain
    for item in result:
        assert not item.strip().startswith('-'), f"Item '{item}' still has bullet marker"
        assert not item.strip().startswith('*'), f"Item '{item}' still has asterisk marker"
        assert 'TODO:' not in item.upper(), f"Item '{item}' still has TODO prefix"


@pytest.mark.slow
def test_llm_extract_real_semantic_understanding():
    """
    Integration test: Verify LLM's semantic understanding (distinguishing action vs description).
    
    This tests the LLM's ability to identify actionable items from narrative text,
    which regex-based approaches cannot do.
    """
    # Arrange: Mix of actionable and descriptive content
    text = """
    The meeting was very productive. Everyone agreed on the timeline.
    We need to optimize the database queries for better performance.
    The current implementation is too slow.
    Consider migrating to a microservices architecture.
    Performance benchmarks showed a 30% improvement.
    """
    
    # Act: Call real LLM
    result = extract_action_items_llm(text)
    
    # Assert: Should extract actionable items, ignore descriptions
    assert isinstance(result, list), "Result should be a list"
    
    # Should extract at least the actionable items
    result_text = " ".join([item.lower() for item in result])
    
    # Check for actionable content
    assert any("optimize" in item.lower() or "database" in item.lower() for item in result), \
        f"Should extract database optimization task. Got: {result}"
    assert any("migrat" in item.lower() or "microservice" in item.lower() for item in result), \
        f"Should extract migration consideration. Got: {result}"
    
    # Should NOT extract purely descriptive statements (though LLM might interpret liberally)
    # We test that it's thoughtful, not that it extracts random descriptions
    assert all(len(item.strip()) > 10 for item in result), \
        "Action items should be substantial (not just 'good' or 'meeting')"


# ============================================================================
# EDGE CASE TESTS: Fast, cover boundary conditions
# ============================================================================

def test_llm_extract_edge_cases():
    """
    Test edge cases: empty input, whitespace-only, no action items.
    
    Combined test for efficiency (all edge cases are fast).
    """
    # Test 1: Empty string
    result_empty = extract_action_items_llm("")
    assert result_empty == [], f"Empty input should return empty list, got {result_empty}"
    
    # Test 2: Whitespace only
    result_whitespace = extract_action_items_llm("   \n\n  \t  ")
    assert result_whitespace == [], f"Whitespace-only input should return empty list, got {result_whitespace}"
    
    # Test 3: Text with no actionable items (this might call real LLM, but should be fast)
    # Note: Depending on implementation, this might need @patch to be fast
    # For now, we test with simple descriptive text
    result_no_action = extract_action_items_llm("The weather is nice today.")
    assert isinstance(result_no_action, list), "Should return a list even with no action items"
    # LLM might or might not extract anything - we just verify it doesn't crash
    assert all(isinstance(item, str) for item in result_no_action), \
        "All returned items should be strings"


# ============================================================================
# CONFIGURATION: Pytest markers
# ============================================================================
# Add this to pytest.ini or pyproject.toml:
# [tool.pytest.ini_options]
# markers = [
#     "slow: marks tests as slow (deselect with '-m \"not slow\"')",
# ]
