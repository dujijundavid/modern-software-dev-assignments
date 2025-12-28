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

@pytest.mark.slow
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


# ============================================================================
# EDGE CASE TESTS: _is_action_line filtering logic (Lines 29, 44, 52, 56, 61)
# ============================================================================

from week2.app.services.extract import _is_action_line, _looks_imperative


@pytest.mark.parametrize("line,expected", [
    ("", False),                           # Empty line (line 29)
    ("   ", False),                        # Whitespace only
    ("\t\n", False),                       # Tab and newline
    ("- a", False),                        # Too short (< 3 chars after strip, line 44)
    ("* ab", False),                       # Too short
    ("1. x", False),                       # Too short
    ("TODO:", True),                       # Has format indicator and >= 3 chars
    ("[ ]", False),                        # Checkbox with no content
])
def test_is_action_line_filters_short_lines(line, expected):
    """Test that _is_action_line filters out very short lines (line 44)."""
    assert _is_action_line(line) == expected


@pytest.mark.parametrize("line,expected", [
    ("- Is this a bug?", False),           # Question ending (line 52)
    ("- Should we fix it?", False),        # Question ending
    ("ACTION: What about testing?", False), # Question with keyword
    ("* Can we deploy?", False),           # Question with asterisk
    ("TODO: Review this?", False),         # Question after TODO
])
def test_is_action_line_filters_questions(line, expected):
    """Test that _is_action_line filters out questions (line 52)."""
    assert _is_action_line(line) == expected


@pytest.mark.parametrize("line,expected", [
    ("- aaa", False),                      # Too few unique chars (line 56)
    ("* ???", False),                      # Only symbols
    ("1. xxxxx", False),                   # Repeated chars
    ("- abcdef", True),                    # Valid unique chars
    ("* test", True),                      # Valid content
])
def test_is_action_line_filters_gibberish(line, expected):
    """Test that _is_action_line filters out gibberish with < 3 unique chars (line 56)."""
    assert _is_action_line(line) == expected


@pytest.mark.parametrize("line,expected", [
    ("- @#$%^&", False),                   # Mostly symbols (line 61)
    ("* !@#$ test", False),                # High symbol ratio
    ("1. ++++", False),                    # Only symbols
    ("- valid text", True),                # Valid alpha content
    ("* mix3d w0rds", True),               # Mixed alphanumeric
    ("- normal task description", True),   # Normal content
])
def test_is_action_line_filters_symbol_heavy(line, expected):
    """Test that _is_action_line filters lines with < 50% alpha chars (line 61)."""
    assert _is_action_line(line) == expected


@pytest.mark.parametrize("line,expected", [
    ("Valid action item", False),          # No format indicator
    ("- Valid action item", True),         # Has bullet
    ("* Valid action item", True),         # Has asterisk
    ("TODO: Valid action item", True),     # Has TODO prefix
    ("1. Valid action item", True),        # Has number prefix
    ("[ ] Valid action item", True),       # Has checkbox
])
def test_is_action_line_requires_format_indicator(line, expected):
    """Test that _is_action_line requires some format indicator."""
    assert _is_action_line(line) == expected


# ============================================================================
# EDGE CASE TESTS: Empty line skipping in main loop (Lines 82-83)
# ============================================================================

def test_extract_action_items_skips_empty_lines():
    """Test that empty lines are skipped in the main loop (lines 82-83)."""
    text = """
    - Task 1

    * Task 2


    1. Task 3
    """
    items = extract_action_items(text)
    assert len(items) == 3
    assert "Task 1" in items
    assert "Task 2" in items
    assert "Task 3" in items


def test_extract_action_items_handles_whitespace_only_lines():
    """Test that whitespace-only lines are handled correctly."""
    text = "- Task 1\n   \n\t \n- Task 2"
    items = extract_action_items(text)
    assert len(items) == 2


# ============================================================================
# EDGE CASE TESTS: Imperative fallback logic (Lines 101-114)
# ============================================================================

def test_extract_action_items_fallback_to_imperative():
    """Test fallback logic when pattern matching fails (lines 101-114)."""
    # Text without bullet patterns but with imperative sentences
    text = "Fix the bug. Create a new feature. Write tests."
    items = extract_action_items(text)

    # Should extract imperative sentences via fallback
    assert "Fix the bug" in items or "Fix the bug." in items
    assert "Create a new feature" in items or "Create a new feature." in items
    assert "Write tests" in items or "Write tests." in items


def test_extract_action_items_fallback_ignores_non_imperative():
    """Test that fallback ignores non-imperative sentences."""
    text = "The meeting was productive. We should improve performance."
    items = extract_action_items(text)

    # Should not extract non-imperative sentences
    assert len(items) == 0 or all("productive" not in item.lower() for item in items)


def test_extract_action_items_fallback_with_mixed_content():
    """Test fallback with mix of imperative and non-imperative sentences."""
    text = "The bug needs fixing. Fix the authentication issue. Consider refactoring."
    items = extract_action_items(text)

    # Should extract imperative sentences
    assert any("fix" in item.lower() and "authentication" in item.lower() for item in items)


# ============================================================================
# EDGE CASE TESTS: Deduplication behavior (Lines 124-125)
# ============================================================================

def test_extract_action_items_deduplicates_case_insensitive():
    """Test that deduplication is case-insensitive."""
    text = """
    - Fix the bug
    * FIX THE BUG
    1. fix the bug
    """
    items = extract_action_items(text)

    # Should deduplicate case-insensitively
    assert len(items) == 1
    assert "Fix the bug" in items


def test_extract_action_items_preserves_order_on_dedup():
    """Test that order is preserved during deduplication."""
    text = """
    - Task B
    - Task A
    - Task B
    * Task C
    - Task A
    """
    items = extract_action_items(text)

    # Should preserve first occurrence order
    assert items == ["Task B", "Task A", "Task C"]


# ============================================================================
# EDGE CASE TESTS: _looks_imperative function (Lines 136-155)
# ============================================================================

@pytest.mark.parametrize("sentence,expected", [
    ("Fix the bug", True),                 # Starts with imperative verb
    ("Create a new feature", True),
    ("Implement the API", True),
    ("Write tests", True),
    ("Refactor the code", True),
    ("Add logging", True),
    ("Update documentation", True),
    ("Check the configuration", True),
    ("Verify the fix", True),
    ("The bug needs fixing", False),       # Not imperative
    ("We should fix it", False),           # Not imperative
    ("The meeting was productive", False), # Not imperative
    ("", False),                           # Empty
    ("???", False),                        # No words
    ("123 numbers", False),                # Starts with number
    ("fixing the bug", False),             # Gerund, not imperative
])
def test_looks_imperative(sentence, expected):
    """Test imperative sentence detection (lines 136-155)."""
    assert _looks_imperative(sentence) == expected


def test_looks_imperative_case_insensitive():
    """Test that _looks_imperative is case-insensitive."""
    assert _looks_imperative("Fix the bug") is True
    assert _looks_imperative("fix the bug") is True
    assert _looks_imperative("FIX THE BUG") is True


# ============================================================================
# EDGE CASE TESTS: Type validation for LLM responses (Lines 263-264)
# ============================================================================

@patch('week2.app.services.extract.chat')
def test_llm_extract_type_validation_invalid_items(mock_chat):
    """Test type validation when LLM returns non-string items (lines 263-264)."""
    # Mock LLM returns invalid types
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": [123, null, ["array"]]}'
        }
    }

    result = extract_action_items_llm("test input")
    assert result == [], "Should return empty list for non-string items"


@patch('week2.app.services.extract.chat')
def test_llm_extract_type_validation_not_a_list(mock_chat):
    """Test type validation when action_items is not a list (lines 263-264)."""
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": "not a list"}'
        }
    }

    result = extract_action_items_llm("test input")
    assert result == [], "Should return empty list for non-list"


@patch('week2.app.services.extract.chat')
def test_llm_extract_type_validation_missing_key(mock_chat):
    """Test type validation when action_items key is missing."""
    mock_chat.return_value = {
        "message": {
            "content": '{"wrong_key": ["item1", "item2"]}'
        }
    }

    result = extract_action_items_llm("test input")
    # Should handle gracefully - either empty list or default
    assert isinstance(result, list)


# ============================================================================
# EDGE CASE TESTS: Vague single-word filtering (Lines 279-280)
# ============================================================================

@patch('week2.app.services.extract.chat')
def test_llm_extract_filters_vague_single_words(mock_chat):
    """Test filtering of vague single-word items (lines 279-280)."""
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["fix", "help", "do", "Implement feature"]}'
        }
    }

    result = extract_action_items_llm("test input")

    # Should filter short vague words but keep substantive ones
    assert "Implement feature" in result
    assert "fix" not in result, "Should filter 'fix' (single short word)"
    assert "help" not in result, "Should filter 'help' (single short word)"
    assert "do" not in result, "Should filter 'do' (single short word)"


@patch('week2.app.services.extract.chat')
def test_llm_extract_keeps_substantive_single_words(mock_chat):
    """Test that substantive single words are kept (lines 279-280)."""
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["investigation", "refactoring", "implementation"]}'
        }
    }

    result = extract_action_items_llm("test input")

    # Words >= 6 chars should be kept
    assert len(result) == 3
    assert "investigation" in result
    assert "refactoring" in result
    assert "implementation" in result


@patch('week2.app.services.extract.chat')
def test_llm_extract_filters_empty_strings(mock_chat):
    """Test that empty strings are filtered out."""
    mock_chat.return_value = {
        "message": {
            "content": '{"action_items": ["Valid task", "", "  ", "Another task"]}'
        }
    }

    result = extract_action_items_llm("test input")

    assert len(result) == 2
    assert "Valid task" in result
    assert "Another task" in result
