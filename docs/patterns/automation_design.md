---
pattern: automation_design
title: "Automation Design Patterns"
type: pattern
status: draft
created: 2026-01-02
updated: 2026-01-02
related:
  - patterns/prompting.md
  - patterns/multi_agent_coordination.md
tags: [automation, workflows, ai-engineering, patterns]
---

# Automation Design Patterns

> **Navigation**: [CS146S Docs](../INDEX.md) > [Patterns](../patterns/) > Automation Design

> **Status**: Template - To be populated by Agent C with automation patterns from Week 5+ reflections

## Overview

Building effective automations is a core AI Engineering skill. This document captures proven patterns for designing, implementing, and improving automations.

## The Automation Hierarchy

```
Level 4: Self-Improving
    ↓ Automations that discover and optimize their own bottlenecks

Level 3: Composable System
    ↓ Automations that can be combined and chained

Level 2: Reusable Function
    ↓ Parameterized automations for similar tasks

Level 1: One-off Script
    ↓ Solves a specific problem once
```

**Goal**: Always aim for Level 3+, with clear path to Level 4.

---

## Design Principles

### Principle 1: The Three Questions

Before building any automation, ask:

1. **What's the bottleneck?**
   - What repetitive, low-value work are you doing?
   - What causes context switching?
   - What errors do you make repeatedly?

2. **What's the leverage point?**
   - How can this be automated to be reusable?
   - How can it be parameterized, not hardcoded?
   - What's the minimum viable automation?

3. **How to compound value?**
   - How does this combine with other automations?
   - What's the input/output contract?
   - How can this be used by others?

### Principle 2: Design for Failure

Assume your automation will fail. Design for it:

- Clear error messages
- Rollback mechanisms
- Idempotent operations (can run multiple times safely)
- Logging and audit trails

### Principle 3: Start Small, Scale Up

1. Build a one-off script (Level 1)
2. Generalize to reusable function (Level 2)
3. Design for composition (Level 3)
4. Add self-improvement (Level 4)

---

## Automation Patterns

### Pattern 1: Environment Health Check
**Level**: 2 (Reusable Function)

**Problem**: Environment issues waste time switching contexts

**Solution**: Automated health check script

**Input**: None (runs on current environment)

**Output**: Status report with ✅/❌ for each check

**Implementation**:
```bash
#!/bin/bash
# Checks:
# 1. Python version >= 3.10
# 2. poetry.lock up to date
# 3. Tests discoverable
# 4. Database exists
# 5. Server responds
```

**Used in**: [Week 5](../weeks/week5/implementation.md)

**Time saved**: 10-15 minutes per context switch

**Next evolution** (Level 3): Chain with test runner to validate before commits

---

### Pattern 2: Test Runner with Coverage
**Level**: 2 (Reusable Function)

**Problem**: Developers forget to run tests, or run them incompletely

**Solution**: Automated test runner with coverage reporting

**Input**: Test directory path

**Output**: Test results + coverage report

**Implementation**:
```bash
#!/bin/bash
pytest $1 --cov=$2 --cov-report=html --cov-report=term
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

**Time saved**: 5-10 minutes per test run

**Next evolution** (Level 3): Pre-commit hook integration

---

### Pattern 3: Format + Lint Pipeline
**Level**: 2 (Reusable Function)

**Problem**: Code quality checks are manual and inconsistent

**Solution**: Automated formatting and linting pipeline

**Input**: File or directory to check

**Output**: Formatted code + lint report

**Implementation**:
```bash
#!/bin/bash
black $1
ruff check $1 --fix
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

**Time saved**: 5-10 minutes per commit

**Next evolution** (Level 3): Pre-commit hook with auto-fix

---

### Pattern 4: API Response Standardization
**Level**: 3 (Composable System)

**Problem**: Inconsistent error handling across endpoints

**Solution**: Response wrapper with standard envelope

**Input**: Endpoint path, model name

**Output**: Wrapped response with consistent structure

**Implementation**:
```python
# Success: {"ok": true, "data": {...}}
# Error: {"ok": false, "error": {"code": "NOT_FOUND", "message": "..."}}
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

**Composability**: Works with any endpoint, any model

**Next evolution** (Level 4): Auto-generate wrappers from OpenAPI spec

---

### Pattern 5: Pagination Pattern
**Level**: 3 (Composable System)

**Problem**: Reimplementing pagination for every endpoint

**Solution**: Reusable pagination mixin

**Input**: Query, page, page_size

**Output**: Paginated results with metadata

**Implementation**:
```python
def paginate(query, page=1, page_size=10):
    total = query.count()
    items = query.offset((page-1)*page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}
```

**Used in**: [Week N](../weeks/weekN/implementation.md)

**Composability**: Works with any SQLAlchemy query

**Next evolution** (Level 4): Auto-apply based on query parameters

---

## Anti-Patterns

### Anti-Pattern 1: Hard-Coded Values
**Problem**: Automation only works in one specific context

**Example**:
```python
# Bad
PORT = 8000
HOST = "localhost"

# Good
PORT = os.getenv("API_PORT", "8000")
HOST = os.getenv("API_HOST", "localhost")
```

**How to avoid**: Parameterize everything

---

### Anti-Pattern 2: Silent Failures
**Problem**: Automation fails but doesn't report errors

**Example**:
```python
# Bad
try:
    risky_operation()
except:
    pass  # Swallows all errors

# Good
try:
    risky_operation()
except Exception as e:
    logger.error(f"Automation failed: {e}")
    raise  # Or handle gracefully
```

**How to avoid**: Explicit error handling and logging

---

### Anti-Pattern 3: Brittle Dependencies
**Problem**: Automation breaks when environment changes

**Example**:
```python
# Bad: Assumes specific file structure
with open("data/output.json") as f:
    data = json.load(f)

# Good: Validates environment
output_path = Path("data/output.json")
if not output_path.exists():
    raise FileNotFoundError(f"Expected output at {output_path}")
with open(output_path) as f:
    data = json.load(f)
```

**How to avoid**: Validate preconditions, fail fast

---

## Automation Evaluation Rubric

Score each automation on these dimensions (1-5 each):

### Reusability
- 1 = One-off, hardcoded
- 3 = Can be used for similar tasks with minor tweaks
- 5 = Fully parameterized, works for any similar task

### Composability
- 1 = Standalone, can't combine with others
- 3 = Can be chained manually
- 5 = Designed to compose, has clear input/output contracts

### Autonomy
- 1 = Requires constant human intervention
- 3 = Runs autonomously with supervision
- 5 = Fully autonomous, handles edge cases and self-recovers

### Robustness
- 1 = Fails silently or catastrophically
- 3 = Fails gracefully with errors
- 5 = Handles errors, rolls back, reports issues

**Total Score**: ___ / 20
**Target**: 12+ for each automation

---

## Automation Design Checklist

Before building an automation:

### Planning
- [ ] Answered The Three Questions
- [ ] Identified bottleneck
- [ ] Defined input/output contract
- [ ] Planned for failure modes

### Design
- [ ] Parameterized (not hardcoded)
- [ ] Clear error handling
- [ ] Idempotent operations
- [ ] Logging and audit trails

### Implementation
- [ ] Follows existing patterns
- [ ] Documented with examples
- [ ] Tested with edge cases
- [ ] Version controlled

### Validation
- [ ] Runs successfully 5 times in a row
- [ ] Handles errors gracefully
- [ ] Clear error messages
- [ ] Achieves target score (12+/20)

---

## Real-World Automation Examples

### Example 1: Week 5 Environment Health Check
**Problem**: 10-15 minutes wasted each context switch

**Solution**: Automated health check script

**Implementation**: [See Week 5](../weeks/week5/implementation.md)

**Results**:
- Time saved: 10-15 minutes per switch
- Reliability: 100% (passes 5/5 runs)
- Score: 15/20

**Next iteration**: Add auto-fix for common issues

---

### Example 2: Multi-Agent Task Runner
**Problem**: Coordinating 3 agents working on different tasks

**Solution**: Git worktree + shared contract approach

**Implementation**: [See Week 5](../weeks/week5/implementation.md)

**Results**:
- Parallel execution: 3 agents working simultaneously
- Validation: Agent C validates A and B before merge
- Rollback: If validation fails, revert all changes

**Score**: 17/20

**Next iteration**: Add automated conflict resolution

---

## Quick Reference

### Automation Levels Quick Check

| Level | Name | Key Characteristic | Example |
|-------|------|-------------------|---------|
| 1 | One-off Script | Solves specific problem | Bash script for one-time task |
| 2 | Reusable Function | Parameterized | Function with arguments |
| 3 | Composable System | Clear I/O contract | Can chain with other automations |
| 4 | Self-Improving | Discovers own bottlenecks | Optimizes itself over time |

### Tool Choices by Use Case

| Use Case | Recommended Tool | Why |
|----------|------------------|-----|
| File operations | Bash scripts | Simple, ubiquitious |
| API automation | Python + requests | Easy HTTP, good error handling |
| Code generation | Jinja2 templates | Parameterized, composable |
| Workflows | Make/Just | Dependency management |
| CI/CD | GitHub Actions | Integrated with git |

---

*[Template created 2026-01-02 - Agent C will populate with automation patterns extracted from Week 5+ reflections]*
