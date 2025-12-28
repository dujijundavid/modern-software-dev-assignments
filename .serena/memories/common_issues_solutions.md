# Common Issues and Solutions

Living knowledge base of recurrent problems and proven solutions.

---

## Environment & Setup

### Ollama Connection Timeout

**Symptoms:** `ollama.__call__()` hangs indefinitely

**Root Cause:** Ollama service not running or port conflict

**Solution:**
```bash
# Check if running
ollama list

# Start service
ollama serve

# In Python, add timeout and retry
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_ollama_with_retry(prompt):
    return ollama.__call__(prompt)
```

**Prevention:** Add health check endpoint that pings Ollama before extraction

---

### Poetry Environment Issues

**Symptoms:** Module not found despite poetry install

**Root Cause:** Poetry using wrong Python environment

**Solution:**
```bash
# Check Poetry Python version
poetry env info

# Recreate with correct Python
poetry env use python3.12
poetry install
```

---

## LLM Integration

### JSON Parse Errors from LLM

**Symptoms:** `json.loads()` fails on LLM response

**Root Cause:** LLM returns markdown-formatted JSON or includes explanations

**Solution:**
```python
# Use JSON schema validation with Ollama
response = ollama.__call__(
    prompt, 
    format='json',  # Enforces pure JSON
    schema={"type": "array", "items": {"type": "string"}}
)
```

**Prevention:** Always use `format='json'` with schema validation

---

### LLM Hallucinations in Action Items

**Symptoms:** Extracted items contain generic/vague content like "do stuff"

**Root Cause:** Prompt lacks specificity or temperature too high

**Solution:**
```python
# Lower temperature for consistency
temperature=0.1

# Add explicit constraints in prompt
"Extract ONLY specific, actionable items. Vague items like 'do work' should be excluded."
```

**Post-processing:**
```python
# Filter single-word items < 6 characters
filtered = [item for item in items if len(item) >= 6 or ' ' in item]
```

---

## FastAPI & Async

### Async/Await Database Errors

**Symptoms:** "RuntimeError: Event loop is closed"

**Root Cause:** Mixing sync and async database operations

**Solution:**
```python
# Always use async context
async def get_db():
    async with db.session() as session:
        yield session

# Use async/await consistently
async def create_note(note: NoteCreate, db: AsyncSession):
    result = await db.execute(insert(Note).values(**note.dict()))
    await db.commit()
    return result.scalar_one()
```

---

### CORS Errors in Development

**Symptoms:** Browser blocks API requests due to CORS

**Solution:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing

### Test Database Pollution

**Symptoms:** Tests affect each other, data from previous tests appears

**Root Cause:** Tests not properly isolated

**Solution:**
```python
# Use tempfile for each test
@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    app.dependency_overrides[get_db] = lambda: get_test_db(db_path)
    yield TestClient(app)
    os.close(db_fd)
    os.unlink(db_path)
    app.dependency_overrides = {}
```

---

### Mocking LLM Responses

**Symptoms:** Tests are slow, depend on external Ollama service

**Solution:**
```python
@pytest.fixture
def mock_ollama(monkeypatch):
    async def mock_call(prompt, **kwargs):
        return json.dumps(["action item 1", "action item 2"])
    monkeypatch.setattr("ollama.__call__", mock_call)

# Use in tests
def test_extract_action_items(mock_ollama):
    result = extract_action_items_llm("test note")
    assert result == ["action item 1", "action item 2"]
```

---

## Database

### SQLite Locking Errors

**Symptoms:** "database is locked" errors during concurrent access

**Root Cause:** SQLite write locks during concurrent writes

**Solution:**
```python
# Use WAL mode for better concurrency
cursor.execute("PRAGMA journal_mode=WAL")

# Or use connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "sqlite:///database.db",
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10
)
```

---

### Migration Issues

**Symptoms:** Schema changes break existing code

**Solution:**
```python
# Version your schema
# Version 1: Initial schema
# Version 2: Add 'completed' column to notes

def migrate_db(db_path):
    conn = sqlite3.connect(db_path)
    # Check current version
    version = conn.execute("SELECT version FROM schema_version").fetchone()[0]
    
    if version < 2:
        conn.execute("ALTER TABLE notes ADD COLUMN completed BOOLEAN DEFAULT 0")
        conn.execute("UPDATE schema_version SET version = 2")
    
    conn.commit()
```

---

## Git Workflow

### Commit Message Format Issues

**Symptoms:** Inconsistent commit history, unclear intent

**Solution:**
```
# Use conventional commits
type(scope): description

# Types: feat, fix, refactor, docs, test, chore
feat(week2): add LLM extraction endpoint
fix(db): resolve SQLite locking in concurrent tests
refactor(services): extract LLM logic to service layer

# Always include why, not just what
# Bad: "add function"
# Good: "add function to extract action items using LLM"
```

---

### Merge Conflict in .gitignore

**Symptoms:** .gitignore changes cause conflicts

**Prevention:**
```
# Use section-based organization with clear comments
# Each section has one purpose
# Add new sections at the end, don't reorder existing
```

---

## Performance

### Slow LLM Response Times

**Symptoms:** API calls take 5-10 seconds

**Root Cause:** High temperature, verbose prompts, or slow model

**Solutions:**
```python
# 1. Lower temperature (0.1 vs 0.7)
# 2. Use smaller model (llama3.1:8b vs llama3.1:70b)
# 3. Add caching for repeated prompts
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_llm_call(prompt_hash):
    return ollama.__call__(prompt)
```

---

## Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or for FastAPI
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.debug(f"Response: {response.status_code}")
    return response
```

---

### Use FastAPI Auto-Docs

```
# Visit these URLs for debugging
http://localhost:8000/docs     # Swagger UI
http://localhost:8000/redoc    # ReDoc
```
