# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
I need to implement extract_action_items_llm() in week2/app/services/extract.py.

Requirements:
1. Use Ollama API with llama3.1:8b model
2. Implement structured outputs using JSON schema to guarantee valid response format
3. System prompt should instruct the LLM to:
   - Extract actionable tasks from meeting notes
   - Ignore non-actionable content (greetings, context, statements)
   - Remove formatting markers (bullets, checkboxes, TODO: prefixes)
4. Handle edge cases: empty input, API errors, invalid responses
5. Post-process to deduplicate and clean whitespace
6. Add comprehensive debug logging for traceability
7. Use temperature=0.3 for more deterministic outputs

The function should have the same signature pattern as extract_action_items() but use LLM intelligence instead of regex heuristics.
``` 

Generated Code Snippets:
```
Modified file: week2/app/services/extract.py (lines 117-264)
- Added extract_action_items_llm() function with full implementation
- Includes system prompt engineering for task extraction
- JSON schema definition for structured outputs: { "action_items": ["item1", ...] }
- Ollama API integration with chat() function
- Error handling with graceful fallback to empty list
- Post-processing: whitespace cleaning, deduplication
- Extensive debug logging for observability

Test file created: week2/test_llm_manual.py
- 5 test cases covering: bullets, keywords, mixed format, empty input, no actions
- All tests passing with expected behavior
```

### Exercise 2: Add Unit Tests
Prompt: 
```
I need comprehensive unit tests for extract_action_items_llm() in week2/tests/test_extract.py.

Testing Strategy:
1. Use layered testing approach:
   - Unit tests (5 tests): Mock Ollama API, test function logic (fast, deterministic)
   - Integration tests (2 tests): Real LLM calls, test actual behavior (slow, semantic assertions)
   - Edge case tests (1 test): Boundary conditions (empty input, whitespace, no actions)

2. Unit tests should use @patch to mock the chat() function and test:
   - Successful JSON parsing and list extraction
   - Post-processing logic: whitespace cleaning, deduplication, empty string filtering
   - Error handling: API failures, invalid JSON responses
   - Parameter passing: custom model parameter

3. Integration tests should:
   - Use @pytest.mark.slow decorator
   - Make real Ollama API calls
   - Use semantic assertions (not exact string matching) due to LLM non-determinism
   - Test basic extraction from bullets/keywords
   - Test semantic understanding (distinguishing actionable vs descriptive text)

4. All tests should:
   - Have clear docstrings explaining what they test
   - Use descriptive assertion messages
   - Follow pytest best practices

5. Add pytest configuration to pyproject.toml to register 'slow' marker.
``` 

Generated Code Snippets:
```
Modified file: week2/tests/test_extract.py (lines 1-287)
- Import statement: from ..app.services.extract import extract_action_items, extract_action_items_llm
  (Uses relative imports, recommended best practice for package-internal code)
- Added import: unittest.mock.patch for mocking Ollama API calls
- Added import: pytest for test markers

Unit Tests (Mocked - Lines 26-135):
- test_llm_extract_mock_success: Tests normal JSON parsing and list extraction
- test_llm_extract_mock_post_processing: Tests whitespace cleaning, deduplication, empty filtering
- test_llm_extract_mock_api_error: Tests graceful error handling with side_effect
- test_llm_extract_mock_invalid_json: Tests handling of malformed JSON response
- test_llm_extract_mock_custom_model: Tests custom model parameter passing

Integration Tests (Real LLM - Lines 141-253):
- test_llm_extract_real_basic: Tests basic extraction with semantic assertions
- test_llm_extract_real_semantic_understanding: Tests LLM's ability to distinguish action vs description

Edge Case Tests (Lines 259-276):
- test_llm_extract_edge_cases: Tests empty input, whitespace-only, no action items

Modified file: pyproject.toml (lines 37-43)
- Added [tool.pytest.ini_options] section
- Registered 'slow' marker to avoid pytest warnings
- Configured test discovery paths and naming conventions

Learning Notes Created:
- learning_notes/week2/testing_llm_functions_guide.md
  Comprehensive guide on Mock, Pytest decorators, assertions, and LLM testing best practices
- learning_notes/week2/python_import_system_guide.md
  Deep dive into Python's import system, sys.path, absolute vs relative imports, and when to use each

Test Results:
- 7 fast tests (mocked + edge cases) pass in ~0.6-2.8 seconds
- 2 slow tests (real LLM) require Ollama running
- Can run fast tests only with: pytest -m "not slow"

Key Learning Points:
- Relative imports (from ..app...) are safer for package-internal code
- @patch decorator enables fast unit tests by mocking external dependencies
- Pytest automatically adds project root to sys.path, enabling imports to work
- Semantic assertions (checking keywords) are better than exact matching for LLM tests
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
I need to refactor the week2 FastAPI application to improve code quality and maintainability.

Refactoring Goals:
1. Add Pydantic schemas for all API contracts (requests/responses)
2. Change database layer to return dicts instead of sqlite3.Row for better decoupling
3. Add proper error handling with custom exceptions
4. Implement logging throughout the application
5. Add type safety and validation

Areas to refactor:
- app/schemas.py: Add all Pydantic models (NoteCreate, NoteResponse, ExtractRequest, ExtractResponse, ActionItemResponse, MarkDoneRequest)
- app/db.py: Wrap sqlite3 operations with error handling, return dicts instead of Row
- app/routers/: Update all endpoints to use schemas
- app/main.py: Add exception handlers for custom errors

The refactoring should maintain backward compatibility with existing functionality while improving code quality.
```

Generated/Modified Code Snippets:
```
Created file: week2/app/schemas.py (82 lines)
- NoteCreate: Request schema with content validation (min_length=1)
- NoteResponse: Response schema with id, content, created_at + from_dict() class method
- ActionItemResponse: Response schema with id, text, note_id, done, created_at + from_dict()
- ExtractRequest: Request schema for extraction (text, save_note with defaults)
- ExtractResponse: Response schema containing note_id and list of ActionItemResponse
- MarkDoneRequest: Request schema for marking items done/undone

Modified file: week2/app/db.py (243 lines)
- Added custom exceptions: DatabaseError (line 38), NotFoundError (line 59)
- Added logger configuration (line 30)
- Modified insert_note() (lines 122-135): Wrapped in try/except with DatabaseError handling
- Modified list_notes() (lines 138-151): Now returns list[dict] instead of list[sqlite3.Row]
- Modified get_note() (lines 154-173): Returns dict, raises NotFoundError if not found
- Modified insert_action_items() (lines 176-195): Added error handling with DatabaseError
- Modified list_action_items() (lines 198-219): Returns list[dict] with proper error handling
- Modified mark_action_item_done() (lines 222-240): Raises NotFoundError if item not found

Modified file: week2/app/main.py (47 lines)
- Added exception handlers for DatabaseError (lines 25-29) and NotFoundError (lines 31-38)
- Handlers return proper HTTP status codes (500 for DatabaseError, 404 for NotFoundError)
- Added structured logging configuration (lines 7-10)

Modified file: week2/app/routers/notes.py (36 lines)
- Updated create_note() to use NoteCreate/NoteResponse schemas (lines 15-20)
- Added list_notes() endpoint using NoteResponse schema (lines 24-28)
- Updated get_single_note() to use NoteResponse schema (lines 31-35)

Modified file: week2/app/routers/action_items.py (97 lines)
- Updated extract() to use ExtractRequest/ExtractResponse schemas (lines 15-30)
- Added extract_llm() endpoint with LLM integration (lines 33-57)
- Updated mark_done() to use MarkDoneRequest schema (lines 60-75)
- Added list_all() endpoint returning ActionItemResponse list (lines 78-87)

Created file: week2/tests/test_refactoring.py (334 lines)
- 17 comprehensive tests validating all refactoring improvements
- Tests for schema validation, database dict returns, error handling, router integration
- Full workflow end-to-end test

Test Results:
- All 17 refactoring tests passing in ~0.19 seconds
- All existing functionality preserved with improved type safety
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```
I need to complete TODO 4 in the week2 assignment: Use Agentic Mode to add a "List Notes" feature.

Requirements:
1. Add a GET /notes endpoint to app/routers/notes.py that lists all notes
2. Add a "List Notes" button to the frontend (frontend/index.html)
3. Implement JavaScript to fetch and display notes when the button is clicked

The endpoint should:
- Use the existing db.list_notes() function
- Return NoteResponse objects with proper typing
- Order notes by ID descending (newest first)

The frontend should:
- Add a button next to the existing "Extract" buttons
- Display notes in a readable format with ID, timestamp, and content
- Handle empty state when no notes exist
- Handle errors gracefully
```

Generated Code Snippets:
```
Modified file: week2/app/routers/notes.py (lines 24-28)
- Added list_notes() endpoint with @router.get("", response_model=List[NoteResponse])
- Uses existing db.list_notes() function
- Returns list of NoteResponse objects ordered by ID descending

Modified file: week2/frontend/index.html (lines 28, 76-102)
- Added "List Notes" button in the button row (line 28)
- Added btnListNotes reference (line 76)
- Added click event listener with async fetch to /notes endpoint (lines 82-102)
- Displays notes with ID, timestamp, and content in styled cards
- Handles empty state with "No notes found" message
- Handles errors with "Error loading notes" message
```


### Exercise 5: Generate a README from the Codebase
Prompt:
```
Generate a comprehensive README.md for the week2 Action Item Extractor application.

The README should include:
1. Project title and brief description
2. Features overview (rules-based extraction, LLM extraction, notes management)
3. Tech stack (FastAPI, SQLite, Ollama, Pydantic)
4. Project structure/directory layout
5. Setup and installation instructions
6. Usage examples (API endpoints, frontend UI)
7. Running tests
8. Configuration (Ollama setup, model requirements)

Make it clear, well-organized, and suitable for someone new to the project.
```

Generated Code Snippets:
```
Created file: week2/README.md
- Complete project documentation with all required sections
- Includes setup instructions, API documentation, testing guide
- See week2/README.md for full content
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 