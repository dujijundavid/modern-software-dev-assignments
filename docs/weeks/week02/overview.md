---
week: 2
title: "Week 2: LLM-Powered Applications"
type: concept
status: completed
created: 2025-12-28
updated: 2026-01-02
related:
  - week:2:implementation.md
  - week:2:reflection.md
tags: [week-2, concepts, llm-integration, fastapi, testing]
---

# Week 2: LLM-Powered Applications

> **Navigation**: [CS146S Docs](../../INDEX.md) > [Weeks](../weeks/) > [Week 2](../weeks/week02/) > Overview

## Learning Objectives

- **Integrate Local LLMs**: Use Ollama to run llama3.1:8b locally for intelligent text processing
- **Structured Output**: Implement JSON Schema constraints to guarantee parseable LLM responses
- **Testing Patterns**: Master Mock for fast unit tests and semantic assertions for LLM integration tests
- **Code Refactoring**: Transform working code into maintainable, type-safe production code
- **API Development**: Build FastAPI endpoints with Pydantic validation and custom error handling

## Key Concepts

### 1. Structured Output with LLMs

**Description**: LLMs generate text probabilistically, making output unreliable for applications that need structured data. JSON Schema constraints force LLMs to return parseable, typed responses.

**Why it matters**: Without structured output, 95% of production LLM applications fail due to parsing errors, format mismatches, or unexpected data types.

**Key points**:
- LLMs are non-deterministic: same prompt → different outputs
- JSON Schema provides three layers: type constraints, value constraints, structure constraints
- Ollama supports `format='json'` parameter for guaranteed JSON output
- Low temperature (0.1-0.3) increases consistency for extraction tasks
- Post-processing cleans, deduplicates, and validates responses

**Example**:
```python
json_schema = {
    'type': 'object',
    'properties': {
        'action_items': {
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'List of actionable items'
        }
    },
    'required': ['action_items']
}

response = chat(
    model='llama3.1:8b',
    messages=[...],
    format=json_schema,  # Guarantees valid JSON
    options={'temperature': 0.1}
)
```

### 2. Testing Pyramid for LLM Applications

**Description**: LLM tests should be layered: 70% fast unit tests with Mock, 20% integration tests with real LLM, 10% edge case tests.

**Why it matters**: Real LLM calls are slow (2-3s each) and non-deterministic. Mock tests run in milliseconds and are deterministic.

**Key points**:
- **Mock tests**: Replace external dependencies with "stunt doubles", test your logic not the LLM
- **Integration tests**: Use real LLM with semantic assertions (check keywords, not exact matches)
- **Semantic assertions**: For LLM tests, assert on meaning not exact wording
- **Pytest markers**: Use `@pytest.mark.slow` to separate fast from slow tests
- **Speed ratio**: Mock tests are 60x faster than real LLM tests

**Example**:
```python
# Fast, deterministic unit test
@patch('week2.app.services.extract.chat')
def test_extract_fast(mock_chat):
    mock_chat.return_value = {
        'message': {'content': '{"action_items": ["Task 1"]}'}
    }
    result = extract_action_items_llm("test")
    assert result == ["Task 1"]  # Exact match OK

# Slow, semantic integration test
@pytest.mark.slow
def test_extract_real_llm():
    result = extract_action_items_llm("- Fix bug")
    assert len(result) >= 1  # Not exact match
    assert any("bug" in item.lower() for item in result)
```

### 3. Layered Architecture with Type Safety

**Description**: Separate concerns into Router (Pydantic validation), Service (business logic), and Database (persistence) layers.

**Why it matters**: Layered architecture isolates changes, makes testing easier, and enables type-safe APIs.

**Key points**:
- **Router layer**: FastAPI endpoints with Pydantic request/response models
- **Service layer**: Business logic (LLM integration, extraction algorithms)
- **Database layer**: Returns `dict` not `sqlite3.Row` to hide implementation
- **Pydantic schemas**: Auto-validation, type checking, API documentation
- **Factory methods**: Eliminate repetitive object construction

**Example**:
```python
# Router: Type-safe endpoint
class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1)

@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    items = extract_action_items(payload.text)  # Service layer
    return ExtractResponse(items=items)

# Database: Hides implementation
def get_note(note_id: int) -> Optional[dict]:
    row = cursor.fetchone()
    return dict(row) if row else None  # Not sqlite3.Row
```

### 4. Graceful Error Handling

**Description**: Custom exceptions with context, global handlers, and graceful degradation prevent cascading failures.

**Why it matters**: LLM APIs can fail, timeout, or return invalid data. Applications should degrade gracefully, not crash.

**Key points**:
- **Context-rich exceptions**: Carry resource type and ID for debugging
- **Global handlers**: Centralize error responses, not scattered if-checks
- **Graceful degradation**: Return empty list on LLM failure, don't crash
- **Logging**: Use structured logging with levels (DEBUG, INFO, WARNING, ERROR)
- **HTTP status mapping**: DatabaseError → 500, NotFoundError → 404

**Example**:
```python
# Custom exception with context
class NotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(f"{resource_type} with id {resource_id} not found")

# Global handler
@app.exception_handler(NotFoundError)
async def notfound_handler(request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

# Graceful degradation in LLM call
try:
    response = chat(...)
    items = parse_response(response)
except Exception as e:
    logger.warning(f"LLM extraction failed: {e}, returning empty list")
    return []  # Don't crash
```

## Prerequisites

- **Python 3.10+**: For modern type hints and match statements
- **FastAPI basics**: Understanding of routers, dependencies, and request handling
- **SQL fundamentals**: Basic SELECT/INSERT/UPDATE knowledge
- **Testing concepts**: Familiarity with pytest and assertions

**Setup commands**:
```bash
# Install Ollama
ollama pull llama3.1:8b

# Start Ollama server
ollama serve

# Install Python dependencies
poetry install

# Run tests
poetry run pytest week2/tests/ -m "not slow"
```

## Resources

- **Primary**: [Ollama Structured Outputs](https://ollama.com/blog/structured-outputs) - JSON Schema with local LLMs
- **Primary**: [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - Request/response models and error handling
- **Supplementary**: [Pydantic Documentation](https://docs.pydantic.dev/latest/) - Data validation and settings management
- **Reference**: [JSON Schema Specification](https://json-schema.org/) - Understanding schema validation

## Related Patterns

- [Testing Patterns](../patterns/testing-patterns.md) - Mock strategy and test organization
- [API Design Patterns](../patterns/api-design.md) - RESTful design with FastAPI
- [Error Handling Patterns](../patterns/error-handling.md) - Exception design and graceful degradation

## Quick Links

- [Implementation Details](./implementation.md) - Technical approach and code patterns
- [Reflection](./reflection.md) - Learning outcomes and lessons learned
- [Weekly Deliverable](../../weeks/week2/week2_writeup.md) - Submission writeup

## AI Engineering Mindset

**The Three Questions**:
1. **What's the bottleneck?**: Manual testing of LLM features is slow (2-3s per test). Mock tests reduce this to milliseconds.
2. **What's the leverage point?**: Structured output eliminates 95% of parsing errors, making LLMs production-ready.
3. **How to compound value?**: Layered architecture with type safety enables adding new features without breaking existing code.

**Automation Level**: Level 2 (Reusable Functions)
- Evidence: Extract functions are reusable, test patterns are documented, refactoring patterns are repeatable
- Next level: Create Warp prompts for LLM integration and testing patterns
