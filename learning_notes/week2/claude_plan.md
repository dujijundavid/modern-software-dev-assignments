# Exception Handling Refactoring Plan

## Overview

Minimal changes to fix core exception handling issues in week2 codebase:
1. Implement `NotFoundError` usage (currently unused)
2. Add context to exception classes (currently empty `pass`)
3. Add HTTP status code mapping for custom exceptions
4. Eliminate duplicated response building code

---

## Critical Files to Modify

| File | Changes |
|------|---------|
| `week2/app/db.py` | Exception classes + `get_note()` + `mark_action_item_done()` |
| `week2/app/main.py` | Add global exception handlers |
| `week2/app/schemas.py` | Add `from_dict()` class methods |
| `week2/app/routers/notes.py` | Simplify using `from_dict()`, remove manual None checks |
| `week2/app/routers/action_items.py` | Simplify using `from_dict()` |

---

## Detailed Changes

### 1. `week2/app/db.py` (lines 17-24)

Enhance exception classes with context:

```python
class DatabaseError(Exception):
    """Custom exception for database operations."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(Exception):
    """Exception for resource not found errors."""
    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message)
```

### 2. `week2/app/db.py` - `get_note()` (lines 98-114)

Raise `NotFoundError` instead of returning `None`:

```python
def get_note(note_id: int) -> dict:
    """Get a single note by ID.

    Raises:
        NotFoundError: If note with given ID doesn't exist
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            if row is None:
                raise NotFoundError("note", note_id)
            return dict(row)
    except sqlite3.Error as e:
        logger.error(f"Failed to get note {note_id}: {e}")
        raise DatabaseError(f"Failed to get note: {e}") from e
```

### 3. `week2/app/db.py` - `mark_action_item_done()` (lines 163-178)

Add existence check with `rowcount`:

```python
def mark_action_item_done(action_item_id: int, done: bool) -> None:
    """Mark an action item as done or undone.

    Raises:
        NotFoundError: If action item with given ID doesn't exist
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            if cursor.rowcount == 0:
                raise NotFoundError("action item", action_item_id)
            connection.commit()
    except sqlite3.Error as e:
        logger.error(f"Failed to mark action item {action_item_id}: {e}")
        raise DatabaseError(f"Failed to mark action item: {e}") from e
```

### 4. `week2/app/schemas.py`

Add `from_dict()` class methods to both response schemas:

```python
class NoteResponse(BaseModel):
    """Response schema for note data."""
    id: int
    content: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "NoteResponse":
        """Create NoteResponse from database dict."""
        return cls(**data)


class ActionItemResponse(BaseModel):
    """Response schema for a single action item."""
    id: int
    text: str
    note_id: Optional[int] = None
    done: bool = False
    created_at: str

    @classmethod
    def from_dict(cls, data: dict) -> "ActionItemResponse":
        """Create ActionItemResponse from database dict."""
        return cls(
            id=data["id"],
            text=data["text"],
            note_id=data.get("note_id"),
            done=bool(data["done"]),
            created_at=data["created_at"],
        )
```

### 5. `week2/app/main.py`

Add global exception handlers (before `@app.get("/")`):

```python
from fastapi.responses import JSONResponse
from . import db


@app.exception_handler(db.NotFoundError)
async def notfound_error_handler(request, exc: db.NotFoundError):
    """Handle NotFoundError - return 404 status."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(db.DatabaseError)
async def database_error_handler(request, exc: db.DatabaseError):
    """Handle DatabaseError - return 500 status."""
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message},
    )
```

### 6. `week2/app/routers/notes.py`

Simplify endpoints by removing manual None checks (now handled globally):

```python
@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreate) -> NoteResponse:
    """Create a new note."""
    note_id = db.insert_note(payload.content)
    note = db.get_note(note_id)
    return NoteResponse.from_dict(note)


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    """Get a single note by ID."""
    row = db.get_note(note_id)
    return NoteResponse.from_dict(row)
```

Remove unused `HTTPException` import.

### 7. `week2/app/routers/action_items.py`

Use `from_dict()` to eliminate duplication:

```python
# In extract() endpoint
return ExtractResponse(
    note_id=note_id,
    items=[
        ActionItemResponse.from_dict(created_items_map[item_id])
        for item_id in ids
    ],
)

# In list_all()
return [ActionItemResponse.from_dict(r) for r in rows]

# In extract_llm() endpoint
return ExtractResponse(
    note_id=note_id,
    items=[
        ActionItemResponse.from_dict(created_items_map[item_id])
        for item_id in ids
    ],
)
```

Remove unused `HTTPException` import.

---

## Error Flow Comparison

### Before: Non-existent note
```
db.get_note(999) -> returns None
    -> router checks `if row is None`
    -> router raises HTTPException(404)
```

### After: Non-existent note
```
db.get_note(999) -> raises NotFoundError("note", 999)
    -> global handler catches NotFoundError
    -> returns JSONResponse(404, {"detail": "note with id 999 not found"})
```

---

## Verification Tests

After implementation:

1. `GET /notes/999` → 404
2. `POST /action-items/999/done` → 404
3. `pytest week2/tests/test_refactoring.py` → pass
