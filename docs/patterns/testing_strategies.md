---
pattern: testing_strategies
title: "Testing Strategies for AI-Assisted Development"
type: pattern
status: draft
created: 2026-01-02
updated: 2026-01-02
related:
  - patterns/automation_design.md
tags: [testing, pytest, quality, patterns]
---

# Testing Strategies

> **Navigation**: [CS146S Docs](../INDEX.md) > [Patterns](../patterns/) > Testing Strategies

> **Status**: Template - To be populated by Agent C with testing patterns from all weeks

## Overview

Testing in AI-assisted development requires both traditional software testing practices and new approaches for validating AI-generated code. This document captures proven testing strategies.

## Testing Pyramid

```
        ▲
       / \
      / E2E \        ← High-level integration tests
     /-------\
    /  Integration  \  ← API and service integration
   /-----------------\
  /     Unit Tests    \ ← Individual function/component tests /___________________\
```

## Test Organization Patterns

### Pattern 1: [Test Organization Pattern]
**Problem**: [What problem does it solve?]

**Solution**: [Directory structure and naming conventions]

**Example**:
```
tests/
├── unit/
│   ├── test_component1.py
│   └── test_component2.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── e2e/
    └── test_user_flow.py
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

## Unit Testing Patterns

### Pattern: Test Data Builders
**Problem**: Complex test setup makes tests brittle

**Solution**: Use builder pattern for test data

**Example**:
```python
# Before: Repetitive setup
def test_note_creation():
    note = Note(
        title="Test",
        content="Content",
        user_id=1,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

# After: Builder pattern
def test_note_creation():
    note = NoteBuilder()\
        .with_title("Test")\
        .with_content("Content")\
        .build()
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

### Pattern: Parametrized Tests
**Problem**: Similar test cases with different inputs

**Solution**: Use pytest parametrization

**Example**:
```python
@pytest.mark.parametrize("input,expected", [
    ("valid input", "expected output"),
    ("another input", "another output"),
])
def test_function(input, expected):
    assert function(input) == expected
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

## Integration Testing Patterns

### Pattern: Test Database Fixtures
**Problem**: Tests need consistent database state

**Solution**: Use pytest fixtures with proper cleanup

**Example**:
```python
@pytest.fixture
def clean_db(test_db):
    # Setup: Create test data
    db.create_test_note(title="Test")
    yield test_db
    # Teardown: Clean up
    test_db.execute("DELETE FROM notes")
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

### Pattern: Mock External Services
**Problem**: Tests shouldn't depend on external APIs

**Solution**: Use mocks for external dependencies

**Example**:
```python
def test_with_mocked_llm(monkeypatch):
    def mock_llm(prompt):
        return "Test response"
    monkeypatch.setattr("app.services.llm.call", mock_llm)
    # Now test your code without calling real LLM
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

## Testing AI-Generated Code

### Challenge: Validating AI Output
**Problem**: AI-generated code may have subtle bugs

**Strategies**:

1. **Comprehensive Unit Tests**
   - Test edge cases the AI might miss
   - Validate error handling
   - Check boundary conditions

2. **Integration Testing**
   - Verify AI code works with real dependencies
   - Test API contracts
   - Validate database interactions

3. **Manual Review**
   - Code review checklist for AI-generated code
   - Security vulnerability scan
   - Performance profiling

**Example from Week N**:
- AI generated: [What code]
- Issue found: [What was wrong]
- Test added: [What test caught it]
- Lesson: [How to prevent]

---

## Coverage Strategies

### Pattern: Coverage Targets
**Week-by-week coverage goals**:

| Week | Coverage Target | Actual | Notes |
|------|----------------|--------|-------|
| Week 1 | 80% | [X]% | [Notes] |
| Week 2 | 85% | [X]% | [Notes] |
| Week 3 | 90% | [X]% | [Notes] |

**Best practices**:
- Focus coverage on business logic, not boilerplate
- Test error paths, not just happy paths
- Use coverage reports to identify gaps

**Tools**:
- `pytest --cov=module_name`
- Coverage HTML reports: `--cov-report=html`

---

## Test Automation

### Pattern: Pre-commit Tests
**Problem**: Developers forget to run tests

**Solution**: Automate test execution in git hooks

**Example** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: Run tests
        entry: pytest weeks/weekN/tests/
        language: system
        pass_filenames: false
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

### Pattern: Continuous Integration
**Problem**: Catch integration issues early

**Solution**: Run tests on every push

**Example** (`.github/workflows/test.yml`):
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

---

## Common Testing Pitfalls

### Pitfall 1: Brittle Tests
**Problem**: Tests break when implementation changes

**Solution**: Test behavior, not implementation

**Example**:
```python
# Bad: Tests implementation details
def test_note_uses_sqlalchemy():
    assert note.session == expected_session

# Good: Tests behavior
def test_note_can_be_saved():
    saved_note = note.save()
    assert saved_note.id is not None
```

---

### Pitfall 2: Slow Tests
**Problem**: Tests take too long to run

**Solution**: Use mocks, fixtures, and parallel execution

**Strategies**:
- Mock external dependencies
- Use in-memory databases for unit tests
- Run tests in parallel: `pytest -n auto`

---

### Pitfall 3: Testing Everything
**Problem**: Trying to test 100% coverage

**Solution**: Focus on high-value tests

**Priority**:
1. Business logic (high value)
2. Error handling (high value)
3. Edge cases (medium value)
4. Getters/setters (low value)

---

## Testing Checklist

Before considering code "done":

- [ ] Unit tests for all business logic
- [ ] Integration tests for API endpoints
- [ ] Error path tests
- [ ] Edge case tests
- [ ] Tests for AI-generated code
- [ ] Coverage report reviewed
- [ ] All tests passing locally
- [ ] Pre-commit hooks configured
- [ ] CI tests passing (if applicable)

---

## Quick Reference

### Common pytest Commands

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=module_name

# Run specific test file
pytest tests/test_specific.py

# Run specific test function
pytest tests/test_specific.py::test_function

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run in parallel
pytest -n auto

# Generate HTML coverage report
pytest --cov=module_name --cov-report=html
```

---

*[Template created 2026-01-02 - Agent C will populate with testing patterns extracted from all weeks]*
