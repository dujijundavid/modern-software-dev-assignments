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
Modified file: week2/tests/test_extract.py (lines 1-283)
- Added import: unittest.mock.patch for mocking
- Added import: extract_action_items_llm to test new function

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
- Registered 'slow' marker to avoid warnings
- Configured test discovery paths

Test Results:
- 6 fast tests (mocked + edge cases) pass in <1 second
- 2 slow tests (real LLM) require Ollama running
- Can run fast tests only with: pytest -m "not slow"
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
TODO
``` 

Generated/Modified Code Snippets:
```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
TODO
``` 

Generated Code Snippets:
```
TODO: List all modified code files with the relevant line numbers.
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 