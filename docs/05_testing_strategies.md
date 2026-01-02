# Testing Strategies: From Pyramid to E2E

> **Navigation**: [CS146S Docs](./INDEX.md) > Testing Strategies

## Quick Reference

**Testing Philosophy**: Tests should be **fast**, **reliable**, and **maintainable**. Use the testing pyramid to balance coverage with development speed.

**Core Principles**:
- 70% Unit Tests (Mock external dependencies, milliseconds)
- 20% Integration Tests (Real dependencies, seconds)
- 10% E2E Tests (Full workflows, tens of seconds)

**Key Commands**:
```bash
# Run fast tests during development
pytest weekN/tests/ -m "not slow"

# Run all tests before commit
pytest weekN/tests/

# With coverage
pytest weekN/tests/ --cov=weekN/app --cov-report=html

# Run specific test
pytest weekN/tests/test_file.py::test_function
```

---

## Testing Pyramid

### Visual Representation

```
              /\
             /  \
            / E2E \          ← Full user workflows (10%, slowest)
           /-------\
          / Integration \     ← API + Service integration (20%, slower)
         /---------------\
        /     Unit Tests   \  ← Individual functions (70%, fastest)
       /---------------------\
      Fast, Isolated, Deterministic
```

### Why This Distribution?

| Test Type | Quantity | Speed | Purpose | Example |
|-----------|----------|-------|---------|---------|
| **Unit** | 70% | ~50ms | Test business logic in isolation | Mock LLM response parsing |
| **Integration** | 20% | ~2-3s | Verify real dependencies work | Real LLM extraction test |
| **E2E** | 10% | ~30s | Validate complete workflows | Create note → Extract items → Mark done |

**Week 2 Benchmark**:
- Without Mocks: 7 tests in 21 seconds (3s per test)
- With Mocks: 7 tests in 0.35 seconds (0.05s per test)
- **Speedup: 60x faster**

### When to Use Each Layer

```
Unit Tests: When you want to test YOUR logic, not external services
Integration Tests: When you need confidence in real integrations
E2E Tests: When you must validate critical user journeys
```

---

## LLM Application Testing

### Challenge: Non-Deterministic Output

LLMs produce different outputs for the same input, making traditional exact-match assertions unreliable.

**Problem**:
```python
# ❌ Bad: Exact match fails 30% of the time
assert result == ["Fix bug #123", "Write unit tests"]
# LLM might return: ["Fix bug 123", "Write tests", "Unit tests"]
```

**Solution**: Semantic assertions + JSON Schema constraints

### Strategy 1: Structured Output

Use JSON Schema to guarantee parseable responses from LLMs.

```python
def extract_action_items_llm(text: str, model: str = "llama3.1:8b") -> List[str]:
    """Extract action items using LLM with structured output."""

    json_schema = {
        'type': 'object',
        'properties': {
            'action_items': {
                'type': 'array',
                'items': {'type': 'string'}
            }
        },
        'required': ['action_items']
    }

    response = chat(
        model=model,
        messages=[
            {"role": "system", "content": "Extract action items..."},
            {"role": "user", "content": text}
        ],
        format='json',  # ← Enforces JSON Schema
        options={'temperature': 0.1}  # ← Low temperature for consistency
    )

    # Parse and validate
    data = json.loads(response['message']['content'])
    items = data.get('action_items', [])

    return _post_process_items(items)
```

**Benefits**:
- 95% reduction in parsing errors
- Guaranteed valid JSON structure
- Type-safe validation

### Strategy 2: Mock for Unit Tests

Mock external LLM API to test your parsing logic, not the LLM itself.

```python
from unittest.mock import patch

@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_success(mock_chat):
    """Test JSON parsing and list extraction logic."""

    # Arrange: Mock LLM response
    mock_chat.return_value = {
        'message': {
            'content': '{"action_items": ["Fix bug", "Write tests"]}'
        }
    }

    # Act: Call function
    result = extract_action_items_llm("test input")

    # Assert: Verify parsing logic
    assert result == ["Fix bug", "Write tests"]
    mock_chat.assert_called_once()  # Verify LLM was called
```

**What this tests**:
- ✅ JSON parsing logic
- ✅ List extraction from response
- ✅ Post-processing (deduplication, whitespace cleanup)
- ❌ NOT testing LLM quality (that's Ollama's responsibility)

### Strategy 3: Semantic Assertions for Real LLM Tests

When testing with real LLM, use flexible assertions that check meaning, not exact wording.

```python
@pytest.mark.slow
def test_llm_extract_real_basic():
    """Integration test with real LLM."""

    text = """
    Meeting notes:
    - Fix bug #123 in authentication
    * Implement API endpoint for users
    """

    result = extract_action_items_llm(text)

    # ❌ Bad: Exact match (fragile)
    # assert result == ["Fix bug #123", "Implement API endpoint"]

    # ✅ Good: Semantic checks
    assert len(result) >= 2, "Should extract at least 2 items"

    # Check keywords (case-insensitive)
    result_lower = [item.lower() for item in result]
    assert any("bug" in item and "123" in item for item in result_lower)
    assert any("api" in item or "endpoint" in item for item in result_lower)

    # Verify no formatting markers remain
    for item in result:
        assert not item.startswith('-'), f"Item has bullet: {item}"
        assert 'TODO:' not in item.upper()
```

**Semantic Assertion Patterns**:

```python
# Pattern 1: Check length range
assert 2 <= len(result) <= 5

# Pattern 2: Keyword matching (case-insensitive)
assert any("bug" in item.lower() for item in result)

# Pattern 3: Type validation
assert all(isinstance(item, str) for item in result)

# Pattern 4: Substring presence
result_text = " ".join(result).lower()
assert "database" in result_text and "optimization" in result_text

# Pattern 5: Negative assertions (what should NOT be there)
assert not any(item.startswith('-') for item in result)
```

### Strategy 4: Post-Processing Validation

Test data cleaning logic separately from LLM integration.

```python
@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_post_processing(mock_chat):
    """Test deduplication, whitespace cleanup, empty filtering."""

    # Mock returns messy data
    mock_chat.return_value = {
        'message': {
            'content': '{"action_items": ["  Fix bug  ", "fix bug", "", "  "]}'
        }
    }

    result = extract_action_items_llm("test")

    # Verify post-processing
    assert len(result) == 1, "Should deduplicate case-insensitively"
    assert "Fix bug" in result, "Should clean whitespace"
    assert "" not in result, "Should filter empty strings"

    # Verify no whitespace issues
    for item in result:
        assert item == item.strip()
```

### Strategy 5: Error Handling

Test graceful degradation when LLM fails.

```python
@patch('week2.app.services.extract.chat')
def test_llm_extract_mock_api_error(mock_chat):
    """Test graceful error handling."""

    # Simulate API failure
    mock_chat.side_effect = Exception("Ollama service not running")

    # Should not crash
    result = extract_action_items_llm("test input")

    # Should return empty list, not raise exception
    assert result == [], "Should degrade gracefully"
    assert isinstance(result, list)
```

**Error Scenarios to Test**:
- Network timeout
- Invalid JSON response
- Missing required keys
- Wrong data types (array vs string)
- Service unavailable

### Strategy 6: Edge Case Testing

Test boundary conditions with parametrized tests.

```python
@pytest.mark.parametrize("line,expected", [
    ("", False),                           # Empty
    ("   ", False),                        # Whitespace only
    ("- a", False),                        # Too short (< 3 chars)
    ("TODO:", True),                       # Has format indicator
    ("[ ]", False),                        # Checkbox with no content
    ("- Is this a bug?", False),           # Question ending
    ("- @#$%^&", False),                   # Mostly symbols
])
def test_is_action_line_filters(line, expected):
    """Test action line detection logic."""
    assert _is_action_line(line) == expected
```

---

## MCP Server Testing

### Challenge: Testing STDIO Communication

MCP servers use STDIO transport, making traditional HTTP testing insufficient.

**Architecture**:
```
Test Script → ClientSession → stdio_client → MCP Server → External API
```

### Strategy 1: Async Session Testing

Use `mcp.ClientSession` to test tools through real protocol communication.

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_weather_server():
    """Test MCP server tools via STDIO transport."""

    # Configure server parameters
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "weather.py"],
        env=None
    )

    # Create STDIO client
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Test tool call
            result = await session.call_tool(
                "get_alerts",
                arguments={"state": "CA"}
            )

            # Validate response
            assert result.content[0].text is not None
            print(f"Result: {result.content[0].text[:200]}...")

if __name__ == "__main__":
    asyncio.run(test_weather_server())
```

**What this tests**:
- ✅ STDIO transport communication
- ✅ JSON-RPC protocol handling
- ✅ Tool registration and discovery
- ✅ Argument serialization/deserialization
- ✅ Real API integration (weather.gov)

### Strategy 2: Tool Response Validation

Validate that MCP tools return proper data structures.

```python
async def test_tool_response_structure():
    """Test that tool responses match expected schema."""

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_forecast",
                arguments={"latitude": 37.7749, "longitude": -122.4194}
            )

            # Validate response structure
            assert hasattr(result, 'content')
            assert len(result.content) > 0

            # Check content type
            content = result.content[0]
            assert hasattr(content, 'text')
            assert isinstance(content.text, str)

            # Validate JSON parsing (if applicable)
            data = json.loads(content.text)
            assert 'temperature' in data or 'forecast' in data
```

### Strategy 3: Error Handling

Test tool behavior with invalid inputs.

```python
async def test_tool_error_handling():
    """Test tool error handling with invalid inputs."""

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Test with invalid coordinates
            try:
                result = await session.call_tool(
                    "get_forecast",
                    arguments={"latitude": 999, "longitude": 999}
                )
                # Should return error, not raise exception
                assert "error" in result.content[0].text.lower()
            except Exception as e:
                # Or raise structured error
                assert "invalid" in str(e).lower()
```

### Strategy 4: Mock External APIs

For faster tests, mock external API calls.

```python
from unittest.mock import patch, AsyncMock

async def test_tool_with_mocked_api():
    """Test MCP tool with mocked external API."""

    # Mock httpx client
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"alerts": []}
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "get_alerts",
                    arguments={"state": "CA"}
                )

                # Verify mock was called
                mock_get.assert_called_once()
```

**Benefits**:
- Faster tests (no network I/O)
- Deterministic results
- Test error scenarios easily

---

## Test Organization Patterns

### Pattern 1: Directory Structure

```
weekN/
├── app/
│   ├── main.py
│   ├── routers/
│   └── services/
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── test_extract.py          # Unit tests
│   ├── test_notes.py            # API integration tests
│   ├── test_action_items.py     # Business logic tests
│   └── manual/
│       ├── manual_llm.py        # Manual LLM testing
│       └── manual_filter.py     # Manual heuristic testing
└── pyproject.toml               # Pytest configuration
```

### Pattern 2: Fixture Reuse

Create reusable fixtures in `conftest.py`.

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture()
def client():
    """Create test client with in-memory database."""
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        session = TestingSessionLocal(bind=engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    os.unlink(db_path)
```

### Pattern 3: Test Class Organization

Group related tests in classes.

```python
class TestExtractActionItemsLLM:
    """Mock tests: Fast, deterministic, test logic not LLM."""

    @patch('week2.app.services.extract.chat')
    def test_success_case(self, mock_chat):
        """Test successful JSON parsing and list extraction."""
        pass

    @patch('week2.app.services.extract.chat')
    def test_error_handling(self, mock_chat):
        """Test graceful error handling."""
        pass


@pytest.mark.slow
class TestExtractActionItemsLLMReal:
    """Integration tests: Slow, real LLM, semantic assertions."""

    def test_basic_extraction(self):
        """Test basic extraction with real LLM."""
        pass

    def test_semantic_understanding(self):
        """Test semantic understanding vs description."""
        pass
```

### Pattern 4: Marker-Based Selection

Use pytest markers for test categories.

```python
# In pyproject.toml:
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

# In tests:
@pytest.mark.slow
def test_real_llm():
    pass

# Run specific categories:
pytest -m "not slow"      # Fast tests only
pytest -m "slow"          # Slow tests only
pytest -m "integration"   # Integration tests only
```

---

## Common Patterns

### Pattern 1: Parametrized Tests

Run same test with multiple inputs.

```python
@pytest.mark.parametrize("input_text,expected_count", [
    ("- Task 1\n- Task 2", 2),           # Basic case
    ("TODO: Fix bug", 1),                # Single item
    ("No action items here", 0),         # No items
    ("", 0),                             # Empty input
])
def test_extraction(input_text, expected_count):
    result = extract_action_items_llm(input_text)
    assert len(result) >= expected_count
```

### Pattern 2: Test Doubles (Mock, Stub, Fake)

| Type | Purpose | Example |
|------|---------|---------|
| **Mock** | Verify interactions | `mock_chat.assert_called_once()` |
| **Stub** | Provide canned responses | `mock_chat.return_value = {...}` |
| **Fake** | In-memory implementation | `FakeDatabase()` |

```python
# Mock: Verify behavior
@patch('module.function')
def test_mock_verification(mock_func):
    my_function()
    mock_func.assert_called_with("arg1", "arg2")

# Stub: Provide data
@patch('module.function')
def test_stub_response(mock_func):
    mock_func.return_value = "canned response"
    assert my_function() == "canned response"

# Fake: In-memory implementation
class FakeDatabase:
    def __init__(self):
        self.data = []

    def insert(self, item):
        self.data.append(item)
        return len(self.data)

def test_with_fake_db():
    db = FakeDatabase()
    assert db.insert("item") == 1
```

### Pattern 3: Context Managers for Setup/Teardown

Use context managers for resource cleanup.

```python
@pytest.fixture()
def test_client():
    """Automatically cleanup database after test."""
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    # Setup: Create database
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(bind=engine)

    # Yield test resource
    with TestClient(app) as client:
        yield client

    # Teardown: Cleanup
    os.unlink(db_path)
```

### Pattern 4: Assert Messages

Add helpful messages to assertions.

```python
# ❌ Bad: No context
assert len(result) == 2

# ✅ Good: Explains what's wrong
assert len(result) == 2, f"Expected 2 items, got {len(result)}: {result}"

# ✅ Even better: Diagnostic info
assert len(result) == 2, (
    f"Expected 2 action items, but got {len(result)}.\n"
    f"Result: {result}\n"
    f"Input: {input_text}"
)
```

---

## Mistakes & Lessons

### Mistake 1: Testing Implementation Details

**Problem**: Tests break when refactoring, even if behavior is unchanged.

```python
# ❌ Bad: Tests SQLAlchemy internals
def test_note_uses_sqlalchemy():
    assert note.session == expected_session

# ✅ Good: Tests behavior
def test_note_can_be_saved():
    saved_note = note.save()
    assert saved_note.id is not None
```

**Lesson**: Test behavior, not implementation.

### Mistake 2: Brittle LLM Assertions

**Problem**: Tests fail due to minor wording changes.

```python
# ❌ Bad: Exact match fails 30% of the time
assert result == ["Fix Bug #123"]

# ✅ Good: Semantic check
assert any("fix" in item.lower() and "bug" in item.lower() for item in result)
```

**Lesson**: Use semantic assertions for LLM tests.

### Mistake 3: Slow Test Suite

**Problem**: 21 seconds for 7 tests makes TDD painful.

```python
# ❌ Bad: All tests call real LLM
def test_extract():
    result = extract_action_items_llm("test")  # 2-3 seconds

# ✅ Good: 70% mocked, 20% real LLM
@patch('chat')
def test_extract_mock(mock_chat):
    mock_chat.return_value = {...}  # < 10ms

@pytest.mark.slow
def test_extract_real():
    result = extract_action_items_llm("test")  # 2-3s, but rare
```

**Lesson**: Mock external dependencies for 70% of tests.

### Mistake 4: No Error Path Testing

**Problem**: Only testing happy paths leads to production crashes.

```python
# ❌ Bad: Only tests success case
def test_extract_success():
    result = extract_action_items_llm("test")
    assert len(result) > 0

# ✅ Good: Tests failure modes
@patch('chat')
def test_extract_api_error(mock_chat):
    mock_chat.side_effect = Exception("API down")
    result = extract_action_items_llm("test")
    assert result == [], "Should return empty list on error"
```

**Lesson**: Test error paths (network errors, invalid JSON, missing keys).

### Mistake 5: Test Data Coupling

**Problem**: Tests depend on shared mutable state.

```python
# ❌ Bad: Tests share state
global_note = Note(title="Test")

def test_1():
    global_note.title = "Changed"

def test_2():
    # Fails because test_1 modified global_note
    assert global_note.title == "Test"

# ✅ Good: Each test is isolated
def test_1():
    note = Note(title="Test")
    note.title = "Changed"

def test_2():
    note = Note(title="Test")  # Fresh instance
    assert note.title == "Test"
```

**Lesson**: Tests should be isolated and independent.

### Mistake 6: Ignoring Flaky Tests

**Problem**: Intermittent test failures erode trust in test suite.

```python
# ❌ Bad: Retry logic hides flakiness
@retry(times=3)
def test_llm_extraction():
    result = extract_action_items_llm("test")
    assert "bug" in result[0].lower()  # Fails 30% of the time

# ✅ Good: Fix the test (use semantic assertions)
def test_llm_extraction():
    result = extract_action_items_llm("test")
    assert any("bug" in item.lower() for item in result)  # Always passes
```

**Lesson**: Fix flaky tests immediately, don't hide them with retries.

---

## Quick Reference Commands

### Pytest Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=module_name --cov-report=html

# Run specific test file
pytest tests/test_specific.py

# Run specific test function
pytest tests/test_specific.py::test_function

# Verbose output
pytest -v

# Show print output
pytest -s

# Stop on first failure
pytest -x

# Run in parallel (install pytest-xdist)
pytest -n auto

# Run markers
pytest -m "not slow"      # Fast tests only
pytest -m "slow"          # Slow tests only
pytest -m "integration"   # Integration tests only

# Last failed tests
pytest --lf

# Coverage with HTML report
open htmlcov/index.html  # View coverage report
```

### Mock Patterns

```python
from unittest.mock import patch, Mock

# Basic mock
@patch('module.function')
def test(mock_func):
    mock_func.return_value = "data"

# Mock exception
@patch('module.function')
def test(mock_func):
    mock_func.side_effect = Exception("error")

# Verify calls
mock_func.assert_called_once()
mock_func.assert_called_with(arg1, arg2)
mock_func.assert_not_called()

# Multiple mocks
@patch('module.func2')
@patch('module.func1')
def test(mock_func1, mock_func2):  # Order reversed!
    pass
```

### Fixture Patterns

```python
@pytest.fixture
def data():
    return {"key": "value"}

@pytest.fixture(scope="session")  # Shared across tests
def db():
    return Database()

@pytest.fixture(autouse=True)  # Automatically used
def log_time():
    start = time.time()
    yield
    print(f"Test took {time.time() - start}s")
```

---

## Further Reading

### Course Documentation
- [02_llm_integration.md](02_llm_integration.md) - LLM integration patterns
- [03_mcp_protocol.md](03_mcp_protocol.md) - MCP server architecture
- [patterns/testing_strategies.md](patterns/testing_strategies.md) - Original pattern template

### Week-Specific Content
- [Week 2 Implementation](weeks/week02/implementation.md) - LLM testing with Mock
- [Week 3 Overview](weeks/week03/overview.md) - MCP server testing
- [Week 4 Implementation](weeks/week04/implementation.md) - TDD with SubAgents

### Learning Notes
- [Week 2 Testing Patterns](../learning_notes/week2/practice/testing_patterns.md) - Comprehensive Chinese guide to Mock, pytest, and LLM testing
- [Week 2 Testing Concepts](../learning_notes/week2/fundamentals/03_testing_concepts.md) - Testing pyramid and philosophy

### External Resources
- [Pytest Documentation](https://docs.pytest.org/) - Official pytest guide
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html) - Mock library reference
- [MCP Specification](https://modelcontextprotocol.io) - Protocol documentation

---

*Generated from Weeks 1-8 testing experiences*
*Last updated: 2026-01-02*
