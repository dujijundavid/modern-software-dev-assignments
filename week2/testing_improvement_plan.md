# Testing Improvement Plan for Week2 Project

## Current State (Before Implementation)

| Metric | Value |
|--------|-------|
| Tests Passed | 26/26 |
| Overall Coverage | 85% |
| Duration | 13.20s |
| Critical Gaps | main.py (0%), extract.py (75%), action_items.py (75%), db.py (80%) |

## Implementation Strategy: 3-Phase Approach

### Phase 1: High Priority (Critical Coverage Gaps) ✅ COMPLETE

**Goal:** Address 0% coverage in main.py and critical error paths

#### 1.1 Create `week2/tests/test_main.py` ✅
- Tests for exception handlers (NotFoundError, DatabaseError)
- Static file serving tests
- Router integration tests
- Application configuration validation
- **Result:** main.py 0% → 100%

#### 1.2 Enhance `week2/tests/test_extract.py` ✅
Added 43 edge case tests for:
- Line 44: Short line filtering (< 3 chars)
- Line 52: Question filtering
- Line 56: Gibberish filtering (< 3 unique chars)
- Line 61: Symbol-heavy content filtering
- Lines 136-155: Imperative sentence detection
- Lines 263-264: Type validation for LLM responses
- Lines 279-280: Vague single-word filtering
- **Result:** extract.py 75% → 98%

#### 1.3 Create `week2/tests/test_action_items_llm.py` ✅
- LLM endpoint tests (`/extract-llm` - lines 64-80)
- Mock LLM integration with database
- Error handling and propagation
- Response schema validation
- **Result:** action_items.py 75% → 100%

**Phase 1 Results:**
- Total Tests: 107 passed (from 26 - added 81 tests)
- Overall Coverage: 97% (from 85%)
- Duration: 11.85s

---

### Phase 2: Medium Priority (Database Layer) 🔄 IN PROGRESS

**Goal:** Increase db.py coverage from 82% to 95%

#### 2.1 Create `week2/tests/test_db_errors.py`
- Database connection error scenarios
- SQLite exception wrapping (OperationalError, IntegrityError)
- Empty result set handling
- Connection pool validation
- Directory creation tests

#### 2.2 Create `week2/tests/test_db_constraints.py`
- Foreign key constraint validation
- NOT NULL constraint tests
- Data type validation
- Auto-increment verification
- Transaction rollback tests

---

### Phase 3: Low Priority (Testing Infrastructure)
**Goal:** Introduce advanced testing patterns

#### 3.1 Create `week2/conftest.py`
Shared fixtures for:
- Automatic test database isolation (`tmp_path`)
- Sample data fixtures
- Mock fixtures
- Database state fixtures
- Pytest marker configuration

#### 3.2 Create `week2/tests/test_extract_properties.py`
Property-based tests using Hypothesis:
- Return type invariants
- Deduplication properties
- String formatting invariants
- Idempotence properties

#### 3.3 Create `week2/tests/test_integration.py`
End-to-end workflow tests:
- Full extract → save → list workflows
- Multi-note filtering
- Concurrent operations
- Error propagation through stack

---

## Testing Patterns to Adopt

### 1. Fixture-Based Test Data Management
```python
# conftest.py
@pytest.fixture
def sample_note_text():
    return "- Task 1\n- Task 2\n- Task 3"
```

### 2. Parameterized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("- Valid task", True),
    ("- ?", False),
])
def test_edge_cases(input, expected):
    assert _is_action_line(input) == expected
```

### 3. Property-Based Testing (Hypothesis)
```python
@given(st.text())
def test_always_returns_list(text):
    result = extract_action_items(text)
    assert isinstance(result, list)
```

### 4. Test Marker Strategy
```python
@pytest.mark.slow
def test_llm_integration(): pass

@pytest.mark.integration
def test_full_workflow(): pass
```

Usage: `pytest -m "not slow"` or `pytest -m "unit"`

---

## Expected Coverage Improvements

| Module | Before Phase 1 | After Phase 1 | After Phase 2 | After Phase 3 |
|--------|----------------|---------------|---------------|---------------|
| main.py | 0% | 100% | 100% | 100% |
| extract.py | 75% | 98% | 98% | 98% |
| action_items.py | 75% | 100% | 100% | 100% |
| db.py | 80% | 82% | 95% | 95% |
| notes.py | 89% | 89% | 89% | 89% |
| **Overall** | **85%** | **97%** | **97%+** | **98%** |

---

## Critical Files

| File | Priority | Purpose |
|------|----------|---------|
| `week2/tests/test_main.py` | Phase 1 ✅ | Address 0% main.py coverage |
| `week2/tests/test_extract.py` | Phase 1 ✅ | Edge case coverage |
| `week2/tests/test_action_items_llm.py` | Phase 1 ✅ | LLM endpoint coverage |
| `week2/tests/test_db_errors.py` | Phase 2 🔄 | Database error handling |
| `week2/tests/test_db_constraints.py` | Phase 2 | Constraint validation |
| `week2/conftest.py` | Phase 3 | Shared fixtures foundation |

---

## Dependencies

```toml
# pyproject.toml additions
[tool.poetry.dev-dependencies]
pytest-cov = "^7.0.0"  # ✅ Already added
hypothesis = "^6.0"    # For property-based testing (Phase 3)
```

---

## Implementation Order

1. ✅ **Phase 1** - Addresses most critical gaps
2. 🔄 **Phase 2** - Database layer robustness (Current)
3. ⏳ **Phase 3** - Advanced patterns and infrastructure

Each phase can be implemented independently and provides immediate value.
