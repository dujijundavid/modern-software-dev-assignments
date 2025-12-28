# Architecture Decisions

Record of significant architectural choices with rationale and implications.

---

## Database Architecture

### Decision: SQLite with Custom Exception Hierarchy

**Context:** Need reliable database operations with proper error handling for a FastAPI application.

**Options Considered:**
1. Direct sqlite3 with try/except
2. SQLAlchemy with default exceptions
3. SQLAlchemy with custom exception hierarchy ✅ **CHOSEN**

**Rationale:**
- Custom exceptions provide domain-specific error semantics
- Enables global exception handlers for consistent API responses
- Separates database errors from business logic errors

**Implementation:**
```python
# app/db/exceptions.py
class DatabaseError(Exception):
    """Base database error"""
    pass

class NotFoundError(DatabaseError):
    """Resource not found in database"""
    pass

# Usage in handlers
@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content={"error": str(exc)})
```

**Implications:**
- Pros: Clean error handling, type-safe error catching, consistent HTTP responses
- Cons: Additional boilerplate for custom exception classes

**Alternatives for Future:**
- PostgreSQL for production scaling
- Connection pooling for high concurrency

---

## Service Layer Pattern

### Decision: Separate Business Logic from Routers

**Context:** FastAPI route handlers were becoming complex with LLM integration logic.

**Options Considered:**
1. Put all logic in route handlers
2. Use repository pattern with services
3. Service layer with database operations abstracted ✅ **CHOSEN**

**Rationale:**
- Separation of concerns improves testability
- Services can be reused across multiple endpoints
- Easier to mock services for testing

**Architecture:**
```
app/
├── routers/          # HTTP layer (FastAPI routes)
│   └── notes.py      # Defines endpoints, calls services
├── services/         # Business logic layer
│   ├── extract.py    # LLM extraction logic
│   └── notes.py      # Note business operations
└── db/               # Data access layer
    └── database.py   # SQLite operations
```

**Example:**
```python
# routers/notes.py
@router.post("/notes/{id}/extract")
async def extract_items(id: int, service: ExtractService = Depends()):
    return await service.extract_from_note(id)

# services/extract.py
class ExtractService:
    async def extract_from_note(self, note_id: int):
        note = await self.db.get_note(note_id)
        items = await self.llm.extract(note.content)
        return await self.db.create_action_items(items)
```

**Implications:**
- Pros: Testable, reusable, clear separation of concerns
- Cons: More files, additional indirection

---

## Dependency Injection for Testing

### Decision: FastAPI Dependency Overrides

**Context:** Need to test with in-memory databases without affecting production.

**Options Considered:**
1. Environment variables for database path
2. Test base class with database setup
3. FastAPI dependency overrides ✅ **CHOSEN**

**Rationale:**
- FastAPI-native testing approach
- No production code changes for testing
- Clean isolation between test and production

**Implementation:**
```python
# Production dependency
async def get_db():
    async with db.session("database.db") as session:
        yield session

# Test override
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: get_test_db(":memory:")
    yield TestClient(app)
    app.dependency_overrides.clear()
```

**Implications:**
- Pros: Clean test isolation, no production contamination
- Cons: Requires explicit override management

---

## LLM Integration Architecture

### Decision: Ollama with Structured JSON Output

**Context:** Need reliable LLM integration for extracting structured action items.

**Options Considered:**
1. OpenAI API (cloud, costs money)
2. Hugging Face transformers (local, complex setup)
3. Ollama with llama3.1:8b ✅ **CHOSEN**

**Rationale:**
- Ollama provides simple local inference
- llama3.1:8b balances speed and accuracy
- JSON schema enforcement ensures structured output

**Configuration:**
```python
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "llama3.1:8b",
    "temperature": 0.1,  # Low for consistency
    "format": "json",    # Enforce JSON output
}
```

**Prompt Engineering:**
```python
SYSTEM_PROMPT = """You are an action item extractor. Extract ONLY specific, 
actionable items from the given text. Vague items like "do work" should be 
excluded. Return as JSON array of strings."""
```

**Implications:**
- Pros: No API costs, local processing, consistent outputs
- Cons: Requires Ollama service running, ~8GB RAM for model

---

## MCP Server Architecture (Week 3)

### Decision: Async MCP with Rate Limiting

**Context:** Building Model Context Protocol server for tool integration.

**Options Considered:**
1. Synchronous MCP server
2. Async MCP with rate limiting ✅ **CHOSEN**
3. Async MCP with queue system

**Rationale:**
- Async prevents blocking during LLM calls
- Rate limiting prevents API abuse
- Simple approach sufficient for course project

**Implementation Pattern:**
```python
class MCPServer:
    def __init__(self):
        self.rate_limiter = RateLimiter(3)  # 3 req/sec
        self.tools = {}
    
    async def call_tool(self, name: str, params: dict):
        await self.rate_limiter.acquire()
        return await self.tools[name](params)
```

**Implications:**
- Pros: Prevents abuse, non-blocking, simple implementation
- Cons: Fixed rate limit may be restrictive

---

## Exception Handler Strategy

### Decision: Global FastAPI Exception Handlers

**Context:** Need consistent error responses across all endpoints.

**Options Considered:**
1. Try/except in each route handler
2. Custom decorator for error handling
3. Global exception handlers ✅ **CHOSEN**

**Rationale:**
- DRY principle - handle errors once
- Consistent error response format
- Separation of error handling from business logic

**Implementation:**
```python
app = FastAPI()

@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Resource not found", "detail": str(exc)}
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Database error", "detail": str(exc)}
    )
```

**Implications:**
- Pros: Consistent responses, centralized error logic
- Cons: Less granular control per endpoint

---

## API Response Format

### Decision: Standardized Response Envelope

**Context:** Need consistent API response format for frontend integration.

**Chosen Format:**
```python
# Success response
{
    "data": {...},
    "status": "success"
}

# Error response
{
    "error": "Error type",
    "detail": "Human-readable message",
    "status": "error"
}
```

**Rationale:**
- Frontend can parse responses uniformly
- Easy to distinguish success vs error
- Includes metadata for debugging

---

## Future Architectural Considerations

### When to Scale Beyond SQLite
- Consider PostgreSQL when:
  - Multiple concurrent writers needed
  - Complex queries with JOINs become slow
  - Need features like full-text search

### When to Add Message Queue
- Consider when:
  - Background job processing needed
  - Multiple workers required
  - Real-time updates become important

### When to Add Caching
- Consider when:
  - LLM responses become expensive
  - Database queries are repetitive
  - API response times >2 seconds

---

## Decision Log Template

For future architectural decisions, use this template:

```markdown
### Decision: [Title]

**Context:** [What problem are we solving?]

**Options Considered:**
1. [Option 1]
2. [Option 2]
3. [Option 3] ✅ **CHOSEN**

**Rationale:**
- [Reason 1]
- [Reason 2]

**Implementation:**
[Code snippet or architecture diagram]

**Implications:**
- Pros: [List advantages]
- Cons: [List disadvantages]

**Alternatives for Future:**
[What might we consider later?]
```
