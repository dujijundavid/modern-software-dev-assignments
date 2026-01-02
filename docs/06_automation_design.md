# Automation Design: From Scripts to Systems

> **Navigation**: [CS146S Docs](./INDEX.md) > Automation Design

> **Status**: Core Concept - Automation design principles and patterns from CS146S

---

## Quick Reference

### The AI Engineering Mindset

```
Core Principle: Build Systems, Not Just Code

The Three Questions:
1. What's the bottleneck?      Where is the repetitive, low-value work?
2. What's the leverage point?  How can this be reusable and composable?
3. How to compound value?      How does this create 1+1>3 effects?
```

### The Automation Hierarchy

```
Level 4: Self-Improving
    - Automations that discover and optimize their own bottlenecks
    - Meta-automation for improving automations
    - Learning from mistakes and adapting

Level 3: Composable System
    - Clear input/output contracts
    - Can be combined and chained with other automations
    - Designed for integration from the start

Level 2: Reusable Function
    - Parameterized for similar tasks
    - Can be used multiple times with different inputs
    - Generalized from one-off scripts

Level 1: One-off Script
    - Solves a specific problem once
    - Hardcoded values and context
    - Not designed for reuse
```

**Goal**: Always aim for Level 3+, with clear path to Level 4.

### Design Checklist

Before building any automation:

- [ ] Answered The Three Questions
- [ ] Identified the bottleneck
- [ ] Defined input/output contract
- [ ] Planned for failure modes
- [ ] Parameterized (not hardcoded)
- [ ] Clear error handling
- [ ] Idempotent operations
- [ ] Tested with real scenarios

---

## The Automation Hierarchy

### Level 1: One-off Scripts

**Definition**: Solves a specific problem once. Hardcoded values and context.

**Characteristics**:
- Fast to write
- Solves immediate problem
- Not reusable
- Brittle - breaks when context changes

**Example**: Bash script to rename a specific file
```bash
# One-time use - hardcoded paths
mv backend/app/services/extract.py backend/app/services/parser.py
sed -i '' 's/from extract/from parser/g' backend/app/routers/*.py
```

**When to use**: Quick prototyping, exploratory work

**Path to Level 2**: Parameterize inputs, generalize patterns

---

### Level 2: Reusable Functions

**Definition**: Parameterized automations for similar tasks. Can be used multiple times with different inputs.

**Characteristics**:
- Accepts parameters/arguments
- Works for similar tasks
- Some error handling
- Documented usage

**Example**: Environment health check script
```bash
#!/bin/bash
# Parameterized - works for any project
check_environment() {
    local project_dir=$1
    local min_python_version=$2

    # Check Python version
    python_version=$(python3 --version | cut -d' ' -f2)
    # ... checks for poetry.lock, tests, database, etc.
}

# Usage:
check_environment . "3.10"
```

**When to use**: Repeatable tasks across similar contexts

**Path to Level 3**: Define clear input/output contracts, design for composition

---

### Level 3: Composable Systems

**Definition**: Automations with clear input/output contracts that can be combined and chained.

**Characteristics**:
- Well-defined interfaces
- Standardized output formats
- Can be chained together
- Designed for integration
- Error recovery mechanisms

**Example**: TDD Cycle SubAgents System
```markdown
## TestAgent → CodeAgent Handoff Protocol

### Input (from user)
- Feature requirement

### Output (from TestAgent)
- Test files with comprehensive coverage
- Structured handoff with test requirements

### Output (from CodeAgent)
- Implementation code
- Test results verification

### Composition
- TestAgent output → CodeAgent input
- CodeAgent output → TestAgent verification
- Orchestrator manages the workflow
```

**When to use**: Building workflows, multi-agent systems, CI/CD pipelines

**Path to Level 4**: Add self-monitoring, error recovery, learning mechanisms

---

### Level 4: Self-Improving

**Definition**: Automations that discover and optimize their own bottlenecks. Meta-automation.

**Characteristics**:
- Monitors own performance
- Identifies inefficiencies
- Suggests or applies optimizations
- Learns from failures
- Adapts to changing conditions

**Example**: Self-optimizing test runner
```python
class SmartTestRunner:
    def __init__(self):
        self.execution_times = {}
        self.failure_patterns = {}

    def run_tests(self):
        # 1. Identify slow tests
        # 2. Suggest parallelization
        # 3. Learn from failures
        # 4. Optimize test order based on dependencies

    def optimize(self):
        # Auto-apply optimizations based on history
        pass
```

**When to use**: Critical workflows, production systems, long-running processes

**Note**: Level 4 is the frontier - most automations should target Level 3

---

## Design Principles

### Principle 1: The Three Questions

Before building any automation, ask:

**1. What's the bottleneck?**
- What repetitive, low-value work are you doing?
- What causes context switching?
- What errors do you make repeatedly?

**2. What's the leverage point?**
- How can this be automated to be reusable?
- How can it be parameterized, not hardcoded?
- What's the minimum viable automation?

**3. How to compound value?**
- How does this combine with other automations?
- What's the input/output contract?
- How can this be used by others?

**Example**: TDD Cycle automation
- Bottleneck: TDD discipline breaks down, testing/implementation require different mindsets
- Leverage: SubAgents enforce role separation
- Compound: Composes with other automations (refactor, documentation, deployment)

---

### Principle 2: Design for Failure

Assume your automation will fail. Design for it.

**Error Handling Requirements**:
- Clear error messages
- Rollback mechanisms
- Idempotent operations (can run multiple times safely)
- Logging and audit trails
- Graceful degradation

**Example**: Module refactoring with rollback
```python
def refactor_module(source, dest):
    try:
        # 1. Analyze impact
        affected_files = analyze_imports(source)

        # 2. Create backup branch
        git_branch = f"refactor-{int(time.time())}"
        run_git(f"checkout -b {git_branch}")

        # 3. Apply changes
        move_file(source, dest)
        update_imports(affected_files, source, dest)

        # 4. Verify
        if not run_tests():
            raise RefactoringError("Tests failed")

        # 5. Only merge if successful
        run_git(f"checkout master")
        run_git(f"merge {git_branch}")

    except Exception as e:
        # Rollback
        run_git(f"checkout master")
        run_git(f"branch -D {git_branch}")
        logger.error(f"Refactoring failed: {e}")
        raise
```

---

### Principle 3: Start Small, Scale Up

Evolution path from Level 1 to Level 3+:

**Phase 1: Build a one-off script (Level 1)**
- Solve immediate problem
- Don't worry about generalization
- Validate the approach

**Phase 2: Generalize to reusable function (Level 2)**
- Parameterize inputs
- Add configuration options
- Document usage

**Phase 3: Design for composition (Level 3)**
- Define input/output contracts
- Standardize output formats
- Design for chaining

**Phase 4: Add self-improvement (Level 4)**
- Monitor performance
- Learn from failures
- Optimize automatically

**Example Evolution**: Environment Health Check
1. Level 1: Manual commands typed each time
2. Level 2: Bash script that checks environment
3. Level 3: Composable checks that can be chained with test runners
4. Level 4: Self-healing environment that fixes common issues

---

### Principle 4: Clear Contracts

Define input/output contracts explicitly.

**Input Contract**:
- What parameters are required?
- What's the format/type of each parameter?
- What are the valid values/ranges?
- What are the defaults?

**Output Contract**:
- What format is the output?
- What fields are always present?
- What fields are optional?
- How are errors represented?

**Example**: Pagination function
```python
def paginate(query, page=1, page_size=10):
    """
    Input Contract:
        query: SQLAlchemy Query object (required)
        page: int >= 1 (default: 1)
        page_size: int between 1 and 100 (default: 10)

    Output Contract:
        {
            "items": List[Model],      # Always present
            "total": int,               # Always present
            "page": int,                # Always present
            "page_size": int,           # Always present
            "has_next": bool,           # Always present
            "has_prev": bool            # Always present
        }

    Errors:
        ValueError: If page < 1 or page_size not in [1, 100]
    """
    # Implementation...
```

---

## Real-World Examples

### Example 1: TDD Cycle Automation

**From**: Week 4 implementation

**Problem**: TDD discipline breaks down in practice because developers lack discipline to maintain test-first workflow.

**Solution**: SubAgents system that enforces TDD discipline

#### Design

**SubAgents Architecture**:
1. **TestAgent**: Only writes tests, never implementation
2. **CodeAgent**: Only writes implementation, never tests
3. **Orchestrator**: Manages workflow, coordinates agents

**Handoff Protocol**:
```markdown
## TestAgent → CodeAgent Handoff

### Feature: DELETE /notes/{id}

### Tests Written
- `test_delete_note_success` - Verifies deletion and database removal
- `test_delete_note_not_found` - Verifies 404 response

### Implementation Requirements
1. Return 204 on success
2. Return 404 if note not found
3. Remove note from database

### Context
- Related models: Note
- Pattern to follow: backend/app/routers/notes.py
```

#### Implementation

**TestAgent Output**:
```python
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

**CodeAgent Output**:
```python
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.flush()
    return Response(status_code=204)
```

#### Analysis

**Automation Level**: Level 3 (Composable System)
- Clear role separation (TestAgent vs CodeAgent)
- Structured handoff protocol
- Verification loop (TestAgent validates CodeAgent)
- Can compose with other automations

**Strengths**:
- Enforced discipline (agents can't compromise their roles)
- Natural verification loop
- Clear responsibilities

**Weaknesses**:
- Multiple agent handoffs increase latency
- Requires well-designed handoff protocol
- More complex than single agent

**Path to Level 4**:
- Add performance monitoring
- Learn from common test patterns
- Auto-suggest test cases based on code

---

### Example 2: Architect Hub (with Design Flaws)

**From**: Week 4 implementation

**Problem**: Module refactoring requires manual import updates, which is error-prone and repetitive.

**Solution**: Slash command for automated module refactoring

#### Design (Original - with flaws)

**4-Layer Prompt Model**:

1. **Layer 1 (YAML)**:
```yaml
---
name: architect-hub
description: "Module refactoring tool for structural changes"
category: development
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

2. **Layer 2 (Persona)**:
```markdown
You are the Architect Hub, a specialized module refactoring assistant.

## Your Focus
- Renaming modules
- Moving files between directories
- Updating all import statements

## What You Do NOT Handle
- Code cleanup (use /refactor)
- Dead code removal
```

3. **Layer 3 (Process)**:
- Analysis: Find all imports, assess impact, generate change plan
- Approval: Request user approval
- Execution: git mv + update imports
- Verification: Run tests + lint

4. **Layer 4 (Output)**:
- Analysis Output: Affected files, change plan, risk assessment
- Completion Output: Change summary, verification results

#### Critical Design Flaws Identified

**Flaw 1: Command Interface Uses Natural Language**
```bash
# Current (flawed):
/architect-hub rename backend/app/services/extract.py to parser.py

# Improved:
/architect-hub --op=rename --source=backend/app/services/extract.py --dest=parser.py
```

**Problem**: Natural language requires parsing and is ambiguous.

**Impact**: Command is less reliable, harder to use programmatically.

---

**Flaw 2: Persona Lacks Executable Decision Framework**

```markdown
# Current (flawed):
You are the Architect Hub. Your focus is renaming modules.

# Improved:
You are the Architect Hub.

## Decision Framework
IF refactoring involves moving files across package boundaries:
    - Check for circular dependencies
    - Update __init__.py exports
    - Verify no broken imports

IF refactoring involves renaming:
    - Use git mv to preserve history
    - Update all import statements
    - Run tests to verify

IF tests fail:
    - Rollback changes
    - Report specific failure
    - Suggest manual intervention
```

**Problem**: Persona describes role but doesn't guide decisions.

**Impact**: Agent lacks clear decision-making criteria.

---

**Flaw 3: Process is Idealized Without Error Handling**

```markdown
# Current (flawed):
1. Analyze impact
2. Request approval
3. Execute changes
4. Verify

# Improved:
1. Analyze impact
   - IF analysis fails: Report error, suggest manual review
2. Request approval
   - IF denied: Exit gracefully, no changes made
3. Execute changes
   - IF git mv fails: Rollback, report error
   - IF import update fails: Rollback, report specific file
   - IF tests fail: Rollback, provide test output
4. Verify
   - IF lint errors: Show errors, ask if continue
   - IF all pass: Report success, provide rollback command
```

**Problem**: Assumes happy path, no error handling branches.

**Impact**: Command would fail catastrophically in real use.

---

**Flaw 4: Fictional Examples**

```markdown
# Current (flawed):
Example: /architect-hub rename backend/app/services/extract.py to parser.py
This will rename the file and update all imports.

# Improved:
Real Scenario: Renamed extract.py to parser.py in week4/
Files affected:
  - backend/app/routers/notes.py (1 import updated)
  - backend/app/services/__init__.py (1 export updated)
Test results: 6/6 passed
Lint results: No errors
Time taken: 2.3 seconds
```

**Problem**: Examples are fictional, not validated with real scenarios.

**Impact**: Hidden flaws not discovered until real use.

#### Analysis

**Automation Level**: Level 2 (Reusable Function)
- Addresses repetitive problem
- Can be used for multiple refactorings
- But lacks composable design

**Why not Level 3**:
- No clear input/output contract
- Natural language interface prevents programmatic use
- Not designed to compose with other automations

**Path to Level 3**:
1. Fix command interface (structured parameters)
2. Add decision framework to persona
3. Design error handling branches
4. Validate with real scenarios
5. Define clear output format for composition

---

## Evaluation Rubric

Score each automation on these dimensions (1-5 each):

### Reusability

**Score 1**: One-off, hardcoded
- Works for one specific case
- Hardcoded values
- Not portable

**Score 3**: Can be used for similar tasks with minor tweaks
- Some parameterization
- Works for related tasks
- Minor modifications needed

**Score 5**: Fully parameterized, works for any similar task
- Completely parameterized
- Works for any task in domain
- No modifications needed

**Example**:
- Score 1: Script that renames a specific file
- Score 3: Script that renames files in a specific directory
- Score 5: Generic refactoring tool with configurable operations

---

### Composability

**Score 1**: Standalone, can't combine with others
- No defined interfaces
- Inconsistent output
- Can't chain

**Score 3**: Can be chained manually
- Some interface definition
- Requires manual adaptation
- Possible to chain with effort

**Score 5**: Designed to compose, has clear input/output contracts
- Well-defined interfaces
- Standardized output
- Designed for chaining

**Example**:
- Score 1: Script that prints results to stdout
- Score 3: Script that outputs JSON (requires parsing)
- Score 5: Function with structured return type

---

### Autonomy

**Score 1**: Requires constant human intervention
- Every step requires approval
- Can't recover from errors
- No decision-making

**Score 3**: Runs autonomously with supervision
- Handles common cases
- Requires approval for critical operations
- Can recover from expected errors

**Score 5**: Fully autonomous, handles edge cases and self-recovers
- Handles all expected cases
- Self-healing
- Learns from failures

**Example**:
- Score 1: Script that asks before every operation
- Score 3: Script that asks before destructive operations only
- Score 5: Script that runs full workflow with rollback on failure

---

### Robustness

**Score 1**: Fails silently or catastrophically
- No error handling
- Silent failures
- Data corruption possible

**Score 3**: Fails gracefully with errors
- Clear error messages
- No silent failures
- Some rollback capability

**Score 5**: Handles errors, rolls back, reports issues
- Comprehensive error handling
- Full rollback capability
- Detailed error reporting
- Logging and audit trails

**Example**:
- Score 1: Script that crashes and leaves system in unknown state
- Score 3: Script that catches errors and reports them
- Score 5: Script that rolls back all changes on error and provides detailed log

---

### Total Score and Target

**Total Score**: ___ / 20

**Target**: 12+ for each automation

**Interpretation**:
- 16-20: Excellent automation (Level 3-4)
- 12-15: Good automation (Level 2-3)
- 8-11: Needs improvement (Level 1-2)
- <8: Not automation-ready (Level 1)

---

## Automation Design Checklist

### Planning Phase

- [ ] Answered The Three Questions
- [ ] Identified the bottleneck
- [ ] Identified the leverage point
- [ ] Identified compounding opportunities
- [ ] Defined scope (what's in/out)

### Design Phase

- [ ] Defined input contract (parameters, types, validation)
- [ ] Defined output contract (format, fields, errors)
- [ ] Identified failure modes
- [ ] Designed error handling
- [ ] Designed rollback mechanisms
- [ ] Parameterized all configurable values

### Implementation Phase

- [ ] Followed existing patterns
- [ ] Documented with examples
- [ ] Added logging
- [ ] Made operations idempotent
- [ ] Version controlled

### Validation Phase

- [ ] Tested with real scenarios (not fictional)
- [ ] Runs successfully 5 times in a row
- [ ] Handles errors gracefully
- [ ] Tested rollback mechanisms
- [ ] Clear error messages
- [ ] Achieved target score (12+/20)

---

## Common Anti-Patterns

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

**How to avoid**: Parameterize everything that might vary

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

### Anti-Pattern 4: Happy Path Only

**Problem**: Only works when everything goes perfectly

**Example**:
```python
# Bad: Assumes operations succeed
def refactor(source, dest):
    move_file(source, dest)
    update_imports(source, dest)

# Good: Handles failures
def refactor(source, dest):
    try:
        move_file(source, dest)
        update_imports(source, dest)
        verify_changes()
    except MoveError as e:
        rollback_move()
        raise RefactoringError(f"Move failed: {e}")
    except UpdateError as e:
        rollback_move()
        rollback_imports()
        raise RefactoringError(f"Import update failed: {e}")
```

**How to avoid**: Assume every operation can fail

---

## Quick Reference Tables

### Automation Levels Quick Check

| Level | Name | Key Characteristic | Example | Time to Build |
|-------|------|-------------------|---------|---------------|
| 1 | One-off Script | Solves specific problem | Bash script for one-time task | Minutes |
| 2 | Reusable Function | Parameterized | Function with arguments | Hours |
| 3 | Composable System | Clear I/O contract | Can chain with other automations | Days |
| 4 | Self-Improving | Discovers own bottlenecks | Optimizes itself over time | Weeks |

### Tool Choices by Use Case

| Use Case | Recommended Tool | Why |
|----------|------------------|-----|
| File operations | Bash scripts | Simple, ubiquitous |
| API automation | Python + requests | Easy HTTP, good error handling |
| Code generation | Jinja2 templates | Parameterized, composable |
| Workflows | Make/Just | Dependency management |
| CI/CD | GitHub Actions | Integrated with git |
| Interactive prompts | Warp/Claude Code | AI-assisted workflows |

### Common Bottlenecks and Solutions

| Bottleneck | Leverage Point | Automation Level |
|------------|----------------|------------------|
| Environment setup issues | Health check script | Level 2 |
| Forgetting to run tests | Pre-commit hook | Level 2 |
| Inconsistent code quality | Format + lint pipeline | Level 2 |
| Repetitive API tasks | Code generation templates | Level 3 |
| Manual testing | TDD SubAgents | Level 3 |
| Deployment friction | CI/CD pipeline | Level 3 |
| Performance issues | Monitoring + auto-scaling | Level 4 |

---

## Further Reading

### Course Documentation

- [04_multi_agent_systems.md](./04_multi_agent_systems.md) - Multi-agent coordination patterns
- [05_learning_journey.md](./05_learning_journey.md) - Learning progression through the course
- [Week 4 Overview](./weeks/week04/overview.md) - Slash commands and SubAgents
- [Week 4 Implementation](./weeks/week04/implementation.md) - Real-world automation examples
- [Week 4 Reflection](./weeks/week04/reflection.md) - Lessons learned and critical analysis

### Patterns

- [Automation Design Patterns](./patterns/automation_design.md) - Detailed patterns and anti-patterns
- [Prompting Patterns](./patterns/prompting.md) - 4-Layer Prompt Model

### External Resources

- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official Anthropic documentation
- [SubAgents Overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents) - SubAgents collaboration patterns

---

## Summary

Effective automation design is about building systems, not just writing code. The automation hierarchy provides a framework for evolving from quick scripts to robust, composable systems.

**Key takeaways**:
1. **Start with The Three Questions**: Identify bottlenecks, leverage points, and compounding opportunities
2. **Design for failure**: Assume your automation will fail, and plan for it
3. **Aim for Level 3**: Composable systems with clear contracts
4. **Validate with reality**: Test with real scenarios, not fictional examples
5. **Iterate continuously**: Level 1 → Level 2 → Level 3 → Level 4

**Remember**: "The best AI engineers aren't the ones who write the most code. They're the ones who build systems that write, test, and deploy code automatically while they sleep."

---

*[Created 2026-01-02 - Automation design principles and patterns from CS146S]*
