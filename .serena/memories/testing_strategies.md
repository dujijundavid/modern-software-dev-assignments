# Testing Strategies

Comprehensive testing approach for FastAPI applications with LLM integration.

---

## Testing Philosophy

**Three-Tier Testing Strategy:**
- **70% Unit Tests** - Test individual functions and classes in isolation
- **20% Integration Tests** - Test component interactions
- **10% E2E/Refactoring Tests** - Test full workflows and support refactoring

**Goals:**
- Catch bugs early (shift-left testing)
- Enable confident refactoring
- Document expected behavior through tests
- Maintain >80% code coverage

---

## Pytest Configuration

### Setup

**pytest.ini:**
```ini
[pytest]
testpaths = week1 week2 week3 week4 week5 week6 week7 week8
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
markers =
    slow: marks tests as slow (deselect with -m "not slow")
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Key Fixtures

**Database Fixture (tempfile-based):**
```python
@pytest.fixture
def client():
    """Create test client with temporary database"""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    
    # Override production dependency
    app.dependency_overrides[get_db] = lambda: get_test_db(db_path)
    
    yield TestClient(app)
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)
    app.dependency_overrides.clear()
```

**Mock LLM Fixture:**
```python
@pytest.fixture
def mock_ollama(monkeypatch):
    """Mock Ollama LLM calls for fast, deterministic tests"""
    async def mock_call(prompt, **kwargs):
        return json.dumps([
            "Review project requirements",
            "Set up development environment"
        ])
    
    monkeypatch.setattr("ollama.__call__", mock_call)
    return mock_call
```

---

## Testing Patterns

### Unit Tests

**Focus:** Test individual functions in isolation

**Example:**
```python
def test_extract_action_items_parses_json():
    """Test that JSON parsing works correctly"""
    json_response = '["item1", "item2", "item3"]'
    result = extract_action_items_llm(json_response)
    assert result == ["item1", "item2", "item3"]

def test_extract_action_items_filters_short_items():
    """Test that single-word items < 6 chars are filtered"""
    items = ["Complete project setup", "todo", "Write documentation"]
    result = filter_action_items(items)
    assert result == ["Complete project setup", "Write documentation"]
```

### Integration Tests

**Focus:** Test component interactions with real dependencies

**Example:**
```python
@pytest.mark.integration
async def test_extract_endpoint_with_real_llm(client):
    """Test full endpoint with real Ollama (slow)"""
    response = client.post("/notes/1/extract")
    assert response.status_code == 200
    data = response.json()
    assert "action_items" in data
    assert len(data["action_items"]) > 0
```

### Endpoint Tests

**Focus:** Test HTTP layer (status codes, response formats)

**Example:**
```python
def test_create_note_endpoint(client):
    """Test note creation endpoint"""
    response = client.post(
        "/notes",
        json={"title": "Test", "content": "Content"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test"
    assert "id" in data

def test_get_note_not_found(client):
    """Test 404 response for non-existent note"""
    response = client.get("/notes/99999")
    assert response.status_code == 404
    assert "error" in response.json()
```

---

## LLM Testing Strategy

### Challenge: LLMs are Non-Deterministic

**Solutions:**

1. **Mock LLM for Unit Tests**
```python
@pytest.fixture
def mock_llm_response(monkeypatch):
    """Deterministic mock for unit tests"""
    monkeypatch.setattr(
        "ollama.__call__",
        lambda **kwargs: '["action 1", "action 2"]'
    )

def test_extract_with_mock(mock_llm_response):
    result = extract_action_items_llm("test")
    assert result == ["action 1", "action 2"]
```

2. **Use Real LLM for Integration Tests**
```python
@pytest.mark.slow
@pytest.mark.integration
def test_extract_with_real_llm():
    """Actual LLM call - mark as slow/integration"""
    result = extract_action_items_llm("Buy groceries and call mom")
    assert len(result) >= 1
    assert any("groceries" in item.lower() for item in result)
```

3. **Test Post-Processing Logic Separately**
```python
def test_filter_vague_items():
    """Test filtering logic without LLM"""
    items = ["do stuff", "Complete the project report", "todo"]
    filtered = filter_action_items(items)
    assert "do stuff" not in filtered
    assert "todo" not in filtered
    assert "Complete the project report" in filtered
```

---

## Database Testing

### In-Memory Database for Speed
```python
@pytest.fixture
def test_db():
    """Use :memory: database for fast tests"""
    db = SQLAlchemy("sqlite:///:memory:")
    db.create_all()
    yield db
    db.drop_all()
```

### Transaction Rollback for Isolation
```python
@pytest.fixture
def db_session():
    """Roll back transactions after each test"""
    session = Session()
    transaction = session.begin_nested()
    
    yield session
    
    session.close()
    transaction.rollback()
```

---

## Test Organization

### Directory Structure
```
week1/
├── app/
│   ├── main.py
│   └── routers/
│       └── notes.py
└── tests/
    ├── __init__.py
    ├── conftest.py          # Shared fixtures
    ├── test_routes.py       # Endpoint tests
    ├── test_services.py     # Business logic tests
    └── test_db.py           # Database tests
```

### Test Naming Conventions
```python
# Good: Descriptive names that explain what and why
def test_extract_action_items_filters_single_words_under_6_chars():
    pass

# Bad: Vague names
def test_extract_test():
    pass
```

---

## Coverage Targets

### Minimum Coverage by Component
| Component | Target | Rationale |
|-----------|--------|-----------|
| Routes | 80% | HTTP layer should be thoroughly tested |
| Services | 90% | Business logic is critical |
| Database | 85% | Data operations need high confidence |
| Utils | 100% | Small utilities should be fully covered |

### Coverage Commands
```bash
# Run tests with coverage
pytest --cov=week1/app --cov-report=html

# View HTML report
open htmlcov/index.html

# Check specific file coverage
pytest --cov=week1/app/services/extract.py --cov-report=term-missing
```

---

## Testing Anti-Patterns

### ❌ Don't: Test Implementation Details
```python
# Bad: Tests internal function that might change
def test_private_function():
    result = _internal_helper(data)
    assert result == expected
```

### ✅ Do: Test Public Behavior
```python
# Good: Tests the public API
def test_extract_action_items_returns_list():
    result = extract_action_items_llm(note_content)
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)
```

### ❌ Don't: Test with Production Database
```python
# Bad: Uses real database, slow and dangerous
def test_with_real_db():
    db = connect_to_production_db()
    result = db.get_note(1)
    assert result.title == "Test"
```

### ✅ Do: Use Test Doubles
```python
# Good: Uses mock or in-memory database
def test_with_mock_db(mock_db):
    mock_db.add_note(Note(title="Test"))
    result = mock_db.get_note(1)
    assert result.title == "Test"
```

### ❌ Don't: Over-Mock Everything
```python
# Bad: Tests nothing but mock configuration
def test_over_mocked(mock_db, mock_llm, mock_logger, mock_cache):
    result = mock_service.extract()
    assert result == mock_result  # Only tests mocks!
```

### ✅ Do: Mock External Dependencies Only
```python
# Good: Mocks only external LLM, tests real business logic
def test_with_strategic_mocks(mock_llm):
    service = ExtractService(db=real_db, llm=mock_llm)
    result = service.extract_from_note(1)
    assert len(result) > 0
```

---

## Running Tests

### During Development
```bash
# Run fast unit tests only
pytest -m "not slow" -q

# Run tests for specific week
pytest week2/tests/ -v

# Run tests for specific file
pytest week2/tests/test_extract.py -v
```

### Before Committing
```bash
# Run all tests with coverage
pytest --cov=week2/app -v

# Ensure coverage meets threshold
pytest --cov=week2/app --cov-fail-under=80
```

### CI/CD Pipeline
```bash
# Run all tests
pytest -v

# Generate coverage report
pytest --cov=week1/app --cov=week2/app --cov-report=xml
```

---

## Debugging Tests

### Verbose Output
```bash
pytest -v -s  # Show print statements
```

### Drop into PDB on Failure
```bash
pytest --pdb  # Drop into debugger on failure
pytest --pdb-trace  # Trace execution
```

### Run Specific Test
```bash
pytest week2/tests/test_extract.py::test_extract_action_items -v
```

### Show Local Variables on Failure
```bash
pytest -l  # Show locals in traceback
```

---

## Test Maintenance

### When Tests Become Brittle
1. **Identify flaky tests** - Run multiple times to catch non-determinism
2. **Fix isolation issues** - Ensure tests don't depend on execution order
3. **Reduce test coupling** - Tests shouldn't depend on each other

### When Tests Are Slow
1. **Profile the tests** - `pytest --durations=10` shows slowest tests
2. **Mock more dependencies** - Reduce real I/O operations
3. **Use markers** - Mark slow tests as `@pytest.mark.slow`

### When Coverage Stalls
1. **Find uncovered lines** - `--cov-report=term-missing` shows line numbers
2. **Add edge case tests** - Test error paths, boundary conditions
3. **Test error handling** - Ensure exceptions are properly handled
