# Refactoring Journey: From Working to Professional

> **Goal**: Transform "working code" into maintainable, professional code

## The Starting Point

### Problem Diagnosis

| Symptom | Issue | Impact |
|---------|-------|--------|
| `Dict[str, Any]` types | No type checking | Runtime errors |
| Manual validation | Repetitive if-checks | Easy to miss cases |
| `sqlite3.Row` returns | Leaks DB implementation | Tight coupling |
| Print statements | No log level control | Production noise |
| Empty exception classes | No context | Hard to debug |

## Refactoring Strategy

### Design Principles

```
Layered Architecture:
┌─────────────────────┐
│   Router Layer      │ ← Pydantic models: type-safe entry
├─────────────────────┤
│   Service Layer     │ ← Business logic (extract.py)
├─────────────────────┤
│   Database Layer    │ ← Returns dict, hides implementation
└─────────────────────┘
```

**Core ideas**:
1. **Single responsibility** - Each layer does one thing
2. **Abstract upward** - Lower layers provide simple interfaces
3. **Type safety** - Catch errors early

## Step-by-Step Changes

### Step 1: Pydantic Schemas

```python
# Before
@router.post("/extract")
def extract(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = str(payload.get("text", "")).strip()
    if not text:
        raise HTTPException(400, "text required")
    return {"items": [...]}

# After
class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1)
    save_note: bool = Field(default=False)

class ActionItemResponse(BaseModel):
    id: int
    text: str
    note_id: Optional[int]
    done: bool
    created_at: str

@router.post("/extract", response_model=ExtractResponse)
def extract(payload: ExtractRequest) -> ExtractResponse:
    # text auto-validated!
    items = extract_action_items(payload.text)
    return ExtractResponse(items=[...])
```

### Step 2: Database Returns Dict

```python
# Before - exposes sqlite3.Row
def get_note(note_id: int) -> Optional[sqlite3.Row]:
    return cursor.fetchone()

# After - returns dict
def get_note(note_id: int) -> Optional[dict]:
    row = cursor.fetchone()
    return dict(row) if row else None
```

### Step 3: Enhanced Exceptions

```python
# Before
class DatabaseError(Exception):
    pass

class NotFoundError(Exception):
    pass

# After
class DatabaseError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class NotFoundError(Exception):
    def __init__(self, resource_type: str, resource_id: int):
        self.resource_type = resource_type
        self.resource_id = resource_id
        message = f"{resource_type} with id {resource_id} not found"
        super().__init__(message)
```

### Step 4: Factory Method

```python
# Before - repetitive construction
return ExtractResponse(
    items=[
        ActionItemResponse(
            id=item_id,
            text=created_items_map[item_id]["text"],
            note_id=created_items_map[item_id]["note_id"],
            done=bool(created_items_map[item_id]["done"]),
            created_at=created_items_map[item_id]["created_at"],
        )
        for item_id in ids
    ],
)

# After - clean factory method
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

return ExtractResponse(
    items=[ActionItemResponse.from_dict(created_items_map[item_id]) for item_id in ids]
)
```

### Step 5: Global Exception Handler

```python
# main.py
@app.exception_handler(db.NotFoundError)
async def notfound_error_handler(request, exc: db.NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

## Results Comparison

| Dimension | Before | After |
|-----------|--------|-------|
| Type safety | Dict[str, Any] | Pydantic models |
| Input validation | Manual if checks | Auto validation |
| DB coupling | Router knows sqlite3.Row | Router only knows dict |
| Error handling | Raw sqlite exceptions | DatabaseError wrapper |
| Logging | print() everywhere | logging with levels |
| Testability | Hard (specific types) | Easy (clear interfaces) |

## Error Flow Evolution

### Before: Scattered handling
```
db.get_note(999)
    ↓
returns None
    ↓
router checks `if row is None`
    ↓
router raises HTTPException(404)
```

### After: Centralized handling
```
db.get_note(999)
    ↓
raises NotFoundError("note", 999)
    ↓
global handler catches it
    ↓
returns JSONResponse(404, {"detail": "note with id 999 not found"})
```

## Testing the Refactoring

```python
def test_schema_validation():
    """Test Pydantic auto-validation"""
    with pytest.raises(ValidationError):
        ExtractRequest(text="")  # min_length=1 should fail

def test_db_returns_dict():
    """Test DB layer return type"""
    note = db.get_note(1)
    assert isinstance(note, dict)  # not sqlite3.Row
    assert "id" in note

def test_exception_context():
    """Test exception carries context"""
    with pytest.raises(db.NotFoundError) as exc:
        db.get_note(999)
    assert exc.value.resource_type == "note"
    assert exc.value.resource_id == 999
```

## Key Takeaways

1. **Start with schemas** - Define data contracts first
2. **Hide implementation** - DB layer returns dict, not Row
3. **Enhanced exceptions** - Carry context, not just messages
4. **Factory methods** - Eliminate repetitive construction
5. **Centralized handling** - Global handlers vs scattered if-checks
6. **Small changes** - Each step independently testable

## Related Files

- Exception handling: `practice/exception_handling.md`
- Code patterns: `reference/code_patterns.md`
- LLM integration: `practice/llm_integration.md`
