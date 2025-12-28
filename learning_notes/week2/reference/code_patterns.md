# Code Patterns Reference

> **Common patterns used in Week 2 project**

## Pydantic Patterns

### Request/Response Models

```python
from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1)
    save_note: bool = Field(default=False)

class ActionItemResponse(BaseModel):
    id: int
    text: str
    note_id: Optional[int] = None
    done: bool
    created_at: str
```

### Factory Method Pattern

```python
class ActionItemResponse(BaseModel):
    @classmethod
    def from_dict(cls, data: dict) -> "ActionItemResponse":
        return cls(
            id=data["id"],
            text=data["text"],
            note_id=data.get("note_id"),
            done=bool(data["done"]),
            created_at=data["created_at"],
        )
```

### Usage in Router

```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    # payload.text is auto-validated (min_length=1)
    items = extract_action_items(payload.text)
    return ExtractResponse(items=items)
```

## Exception Patterns

### Custom Exceptions with Context

```python
class DatabaseError(Exception):
    """Base exception for database operations."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(DatabaseError):
    """Exception for resource not found errors."""
    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message)
```

### Global Exception Handler

```python
from fastapi.responses import JSONResponse

@app.exception_handler(NotFoundError)
async def notfound_error_handler(request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )
```

## Database Patterns

### Return Dict Not Row

```python
import sqlite3
from typing import Optional

def get_note(note_id: int) -> Optional[dict]:
    """Get a note by ID, returning dict or None."""
    cursor.execute(
        "SELECT id, content, created_at FROM notes WHERE id = ?",
        (note_id,)
    )
    row = cursor.fetchone()
    return dict(row) if row else None
```

### Raise Instead of Return None

```python
def get_note(note_id: int) -> dict:
    """Get a note by ID, raises NotFoundError if not found."""
    row = cursor.fetchone()
    if row is None:
        raise NotFoundError("note", note_id)
    return dict(row)
```

## LLM Integration Patterns

### Structured Output

```python
from ollama import chat
import json

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
    model="llama3.1:8b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ],
    format='json',  # Enable JSON mode
    options={'temperature': 0.1}
)
```

### Post-Processing Pipeline

```python
def post_process_items(items: list[str]) -> list[str]:
    # 1. Clean whitespace
    items = [item.strip() for item in items]
    
    # 2. Filter empty
    items = [item for item in items if item]
    
    # 3. Deduplicate (preserve order)
    seen = set()
    unique_items = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique_items.append(item)
    
    # 4. Validate length
    return [item for item in unique_items if len(item) > 3]
```

### Graceful Error Handling

```python
import logging

logger = logging.getLogger(__name__)

def extract_with_fallback(text: str) -> list[str]:
    try:
        return extract_action_items_llm(text)
    except httpx.ConnectError:
        logger.warning("Ollama not available")
        return []
    except json.JSONDecodeError as e:
        logger.warning(f"Invalid JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []
```

## Testing Patterns

### Mock External Dependencies

```python
from unittest.mock import patch

@patch('week2.app.services.extract.chat')
def test_extract_fast(mock_chat):
    mock_chat.return_value = {
        'message': {'content': '{"action_items": ["Task 1"]}'}
    }
    result = extract_action_items_llm("test")
    assert result == ["Task 1"]
```

### Semantic Assertions for LLM

```python
@pytest.mark.slow
def test_real_llm():
    result = extract_action_items_llm("- Fix bug")
    
    # Semantic assertion (allows variation)
    assert len(result) >= 1
    assert any("bug" in item.lower() for item in result)
```

### Parametrized Tests

```python
@pytest.mark.parametrize("text,expected_count", [
    ("- Task 1\n- Task 2", 2),
    ("TODO: Fix bug", 1),
    ("No actions", 0),
])
def test_extraction(text, expected_count):
    result = extract_action_items(text)
    assert len(result) == expected_count
```

## Logging Patterns

### Replace Print with Logging

```python
import logging

logger = logging.getLogger(__name__)

# Before
print(f"Processing: {text}")

# After
logger.info(f"Extracting from text (len={len(text)})")
logger.debug(f"Items: {items}")
logger.warning("Ollama not available")
logger.error(f"Database error: {e}")
```

### Log Levels

| Level | Usage | Example |
|-------|-------|---------|
| DEBUG | Detailed diagnostics | `logger.debug(f"Items: {items}")` |
| INFO | Key flow events | `logger.info("Starting extraction")` |
| WARNING | Recoverable issues | `logger.warning("Ollama unavailable")` |
| ERROR | Errors with recovery | `logger.error(f"DB error: {e}")` |
| CRITICAL | Unrecoverable failures | `logger.critical("Cannot start server")` |

## Import Patterns

### Relative Imports (Package Files)

```python
# In week2/tests/test_extract.py
from ..app.services.extract import extract_action_items_llm
```

### Absolute Imports (Root Scripts)

```python
# In scripts at project root
from week2.app.services.extract import extract_action_items_llm
```

## Router Patterns

### Clean Router Functions

```python
@router.post("/action-items", response_model=List[ActionItemResponse])
def list_all():
    """List all action items."""
    items = db.get_all_action_items()
    return [ActionItemResponse.from_dict(item) for item in items]
```

### Path Parameters

```python
@router.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int):
    """Get a note by ID."""
    note = db.get_note(note_id)
    return NoteResponse.from_dict(note)
```

### Query Parameters

```python
@router.get("/action-items")
def list_items(done: Optional[bool] = None):
    """List items, optionally filtered by done status."""
    items = db.get_action_items(done=done)
    return items
```

## Related Files

- Testing patterns: `practice/testing_patterns.md`
- Exception handling: `practice/exception_handling.md`
- Import guide: `reference/imports_guide.md`
