---
week: 4
title: "Week 4: Implementation"
type: implementation
status: completed
created: 2025-12-31
updated: 2026-01-02
related:
  - week:4:overview.md
  - week:4:reflection.md
tags: [week-4, implementation, slash-commands, subagents]
---

# Week 4: Implementation

> **Navigation**: [CS146S Docs](../../INDEX.md) > [Weeks](../) > [Week 4](./) > Implementation

## Approach

Week 4 focused on building two automations using Claude Code features: a slash command for module refactoring (`/architect-hub`) and a SubAgents system for Test-Driven Development (`/tdd-cycle`). Both automations were designed using the 4-Layer Prompt Model and SubAgents collaboration patterns.

**Key design principles**:
- **First principles thinking**: Understand why before how
- **Critical analysis**: Identify design flaws, not just apply templates
- **Real-world validation**: Test with actual scenarios, not fictional examples
- **Composability**: Design automations that work together

## Technical Decisions

### Decision 1: Slash Command vs. CLAUDE.md

- **Context**: Need to choose between slash commands and CLAUDE.md for automations
- **Options Considered**:
  - Option A: Only CLAUDE.md - Simple, but not reusable across conversations
  - Option B: Only slash commands - Discoverable, but requires planning
  - Option C: Hybrid approach - CLAUDE.md for context, slash commands for workflows
- **Choice**: Option C (Hybrid)
  - CLAUDE.md provides repository-specific guidance
  - Slash commands provide repeatable workflows
  - Best of both worlds
- **Trade-offs**:
  - Gained: Flexibility + reusability
  - Lost: Slight complexity in maintaining both
  - Risk: Potential inconsistency between CLAUDE.md and slash commands

### Decision 2: SubAgents for TDD

- **Context**: TDD discipline often breaks down in practice
- **Options Considered**:
  - Option A: Single agent with TDD instructions - Simple, but容易妥协
  - Option B: SubAgents with role separation - Enforced discipline
  - Option C: External TDD framework - Overkill for this use case
- **Choice**: Option B (SubAgents)
  - TestAgent only writes tests
  - CodeAgent only writes implementation
  - Orchestrator manages the workflow
- **Trade-offs**:
  - Gained: Enforced TDD discipline, verification loops
  - Lost: Increased complexity, more context management
  - Risk: Handoff protocol must be well-designed

### Decision 3: Handoff Protocol Design

- **Context**: SubAgents need structured communication
- **Options Considered**:
  - Option A: Natural language conversation - Flexible, but ambiguous
  - Option B: Structured handoff format - Clear, but rigid
  - Option C: Semi-structured with templates - Balanced approach
- **Choice**: Option C (Semi-structured templates)
  - Standardized sections (Feature, Tests, Requirements, Context)
  - Flexible content within sections
  - Clear protocol for both directions
- **Trade-offs**:
  - Gained: Clear communication, reduced ambiguity
  - Lost: Some flexibility in communication
  - Risk: Template must cover all necessary information

## Code Structure

### Directory Layout

```
week4/
├── .claude/
│   └── commands/
│       ├── architect-hub.md      # Slash command for module refactoring
│       └── tdd-cycle.md          # Slash command for TDD SubAgents
├── backend/
│   ├── app/
│   │   ├── routers/              # FastAPI routers
│   │   ├── services/             # Business logic
│   │   └── models.py             # SQLAlchemy models
│   └── tests/                    # pytest tests
├── frontend/                     # Static UI
├── data/
│   └── seed.sql                  # Database seed
├── docs/
│   └── TASKS.md                  # Agent-driven workflow tasks
├── pre-commit-config.yaml        # Pre-commit hooks
├── Makefile                      # Development commands
├── writeup.md                    # Comprehensive learning report (486 lines)
└── week4_writeup.md              # Empty template (71 lines) ⚠️ MARKED FOR DELETION
```

### Key Components

#### Automation 1: `/architect-hub`

**Purpose**: Module refactoring tool for structural changes (rename, move, import updates)

**File location**: [`.claude/commands/architect-hub.md`](../../.claude/commands/architect-hub.md)

**4-Layer Design**:

1. **Layer 1 (YAML)**:
```yaml
---
name: architect-hub
description: "Module refactoring tool for structural changes - renames, moves, import updates"
category: development
complexity: medium
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

2. **Layer 2 (Persona)**:
```markdown
You are the **Architect Hub**, a specialized module refactoring assistant.

## Your Focus
- Renaming modules
- Moving files between directories
- Updating all import statements

## What You Do NOT Handle
- Code cleanup (use `/refactor`)
- Dead code removal
```

3. **Layer 3 (Process)**:
- Analysis: Find all imports, assess impact, generate change plan
- Approval: Request user approval (safety mechanism)
- Execution: git mv + update imports
- Verification: Run tests + lint

4. **Layer 4 (Output)**:
- Analysis Output: Affected files, change plan, risk assessment
- Completion Output: Change summary, verification results, rollback commands

**Key functions/methods**:
- `analyze_module()`: Find all import locations
- `plan_refactor()`: Generate change plan
- `execute_refactor()`: Apply changes with git mv
- `verify_changes()`: Run tests and lint

**Dependencies**: Git, Grep, Edit tools

**Critical Design Flaws Identified**:
1. Command interface uses natural language instead of structured parameters
2. Persona lacks executable decision framework
3. Process is idealized without error handling branches
4. Examples are fictional, not validated with real scenarios

#### Automation 2: `/tdd-cycle`

**Purpose**: TDD workflow using SubAgents for enforced discipline

**File location**: [`.claude/commands/tdd-cycle.md`](../../.claude/commands/tdd-cycle.md)

**SubAgents Architecture**:

1. **TestAgent**:
```markdown
You are the **TestAgent**, specialized in writing comprehensive tests.

## Your Responsibility
- Write tests first, before any implementation
- Cover all scenarios (success, failure, edge cases)
- Never write implementation code
- Verify CodeAgent's work

## Your Outputs
- Test files with comprehensive coverage
- TestAgent → CodeAgent handoff
- Verification report
```

2. **CodeAgent**:
```markdown
You are the **CodeAgent**, specialized in writing minimal implementation.

## Your Responsibility
- Write simplest code to pass tests
- Never modify tests
- Follow existing patterns
- Report completion with test results

## Your Outputs
- Implementation code
- CodeAgent → TestAgent handoff
```

3. **Orchestrator**:
```markdown
You are the **Orchestrator**, managing the TDD workflow.

## Your Responsibility
- Parse user requirements
- Coordinate TestAgent and CodeAgent
- Manage handoffs between agents
- Ensure completion standards are met

## You Do NOT
- Write tests (TestAgent's job)
- Write implementation (CodeAgent's job)
```

**Handoff Protocol**:

**TestAgent → CodeAgent**:
```markdown
## TestAgent → CodeAgent Handoff

### Feature: [Feature Name]

### Tests Written
- `test_delete_note_success` - [Description]
- `test_delete_note_not_found` - [Description]

### Implementation Requirements
1. [Requirement 1]
2. [Requirement 2]

### Context
- Related models: [ModelName]
- Pattern to follow: [path/to/similar.py]
```

**CodeAgent → TestAgent**:
```markdown
## CodeAgent → TestAgent Handoff

### Files Modified
1. `path/to/file.py` - [Changes made]

### Test Results
[All tests passed]

### Ready for Verification
Please verify:
1. All tests pass ✅
2. Implementation matches requirements ✅
```

**Dependencies**: SubAgents system, handoff protocol

## Implementation Details

### Phase 1: Study Best Practices

**Goal**: Understand 4-Layer Model and SubAgents patterns

**Steps**:
1. Read [skill-design-best-practices.md](../../claude-best-practices/03-create/skill-design-best-practices.md)
2. Read [subagent-system.md](../../claude-best-practices/02-understand/subagent-system.md)
3. Read [tdd-first-principles.md](../../claude-best-practices/02-understand/tdd-first-principles.md)
4. Analyze existing slash commands in repository

**Outcome**: Deep understanding of design principles, not just templates

### Phase 2: Design `/architect-hub`

**Goal**: Create slash command for module refactoring

**Steps**:
1. Define problem: Manual refactoring is error-prone
2. Apply 4-Layer Model
3. Write command with examples
4. Perform critical analysis

**Code snippet**:
```bash
# Command interface (identified as flawed)
/architect-hub rename backend/app/services/extract.py to parser.py

# Improved design (proposed)
/architect-hub --op=rename --source=backend/app/services/extract.py --dest=parser.py
```

**Outcome**: Working slash command with identified design flaws

### Phase 3: Design `/tdd-cycle`

**Goal**: Create SubAgents system for TDD

**Steps**:
1. Define problem: TDD discipline breaks down
2. Design SubAgents (TestAgent, CodeAgent, Orchestrator)
3. Design handoff protocol
4. Test with real scenario (DELETE /notes/{id})

**Code snippet**:
```python
# TestAgent writes this first
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

**Outcome**: Working TDD SubAgents system

### Phase 4: Critical Analysis

**Goal**: Identify design flaws and propose improvements

**Steps**:
1. Review `/architect-hub` design
2. Identify 4 critical flaws
3. Propose concrete improvements
4. Document lessons learned

**Outcome**: Comprehensive critique with actionable improvements

## Challenges & Solutions

| Challenge | Solution | Lessons Learned |
|-----------|----------|-----------------|
| **Command interface confusion** | Identified need for structured parameters instead of natural language | Natural language is flexible but ambiguous; structured parameters are clearer |
| **Missing error handling** | Proposed error handling branches for all operations | Idealized processes fail in production; always design for failure |
| **Fictional examples** | Use real scenarios for validation | Examples must be tested, not imagined |
| **Persona lacks guidance** | Add decision framework with if-then rules | Persona should be actionable, not just descriptive |
| **Handoff protocol design** | Use semi-structured templates | Balance between structure and flexibility |

## Testing Strategy

### Unit Tests

**Coverage**: Not applicable (automations are slash commands, not code)

**Key test cases**:
- Test `/architect-hub` with real module refactoring
- Test `/tdd-cycle` with DELETE endpoint implementation
- Verify handoff protocol completeness

**Run tests**:
```bash
# From week4/ directory
make test
```

### Integration Tests

**Test scenarios**:
1. `/architect-hub` refactors a module and updates all imports
2. `/tdd-cycle` implements DELETE endpoint with full test coverage
3. SubAgents handoff protocol works bidirectionally

### Validation

**How to validate implementation**:
1. Run `/architect-hub` on a real module
2. Verify all imports are updated correctly
3. Run tests to ensure nothing broke
4. Use `/tdd-cycle` to implement a feature
5. Verify TestAgent and CodeAgent follow their roles
6. Check that all tests pass

## Performance Considerations

- **Bottlenecks identified**:
  - `/architect-hub`: Grep operations across large codebase can be slow
  - `/tdd-cycle`: Multiple agent handoffs increase latency
- **Optimizations applied**:
  - Use Grep with specific file patterns to reduce search space
  - Cache import analysis results
  - Parallelize independent operations
- **Benchmark results**: Not measured (automations are interactive)

## Security Considerations

- **Vulnerabilities addressed**:
  - `/architect-hub` uses `git mv` for safe file operations
  - Pre-commit hooks validate changes
  - Rollback commands provided for safety
- **Best practices followed**:
  - Approval step before destructive operations
  - Verification after changes
  - Never delete files without git tracking

## Automation & Tooling

**Automations created**:
1. **`/architect-hub`**: Module refactoring slash command (with identified flaws)
2. **`/tdd-cycle`**: TDD SubAgents system (working)

**Tools used**:
- **Claude Code**: Slash commands and SubAgents
- **Git**: Version control for safe refactoring
- **Grep**: Finding import statements
- **Edit**: Updating code
- **pytest**: Running tests
- **pre-commit**: Code quality gates

## Quick Links

- [Overview](./overview.md) - Concepts and objectives
- [Reflection](./reflection.md) - Learning outcomes and lessons
- [Weekly Deliverable](../../week4/writeup.md) - Original submission writeup

---
*[Template: weekly_implementation.md - Last updated: 2026-01-02]*
