# Troubleshooting Guide

> **Common issues and solutions for Week 2**

## Import Errors

### ModuleNotFoundError: No module named 'week2'

**Symptoms:**
```bash
$ python week2/tests/test_extract.py
ModuleNotFoundError: No module named 'week2'
```

**Cause:** Running Python script directly doesn't add project root to `sys.path`

**Solutions:**
```bash
# Solution 1: Use pytest (recommended)
poetry run pytest week2/tests/test_extract.py

# Solution 2: Use python -m
python -m week2.tests.test_extract

# Solution 3: Use relative imports in test file
from ..app.services.extract import extract_action_items
```

### ImportError: attempted relative import with no known parent package

**Symptoms:**
```bash
$ python week2/app/main.py
ImportError: attempted relative import with no known parent package
```

**Cause:** Can't use relative imports when running file directly

**Solutions:**
```bash
# Solution: Run as module
poetry run python -m week2.app.main

# Or use uvicorn
poetry run uvicorn week2.app.main:app --reload
```

## Ollama Issues

### Connection refused

**Symptoms:**
```python
httpx.ConnectError: [Errno 61] Connection refused
```

**Cause:** Ollama is not running

**Solutions:**
```bash
# Start Ollama
ollama serve

# In another terminal, verify it's running
curl http://localhost:11434/api/tags
```

### Model not found

**Symptoms:**
```python
Error: model 'llama3.1:8b' not found
```

**Solutions:**
```bash
# Pull the model
ollama pull llama3.1:8b

# Verify it's available
ollama list
```

### LLM returns inconsistent results

**Symptoms:** Same input produces different outputs

**Solutions:**
```python
# Lower temperature for deterministic results
options = {'temperature': 0.1}  # Was 0.3 or higher
```

## Database Issues

### sqlite3.OperationalError: no such table

**Symptoms:**
```python
sqlite3.OperationalError: no such table: notes
```

**Cause:** Database not initialized

**Solutions:**
```bash
# Initialize database
poetry run python -c "from week2.app.database import init_db; init_db()"
```

### Database is locked

**Symptoms:**
```python
sqlite3.OperationalError: database is locked
```

**Cause:** Multiple processes accessing database

**Solutions:**
```bash
# Close all connections, then:
rm week2/database.db
poetry run python -c "from week2.app.database import init_db; init_db()"
```

### Wrong data returned

**Symptoms:** Queries return unexpected results

**Solutions:**
```bash
# Inspect database
sqlite3 week2/database.db
> SELECT * FROM notes;
> SELECT * FROM action_items;
> .quit
```

## Server Issues

### Port already in use

**Symptoms:**
```bash
ERROR: [Errno 48] Address already in use
```

**Solutions:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
poetry run uvicorn week2.app.main:app --port 8080
```

### Changes not reflected

**Symptoms:** Code changes don't affect running server

**Cause:** Server running without `--reload`

**Solutions:**
```bash
# Always use --reload for development
poetry run uvicorn week2.app.main:app --reload
```

## Testing Issues

### Tests pass locally but fail in CI

**Common causes:**
- Ollama not available in CI
- Database not initialized
- Environment variables missing

**Solutions:**
```python
# Use pytest marks for slow/integration tests
@pytest.mark.slow
def test_real_llm():
    pass

# Skip in CI if needed
@pytest.mark.skipif(os.getenv("CI") == "true", reason="No Ollama in CI")
def test_needs_ollama():
    pass
```

### Mock not working

**Symptoms:** Mock decorator doesn't replace function

**Cause:** Wrong import path in mock

**Solutions:**
```python
# WRONG - imports the function, can't mock it
from week2.app.services.extract import chat
@patch('week2.app.services.extract.chat')  # Wrong path!

# CORRECT - mock where it's used
from week2.app.services.extract import extract_action_items_llm
@patch('week2.app.services.extract.chat')  # Correct path!
```

### AssertionError in post-processing

**Symptoms:** Test fails due to ordering or duplicates

**Solutions:**
```python
# Use set comparison for order-insensitive checks
assert set(result) == set(expected)

# Or sort both
assert sorted(result) == sorted(expected)
```

## Type Validation Issues

### ValidationError from Pydantic

**Symptoms:**
```python
pydantic.ValidationError: 1 validation error for ExtractRequest
```

**Cause:** Input doesn't match schema

**Solutions:**
```python
# Check schema requirements
class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1)  # Required, min 1 char
    save_note: bool = Field(default=False)  # Optional, defaults to False

# Valid request:
{"text": "some text", "save_note": true}
{"text": "some text"}  # save_note uses default

# Invalid request:
{}  # Missing required 'text'
{"text": ""}  # Too short (< 1 char)
```

## Logging Issues

### Too much output

**Symptoms:** Console flooded with debug messages

**Solutions:**
```python
# Configure log level
import logging
logging.basicConfig(level=logging.INFO)  # Hide DEBUG messages

# Or per module
logger.setLevel(logging.WARNING)
```

### No output when expected

**Symptoms:** Log messages not appearing

**Solutions:**
```python
# Ensure handler is configured
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Check logger name
logger = logging.getLogger(__name__)  # Use __name__, not hardcoded string
```

## Performance Issues

### Slow test execution

**Symptoms:** Tests take too long

**Solutions:**
```bash
# Skip slow tests during development
poetry run pytest week2/tests/ -m "not slow"

# Only run specific test
poetry run pytest week2/tests/test_extract.py::test_specific_function

# Use parallel execution (if configured)
poetry run pytest -n auto week2/tests/
```

### LLM API slow

**Symptoms:** Each request takes 2-3 seconds

**Solutions:**
```python
# Mock LLM in most tests
@patch('week2.app.services.extract.chat')
def test_fast(mock_chat):
    mock_chat.return_value = {...}
    # Runs in milliseconds

# Only use real LLM in integration tests
@pytest.mark.slow
def test_real_llm():
    # Runs in seconds, but marked as slow
    pass
```

## Git Issues

### Pre-commit hook fails

**Symptoms:**
```bash
pre-commit hook failed...
```

**Solutions:**
```bash
# Run pre-commit manually to see issues
poetry run pre-commit run --all-files

# Fix formatting
poetry run black week2/
poetry run ruff check --fix week2/

# Re-run commit
git commit ...
```

### Merge conflicts

**Symptoms:** Git reports conflicts after pull

**Solutions:**
```bash
# Resolve conflicts manually, then:
git add <resolved-files>
git commit
```

## Environment Issues

### Poetry install fails

**Symptoms:**
```bash
EnvCommandError: command ['python', '...'] returned non-zero exit status
```

**Solutions:**
```bash
# Try with explicit Python version
poetry env use python3.12
poetry install

# Or recreate environment
poetry env remove --all
poetry install
```

### Wrong Python version

**Symptoms:**
```bash
 poetry run python --version
Python 3.11.x  # Expected 3.12
```

**Solutions:**
```bash
# Check available versions
poetry env list

# Create new env with correct version
poetry env use /path/to/python3.12
poetry install
```

## Quick Diagnostic Commands

```bash
# Check all services
echo "=== Python Version ==="
poetry run python --version

echo "=== Dependencies ==="
poetry show

echo "=== Ollama Status ==="
curl -s http://localhost:11434/api/tags || echo "Ollama not running"

echo "=== Database ==="
ls -la week2/database.db 2>/dev/null || echo "Database not found"

echo "=== Server ==="
lsof -i :8000 || echo "Port 8000 free"

echo "=== Tests ==="
poetry run pytest week2/tests/ -m "not slow" --collect-only | head -20
```

## Getting Help

1. Check error messages carefully - they usually indicate the issue
2. Search error messages in project issues/docs
3. Use diagnostic commands above
4. Check related reference files:
   - `reference/command_reference.md`
   - `reference/code_patterns.md`
   - `practice/exception_handling.md`
