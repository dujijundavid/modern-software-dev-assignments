# Multi-Agent Systems: Coordination & Design

> **Navigation**: [CS146S Docs](INDEX.md) > [Core Concepts](.) > Multi-Agent Systems

> **Learning Outcomes**: Master SubAgents coordination patterns, handoff protocols, and design principles for building composable AI workflows

---

## Quick Reference

### What Are Multi-Agent Systems?

Multi-agent systems (MAS) coordinate multiple specialized AI agents to complete complex tasks through collaboration, not just computation. Each agent has a specific role, clear responsibilities, and well-defined interfaces for communication.

**Key characteristics**:
- **Specialization**: Each agent excels at one domain
- **Separation of concerns**: Testing vs. implementation vs. review
- **Structured communication**: Handoff protocols prevent ambiguity
- **Composability**: Agents combine to create workflows

### When to Use Multi-Agent Systems

```yaml
✅ Use MAS when:
  - Task requires multiple mindsets (TDD: test then implement)
  - Different expertise needed (API design + security + testing)
  - Workflow benefits from verification loops
  - Task is too complex for one agent

❌ Don't use MAS when:
  - Simple, single-step tasks
  - Task doesn't benefit from specialization
  - Coordination overhead exceeds benefit
  - Tight coupling between steps
```

### Single Agent vs. Multi-Agent

| Dimension | Single Agent | Multi-Agent System |
|-----------|--------------|-------------------|
| **Complexity** | Low | Medium-High |
| **Specialization** | Generalist | Specialist roles |
| **Coordination** | None | Handoff protocols |
| **Verification** | Self-checking | Cross-agent validation |
| **Best For** | Simple tasks | Complex workflows |
| **Example** | `/llm-extract` | `/tdd-cycle` |

---

## Core Patterns

### SubAgent Coordination

#### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Agent (Orchestrator)                │
│                   Coordinator + Router + Manager              │
│                                                              │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐  │
│  │  Task Route │  Context Mgmt│  Quality Gate│  Final Decision│  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────┐      ┌──────────┐     ┌─────────────┐
   │ Test    │      │ Code     │     │ Review      │
   │ Agent   │      │ Agent    │     │ Agent       │
   └─────────┘      └──────────┘     └─────────────┘
```

#### Coordination Pattern 1: Sequential Collaboration

**Use case**: Tasks where each step depends on the previous

```yaml
Workflow: Feature Development with TDD

Step 1: TestAgent
  role: Write comprehensive tests
  input: Feature requirements
  output: Test file + requirements specification

Step 2: CodeAgent
  role: Implement minimal code to pass tests
  input: Test file + requirements
  output: Implementation + test results

Step 3: TestAgent (verification)
  role: Verify implementation matches tests
  input: Implementation + test results
  output: Sign-off or feedback

Step 4: Orchestrator
  role: Provide completion summary
  input: All previous outputs
  output: Final status + next steps
```

**Example from `/tdd-cycle`**:
```python
# TestAgent writes this FIRST
def test_delete_note_success(db_session):
    note = Note(title="Test", content="Content")
    db_session.add(note)
    db_session.flush()

    response = client.delete(f"/notes/{note.id}")

    assert response.status_code == 204
    deleted_note = db_session.get(Note, note.id)
    assert deleted_note is None

# Then CodeAgent writes this
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
    return Response(status_code=204)
```

#### Coordination Pattern 2: Parallel Collaboration

**Use case**: Independent tasks that can run simultaneously

```yaml
Workflow: Multi-Module Development

PM Agent spawns:
  ├─► api-architect (API contract design)
  ├─► fastapi-expert (backend implementation)
  ├─► frontend-developer (UI components)
  └─► python-testing-expert (test framework)

All agents work in parallel → Results integrated by code-reviewer
```

**Key principles**:
- Each agent works in isolation (git worktrees or separate directories)
- Shared contract defines interfaces (OpenAPI spec, schemas)
- Final integration agent validates all work
- If validation fails, rollback all changes

#### Coordination Pattern 3: Agent Pool

**Use case**: Multiple agents with similar capabilities

```yaml
Testing Pool:
  - python-testing-expert (unit tests)
  - integration-test-expert (integration tests)
  - e2e-test-expert (end-to-end tests)

PM Agent selects based on:
  - Task type
  - Historical success rate
  - Current availability
```

### Handoff Protocols

#### What Are Handoff Protocols?

Handoff protocols are structured communication formats that agents use to pass work between each other. They prevent ambiguity, context loss, and miscommunication.

#### Protocol Design Principles

1. **Standardized structure**: Same format every time
2. **Complete context**: All necessary information included
3. **Clear next steps**: What the receiving agent should do
4. **Bidirectional**: Works in both directions

#### Example: TDD Handoff Protocol

**TestAgent → CodeAgent**:
```markdown
## TestAgent → CodeAgent Handoff

### Feature: DELETE /notes/{id}

### Tests Written
- `test_delete_note_success` - Verify note is deleted from database
- `test_delete_note_not_found` - Verify 404 returned for non-existent note
- `test_delete_note_unauthorized` - Verify auth check (if applicable)

### Implementation Requirements
1. Add DELETE endpoint at `/notes/{note_id}`
2. Query database for note by ID
3. Return 404 if note not found
4. Delete note and return 204 if found
5. Follow pattern in `app/routers/notes.py`

### Context
- Related models: `Note` in `app/models.py`
- Pattern to follow: `update_note` endpoint (same file)
- Database: SQLAlchemy with Session dependency
- Week: week4
```

**CodeAgent → TestAgent**:
```markdown
## CodeAgent → TestAgent Handoff

### Files Modified
1. `app/routers/notes.py` - Added `delete_note` endpoint

### Changes Made
- Added DELETE route handler at `/{note_id}`
- Implemented database query and deletion logic
- Added HTTP 404 error handling

### Test Results
- test_delete_note_success: ✅ PASS
- test_delete_note_not_found: ✅ PASS
- test_delete_note_unauthorized: ✅ PASS

### Ready for Verification
Please verify:
1. All tests pass ✅
2. Implementation matches requirements ✅
3. Code follows project patterns ✅
```

#### Handoff Protocol Template

```markdown
## [Source Agent] → [Target Agent] Handoff

### Feature/Task: [Name]

### [Relevant Section 1]
- [Item 1] - [Description]
- [Item 2] - [Description]

### [Relevant Section 2]
1. [Requirement 1]
2. [Requirement 2]

### Context
- [Context point 1]
- [Context point 2]
- [Pattern reference]
```

**Key sections**:
- **Feature/Task**: What is being worked on
- **Tests/Requirements**: What needs to be done
- **Context**: Environment, patterns, related files
- **Changes**: What was actually done
- **Results**: Test outcomes, verification status

### TDD with Agents

#### The TDD Challenge

Test-Driven Development requires discipline that often breaks down in practice:
- Cognitive conflict: "I just want to write the code"
- Context switching: Testing vs. implementation mindsets
- Temptation: "I'll write tests later"

#### Multi-Agent Solution

**Role Separation**:
- **TestAgent**: Only writes tests, never implementation
- **CodeAgent**: Only writes implementation, never tests
- **Orchestrator**: Manages workflow, ensures TDD discipline

**Enforced Discipline**:
- Agents cannot compromise their roles
- Verification loop ensures tests pass
- Orchestrator enforces completion standards

#### The TDD Cycle with SubAgents

```yaml
Phase 1: Test Agent (Red)
  input: Feature requirements
  action: Write comprehensive tests
  output: Test file (failing) + handoff
  validation: Tests fail as expected

Phase 2: Code Agent (Green)
  input: Test file + handoff
  action: Write minimal implementation
  output: Implementation + test results
  validation: All tests pass

Phase 3: Test Agent (Verify)
  input: Implementation + test results
  action: Verify implementation
  output: Sign-off or feedback
  validation: Quality standards met

Phase 4: Complete
  output: Completion summary + next steps
```

#### Real Example: Implementing DELETE Endpoint

**User invokes**:
```bash
/tdd-cycle Add DELETE /notes/{id} endpoint to delete notes
```

**Orchestrator delegates to TestAgent**:
```markdown
## Delegating to TestAgent

Please write comprehensive tests for DELETE /notes/{id} endpoint

**Requirements**:
- Delete note by ID
- Return 204 on success
- Return 404 if not found

**Context**:
- Week: week4
- Related files: app/routers/notes.py
- Pattern: Follow existing update_note endpoint

**Test Requirements**:
1. Write tests FIRST
2. Cover: success, not found, edge cases
3. Follow existing test patterns
4. Verify tests FAIL initially
```

**TestAgent writes tests**:
```python
# tests/test_notes.py
def test_delete_note_success(db_session):
    note = Note(title="Test", content="Content")
    db_session.add(note)
    db_session.flush()

    response = client.delete(f"/notes/{note.id}")

    assert response.status_code == 204
    deleted_note = db_session.get(Note, note.id)
    assert deleted_note is None


def test_delete_note_not_found():
    response = client.delete("/notes/99999")
    assert response.status_code == 404
```

**TestAgent provides handoff**:
```markdown
## TestAgent → CodeAgent Handoff

### Feature: DELETE /notes/{id}

### Tests Written
- test_delete_note_success - Verify deletion and 204 response
- test_delete_note_not_found - Verify 404 for non-existent note

### Implementation Requirements
1. Add DELETE endpoint at /notes/{note_id}
2. Query database for note
3. Return 404 if not found
4. Delete note and return 204 if found

### Context
- Model: Note in app/models.py
- Pattern: Similar to update_note in app/routers/notes.py
- Database: SQLAlchemy with Session dependency
```

**CodeAgent implements**:
```python
# app/routers/notes.py
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
    return Response(status_code=204)
```

**CodeAgent provides handoff**:
```markdown
## CodeAgent → TestAgent Handoff

### Files Modified
1. app/routers/notes.py - Added delete_note endpoint

### Test Results
- test_delete_note_success: ✅ PASS
- test_delete_note_not_found: ✅ PASS

### Ready for Verification
All tests pass. Implementation matches requirements.
```

**Orchestrator completes**:
```markdown
## TDD Cycle Complete

**Feature**: DELETE /notes/{id}
**Status**: ✅ READY FOR CODE REVIEW

### Summary
- Tests: 2 tests written
- Implementation: Complete
- All tests: PASSING
- Code review: Run code-reviewer before committing

### Files Modified
1. tests/test_notes.py - Tests added
2. app/routers/notes.py - Implementation added

### Next Steps
1. Run code-reviewer for quality check
2. Commit changes
3. Update documentation if needed
```

---

## Real-World Examples

### Example 1: TDD Cycle (Working Implementation)

**File**: [`.claude/commands/tdd-cycle.md`](../.claude/commands/tdd-cycle.md)

**What works well**:
- Clear role separation (TestAgent, CodeAgent, Orchestrator)
- Structured handoff protocol
- Enforced TDD discipline
- Verification loop

**Key design decisions**:
1. **Orchestrator doesn't write code**: Only coordinates
2. **TestAgent never writes implementation**: Enforced by instructions
3. **CodeAgent never modifies tests**: Enforced by constraints
4. **Bidirectional handoff**: TestAgent → CodeAgent → TestAgent

**Code structure**:
```yaml
4-Layer Prompt Model:
  Layer 1 (YAML): Metadata and tool permissions
  Layer 2 (Persona): Orchestrator role and responsibilities
  Layer 3 (Process): 7-step workflow (delegate, receive, verify)
  Layer 4 (Output): Completion summary format
```

**Why it works**:
- Each agent has clear constraints
- Handoff protocol is structured
- Verification loop ensures quality
- Orchestrator manages complexity

### Example 2: Architect Hub (With Design Flaws)

**Note**: The original `/architect-hub` command had critical design flaws identified in Week 4 reflection. These flaws provide valuable lessons.

**Intended purpose**: Module refactoring tool for renaming, moving, and updating imports

**Critical Design Flaws**:

1. **Command Interface Uses Natural Language**
   ```bash
   # Flawed design
   /architect-hub rename backend/app/services/extract.py to parser.py

   # Better design (proposed)
   /architect-hub --op=rename --source=backend/app/services/extract.py --dest=parser.py
   ```
   - **Problem**: Natural language is ambiguous, requires parsing
   - **Fix**: Use structured parameters for clarity and programmatic use

2. **Persona Lacks Executable Decision Framework**
   ```markdown
   # Flawed: Just describes role
   You are the Architect Hub, a specialized module refactoring assistant.

   # Better: Provides decision framework
   You are the Architect Hub. Decision rules:
   - IF single file rename → Use git mv
   - IF multi-file refactor → Create migration plan
   - IF imports affected → Update all import statements
   - IF tests fail → Rollback changes
   ```
   - **Problem**: Persona doesn't guide decision-making
   - **Fix**: Add if-then rules for common scenarios

3. **Process Is Idealized Without Error Handling**
   ```markdown
   # Flawed: Only shows happy path
   Process:
   1. Analyze module
   2. Request approval
   3. Execute refactor
   4. Verify changes

   # Better: Includes error branches
   Process:
   1. Analyze module
     - IF import not found → Report error
   2. Request approval
     - IF denied → Stop and report
   3. Execute refactor
     - IF git mv fails → Rollback and report
     - IF tests fail → Rollback and report
   4. Verify changes
     - IF lint fails → Fix automatically or report
   ```
   - **Problem**: No error handling, assumes everything works
   - **Fix**: Add error branches for every operation

4. **Fictional Examples, Not Validated**
   ```markdown
   # Flawed: Fictional examples
   Example: Rename backend/app/services/extract.py to parser.py
   [Idealized output without testing]

   # Better: Real examples with actual output
   Example: Actual run from week4 refactoring
   Input: /architect-hub --op=rename --source=...
   Output:
   [Real terminal output with errors encountered]
   ```
   - **Problem**: Examples hide flaws
   - **Fix**: Use real scenarios, test actual commands

**Lessons learned**:
- Design flaws are inevitable; critical analysis is essential
- Real-world validation catches issues that idealized design misses
- Structured parameters beat natural language for command interfaces
- Error handling is not optional; it's essential

---

## Design Principles

### What Makes Good Multi-Agent Systems?

#### Principle 1: Clear Role Separation

Each agent should have:
- **Single responsibility**: One job, done well
- **Clear boundaries**: What it does and doesn't do
- **No overlap**: Don't duplicate capabilities

```yaml
Good role separation:
  TestAgent: Writes tests, never implementation
  CodeAgent: Writes implementation, never tests
  Orchestrator: Coordinates, never writes code

Bad role separation:
  DeveloperAgent: Can do everything (no specialization)
  TestAgent: Can write tests AND implementation (blurred lines)
```

#### Principle 2: Structured Communication

Handoffs must be:
- **Standardized**: Same format every time
- **Complete**: Include all necessary context
- **Minimal**: No unnecessary information

```yaml
Good handoff:
  ## TestAgent → CodeAgent Handoff
  ### Feature: DELETE /notes/{id}
  ### Tests: 2 tests written
  ### Requirements: 3 requirements listed
  ### Context: Related files, patterns

Bad handoff:
  "Hey, I wrote some tests for that delete thing.
   The tests are in the test file. You know what to do."
```

#### Principle 3: Enforcement Mechanisms

Agents must:
- **Cannot compromise roles**: Built into instructions
- **Verification loops**: Check work quality
- **Completion standards**: Don't finish until done

```yaml
Good enforcement:
  TestAgent constraints:
    - MUST: Write tests first
    - MUST NOT: Write implementation code
    - MUST: Verify CodeAgent work

Bad enforcement:
  TestAgent: "Try to write tests first, but you can write code if needed"
```

#### Principle 4: Composability

Systems should:
- **Combine easily**: Agents work with other agents
- **Clear interfaces**: Well-defined inputs/outputs
- **Reusable patterns**: Apply to different domains

```yaml
Good composability:
  /tdd-cycle + /architect-hub = Refactor with tests
  /tdd-cycle + /explore-week = TDD with context
  /explore-week + code-archaeologist = Deep analysis

Bad composability:
  /build-feature: Does everything (can't combine)
  Agent A: Only works with Agent B (tight coupling)
```

#### Principle 5: Error Handling

Design for:
- **Failure modes**: What could go wrong?
- **Rollback mechanisms**: How to undo changes?
- **Recovery strategies**: How to continue after errors?

```yaml
Good error handling:
  Process:
    1. Analyze
       - IF error → Report and stop
    2. Execute
       - IF failure → Rollback and report
    3. Verify
       - IF tests fail → Retry or rollback

Bad error handling:
  Process:
    1. Analyze
    2. Execute
    3. Verify
    (Assumes everything works)
```

### Design Checklist

Before implementing a multi-agent system, ask:

```markdown
## Role Design
- [ ] Does each agent have a single responsibility?
- [ ] Are role boundaries clear and non-overlapping?
- [ ] Can agents work independently?

## Communication Design
- [ ] Is the handoff protocol standardized?
- [ ] Does it include all necessary context?
- [ ] Is it bidirectional (works both ways)?

## Enforcement Design
- [ ] Are there constraints preventing role compromise?
- [ ] Is there a verification loop?
- [ ] Are completion standards defined?

## Composability Design
- [ ] Can agents combine with other agents?
- [ ] Are interfaces clear and well-defined?
- [ ] Can the pattern apply to other domains?

## Error Handling Design
- [ ] What could go wrong at each step?
- [ ] How do we rollback changes?
- [ ] What are the recovery strategies?

## Validation Design
- [ ] Have we tested with real scenarios?
- [ ] Are examples from actual runs, not fictional?
- [ ] Have we identified design flaws through critical analysis?
```

---

## Common Mistakes

### Mistake 1: Natural Language Command Interfaces

**Problem**:
```bash
# Ambiguous, requires parsing
/architect-hub rename backend/app/services/extract.py to parser.py
```

**Solution**:
```bash
# Clear, programmatic
/architect-hub --op=rename --source=backend/app/services/extract.py --dest=parser.py
```

**Why**: Natural language is flexible but ambiguous. Structured parameters are clearer and work programmatically.

### Mistake 2: Personas Without Decision Frameworks

**Problem**:
```markdown
You are the Architect Hub, a specialized module refactoring assistant.

## Your Focus
- Renaming modules
- Moving files
- Updating imports
```

**Solution**:
```markdown
You are the Architect Hub. Decision rules:

## When to Use Git MV
- IF single file in same directory → Use git mv
- IF file has no dependents → Direct rename

## When to Create Migration Plan
- IF multi-file refactor → Create step-by-step plan
- IF circular imports detected → Break cycles first

## When to Stop
- IF import not found → Report error, don't proceed
- IF tests fail → Rollback changes, report failure
```

**Why**: Personas should guide decisions, not just describe roles.

### Mistake 3: Idealized Processes Without Error Handling

**Problem**:
```markdown
Process:
1. Analyze module
2. Request approval
3. Execute refactor
4. Verify changes
```

**Solution**:
```markdown
Process:
1. Analyze module
   - IF import not found → Report error and stop
2. Request approval
   - IF denied → Report cancellation
3. Execute refactor
   - IF git mv fails → Rollback and report
   - IF tests fail → Rollback and report
   - IF lint fails → Fix or report
4. Verify changes
   - IF verification fails → Retry or rollback
```

**Why**: Idealized processes fail in production. Always design for failure.

### Mistake 4: Fictional Examples

**Problem**:
```markdown
Example: Rename extract.py to parser.py

Output:
[Perfect, idealized output without any issues]
```

**Solution**:
```markdown
Example: Actual run from week4 refactoring

Input:
/architect-hub --op=rename --source=backend/app/services/extract.py --dest=parser.py

Output:
Analyzing module...
Found 3 import locations:
- backend/app/main.py: from app.services.extract import ...
- backend/tests/test_extract.py: from app.services.extract import ...
- backend/app/api/endpoints.py: import app.services.extract

Change plan:
1. Rename backend/app/services/extract.py → parser.py
2. Update 3 import statements
3. Run tests

Error encountered: Tests failed after rename
Rolling back changes...
[Real terminal output showing actual error and recovery]
```

**Why**: Fictional examples hide flaws. Real scenarios expose them.

### Mistake 5: Over-Engineering

**Problem**:
```yaml
Task: "Add a simple test file"
Solution: Deploy 5 agents (TestAgent, CodeAgent, ReviewAgent, ...)
Result: Coordination overhead exceeds task complexity
```

**Solution**:
```yaml
Task: "Add a simple test file"
Solution: Single agent or simple slash command
Result: Appropriate complexity for task
```

**Why**: Not every task needs multiple agents. Match complexity to task.

### Mistake 6: Tight Coupling

**Problem**:
```yaml
Agent A: Generates Python code
Agent B: Only works with Agent A's output (hardcoded format)
Agent C: Only works if Agent A and B run in specific order
```

**Solution**:
```yaml
Agent A: Generates code following standard format
Agent B: Works with any code following standard format
Agent C: Validates any implementation, independent of source
```

**Why**: Tight coupling prevents composability. Use standard interfaces.

---

## Advanced Topics

### Scaling to 3+ Agents

**Challenge**: Coordination overhead grows quadratically with agent count

**Solutions**:

1. **Hierarchical Organization**
   ```
   Orchestrator
     ├── Team A (2-3 agents)
     ├── Team B (2-3 agents)
     └── Team C (2-3 agents)
   ```
   - Each team has a sub-orchestrator
   - Reduces coordination complexity

2. **Shared State Management**
   ```yaml
   State Store:
     current_phase: "implementation"
     agents_completed: ["TestAgent"]
     agents_pending: ["CodeAgent", "ReviewAgent"]
     shared_context: {...}
   ```
   - Central source of truth
   - Prevents race conditions

3. **Event-Driven Coordination**
   ```yaml
   Events:
     - test_complete → Trigger CodeAgent
     - implementation_complete → Trigger ReviewAgent
     - review_approved → Complete
   ```
   - Loose coupling through events
   - Agents react to state changes

### Parallel Execution Strategies

**Strategy 1: Git Worktrees**
```bash
# Create isolated workspaces for each agent
git worktree add ../agent-A-worktree branch-A
git worktree add ../agent-B-worktree branch-B

# Agents work independently
# Merge after validation
```

**Strategy 2: Clear Ownership Boundaries**
```yaml
Agent A: backend/
  - Can edit: backend/**/*.py
  - Cannot edit: frontend/**

Agent B: frontend/
  - Can edit: frontend/**/*
  - Cannot edit: backend/**

Agent C: tests/
  - Can read: backend/, frontend/
  - Can edit: tests/**/*.py
```

**Strategy 3: Contract-Based Integration**
```yaml
Shared Contract: OpenAPI spec
  - Agent A: Implements backend to match spec
  - Agent B: Builds frontend to match spec
  - Agent C: Tests against spec

Integration:
  - All agents implement to contract
  - Integration is contract validation
```

### Verification Loops

**Single-Loop Verification**:
```yaml
Agent A → Agent B → Verify → Complete
```

**Double-Loop Verification** (like `/tdd-cycle`):
```yaml
TestAgent → CodeAgent → TestAgent (verify) → Complete
```

**Multi-Loop Verification**:
```yaml
TestAgent → CodeAgent → SecurityAgent → TestAgent → PerformanceAgent → Complete
```

**When to use multiple loops**:
- High-stakes deployments (security, finance)
- Complex requirements (multiple domains)
- Quality-critical systems (medical, aerospace)

---

## Further Reading

### Related Documentation

- [01_prompt_engineering.md](01_prompt_engineering.md) - 4-Layer Prompt Model in depth
- [06_automation_design.md](06_automation_design.md) - Designing composable automations
- [../claude-best-practices/02-understand/subagent-system.md](../claude-best-practices/02-understand/subagent-system.md) - Complete SubAgents reference

### Week 4 Resources

- [Week 4 Implementation](../weeks/week04/implementation.md) - How `/tdd-cycle` was built
- [Week 4 Reflection](../weeks/week04/reflection.md) - Critical analysis of design flaws
- [TDD First Principles](../claude-best-practices/02-understand/tdd-first-principles.md) - TDD philosophy

### External Resources

- [Claude Code SubAgents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents) - Official SubAgents guide
- [Multi-Agent Systems Research](https://en.wikipedia.org/wiki/Multi-agent_system) - Academic background
- [Orchestration Patterns](https://www.enterpriseintegrationpatterns.com/patterns/messaging/) - Enterprise patterns

### Practice Exercises

1. **Extend `/tdd-cycle`**:
   - Add parallel test support
   - Add code coverage requirements
   - Add performance benchmarks

2. **Create new SubAgents workflow**:
   - Identify a repetitive multi-step task
   - Design agent roles and handoff protocol
   - Implement and test with real scenarios

3. **Redesign `/architect-hub`**:
   - Fix the 4 design flaws identified
   - Add error handling branches
   - Test with real refactoring scenarios

4. **Build a 3-agent system**:
   - Orchestrator + 2 specialized agents
   - Clear roles and handoff protocol
   - Verification loop
   - Test with real work

---

## Summary

Multi-agent systems are powerful when designed well. The key is **coordination**, not just computation:

**Good multi-agent systems**:
- Clear role separation with enforcement
- Structured handoff protocols
- Verification loops for quality
- Composable design patterns
- Error handling and recovery

**Common mistakes**:
- Natural language interfaces (use structured parameters)
- Personas without decisions (add if-then rules)
- Idealized processes (design for failure)
- Fictional examples (test with reality)
- Over-engineering (match complexity to task)

**The Week 4 lesson**: Critical analysis is as important as design. Identifying flaws in `/architect-hub` was as valuable as building `/tdd-cycle`. Build systems, learn from mistakes, iterate.

> **Next**: [05_context_management.md](05_context_management.md) - Managing context in multi-agent systems

---

*[Last updated: 2026-01-02]*
