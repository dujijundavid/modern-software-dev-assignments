# Workflow Templates

Optimized workflows for common interaction patterns to prevent inefficiencies.

## Universal Decision Framework

Before starting ANY task, follow this mental checklist:

```
┌─────────────────────────────────────────────────────┐
│  1️⃣ CLARIFY GOAL (Enhanced)                         │
│     • What is the user's ultimate objective?        │
│     • What output format do they expect?            │
│     • Is this for analysis or action?               │
│     • Specific case OR general framework?           │
│     • One-time use OR reusable asset?               │
├─────────────────────────────────────────────────────┤
│  2️⃣ CONFIRM SCOPE                                  │
│     • Which product/system? (Code/Desktop/Cursor)   │
│     • Current project or system-wide?               │
│     • Single file or entire codebase?               │
├─────────────────────────────────────────────────────┤
│  3️⃣ PERMISSION PRE-CHECK                           │
│     • Review required permissions                   │
│     • Check allow list for gaps                     │
│     • Proactively ask for missing permissions       │
│     • Avoid mid-task interruptions                  │
├─────────────────────────────────────────────────────┤
│  4️⃣ SELECT TOOLS                                   │
│     • Specialized tools first (experts, skills)     │
│     • Batch independent operations                  │
│     • Prefer domain-specific over generic           │
├─────────────────────────────────────────────────────┤
│  5️⃣ EXECUTE STRATEGICALLY                          │
│     • Parallel when possible                        │
│     • Sequential only with dependencies             │
│     • Validate assumptions early                    │
├─────────────────────────────────────────────────────┤
│  6️⃣ DELIVER EXPECTED OUTPUT                        │
│     • Match requested format                        │
│     • Include context/sources                       │
│     • Summarize findings                            │
└─────────────────────────────────────────────────────┘
```

## Enhanced Goal Clarification Template

When task is ambiguous, use this proactive confirmation:

```markdown
## Task Confirmation

🎯 **Primary Goal**:
   - Are you looking for [specific solution] or [general framework]?
   - Is this [one-time analysis] or [reusable workflow]?

📦 **Expected Output**:
   - Documentation report?
   - Executable code/skill?
   - Both?

🔄 **Usage Context**:
   - Personal use or team sharing?
   - Single scenario or multiple use cases?

This ensures I deliver exactly what you need.
```

## Permission Pre-Check Template

Before executing tasks with multiple tool calls:

```markdown
## Permission Check

Required permissions for this task:
   ✅ Bash(python3) - Already allowed
   ✅ Bash(rm -f *.py) - Already allowed
   ⚠️  Bash(npx) - NOT in allow list

Options:
   a) Add `Bash(npx:*)` to permissions now
   b) Prompt when needed during execution
   c) Proceed without npx-dependent features

Which would you prefer?
```

## Template 1: System Status Check

When user asks "check my system", "analyze configuration", or similar:

### Workflow
```
1. Ask clarifying question:
   "What do you need - status overview or detailed document?"
   "Which product - Claude Code, Claude Desktop, or other?"

2. Run specialized commands first:
   claude mcp list
   claude --version

3. Read project config:
   .claude/settings.local.json

4. Generate structured output

5. Save to docs/ if document requested
```

### Anti-Patterns to Avoid
- ❌ Using `find` to search for config files
- ❌ Reading multiple unrelated configs
- ❌ Guessing which product user means

## Template 2: Code Investigation

When user asks to find, analyze, or understand code:

### Workflow
```
1. Clarify scope:
   • Single file or entire codebase?
   • What specific aspect (function, class, pattern)?

2. Choose search strategy:
   • Known symbol → Serena find_symbol
   • Pattern across files → Grep
   • Browse structure → Task with Explore agent

3. Read targeted content:
   • Get overview first (get_symbols_overview)
   • Read specific symbols as needed
   • Avoid reading entire files

4. Analyze and summarize
```

### Tool Selection Guide
```
Need → Tool
────────────────────────────────────────
Find specific class/function → find_symbol
Find all references → find_referencing_symbols
Find pattern → search_for_pattern
Understand file structure → get_symbols_overview
Explore unfamiliar codebase → Task(Explore agent)
```

## Template 3: Multi-File Changes

When user requests changes across multiple files:

### Workflow
```
1. Plan first (don't implement yet):
   • List all affected files
   • Identify dependencies
   • Check for breaking changes

2. Use EnterPlanMode for non-trivial changes
   • Get user approval on approach
   • Define clear implementation steps

3. Execute with parallelization:
   • Independent changes → parallel tool calls
   • Dependent changes → sequential

4. Validate:
   • Run tests
   • Check for references
   • Use code-reviewer before committing
```

### Parallel Execution Example
```yaml
# Independent file edits (parallel):
- Edit file1.py
- Edit file2.py
- Edit file3.py

# Dependent changes (sequential):
1. Edit base_class.py
2. Update child_class.py (depends on base)
3. Update tests.py (depends on both)
```

## Template 4: Debugging Task

When user reports a bug or error:

### Workflow
```
1. Gather information:
   • Exact error message
   • Steps to reproduce
   • Expected vs actual behavior

2. Isolate the problem:
   • Check recent changes (git diff)
   • Search for error context (Grep)
   • Check logs/console output

3. Form hypothesis:
   • What could cause this?
   • Verify with targeted checks

4. Implement fix:
   • Minimal change principle
   • Add test to prevent regression

5. Verify:
   • Test the fix
   • Check for similar issues
```

## Template 5: Documentation Generation

When user asks for docs, README, or analysis:

### Workflow
```
1. Understand target:
   • Audience? (technical, non-technical)
   • Format? (README, API docs, guide)
   • Scope? (feature, project, system)

2. Gather context:
   • Use /sc:index if project-wide
   • Read relevant source files
   • Check existing docs for consistency

3. Structure output:
   • Define outline first
   • Fill in sections
   • Add code examples if helpful

4. Review and refine:
   • Check clarity
   • Verify accuracy
   • Add diagrams if complex
```

## Template 6: Task Estimation

When user asks "how long will this take" or similar:

### Workflow
```
1. Break down task:
   • Identify subtasks
   • Note dependencies
   • Flag unknowns

2. Categorize complexity:
   • Routine → straightforward
   • Novel → requires exploration
   • Complex → multiple steps/dependencies

3. Provide structured estimate:
   • NOT time-based ("2-3 weeks") ✗
   • Step-based with complexity notes ✓

4. Highlight risks:
   • What could go wrong?
   • What requires more investigation?
```

## Template 7: Learning/Exploration

When user wants to understand a new topic or codebase:

### Workflow
```
1. Start with overview:
   • Use code-archaeologist for unfamiliar code
   • Get high-level structure first

2. Identify key concepts:
   • What are the main components?
   • How do they interact?

3. Deep dive selectively:
   • Read only relevant sections
   • Follow learning path (simple → complex)

4. Synthesize:
   • Create mental models
   • Document key insights
   • Note open questions
```

## Workflow Optimization Checklist

Before starting a task, ask:

- [ ] Goal is clear? (What does success look like?)
- [ ] Scope is defined? (What's in/out of bounds?)
- [ ] Tools are selected? (Specialized > generic)
- [ ] Order is optimal? (Dependencies respected)
- [ ] Output format confirmed? (Document, code, summary?)

## Common Anti-Patterns

| Anti-Pattern | Better Alternative |
|--------------|-------------------|
| Read entire file | Use symbol-level tools |
| Sequential independent calls | Parallel tool calls |
| Guess user intent | Ask clarifying question |
| Start coding immediately | Plan with EnterPlanMode |
| Use generic expert | Use domain-specific expert |
| Search with find/grep | Use specialized search tools |

## Agent Selection Guide

```
Task Type → Recommended Agent
─────────────────────────────────────────────
FastAPI work → @fastapi-expert
Python general → @python-expert
Testing → @python-testing-expert
Security review → @python-security-expert
Performance → @performance-optimizer
Code review → @code-reviewer (always before commits)
Unfamiliar code → @code-archaeologist
Documentation → @documentation-specialist
```

## Parallel Execution Rules

**Can parallelize if:**
- Operations are on different files
- No data dependency between operations
- Order doesn't matter for final result

**Must serialize if:**
- Second operation uses first operation's output
- Operations affect shared state
- Order is meaningful for correctness
