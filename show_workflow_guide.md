# /sc:show-workflow Quick Reference

## What Does It Do?

Demonstrates complex workflows with full transparency:
- Phase-by-phase execution (Analysis → Discovery → Decisions → Execution → Verification)
- Tool-by-tool transparency (shows every tool call and result)
- Decision rationale (explains WHY, not just HOW)
- Optional teaching mode (quizzes and knowledge checks)

## Basic Usage

```bash
# Standard workflow demonstration
/sc:show-workflow commit and push changes

# With teaching mode (adds quizzes)
/sc:show-workflow --teach add authentication

# Complex multi-step tasks
/sc:show-workflow refactor the notes service
/sc:show-workflow add pagination to all endpoints
/sc:show-workflow test and debug the /notes endpoint
```

## What You'll See

### Phase 1: Task Analysis
```
🎯 Task Analysis
├─ Sub-tasks identified
├─ Execution strategy
└─ Complexity assessment
```

### Phase 2: State Discovery (Parallel)
```
🔍 State Discovery
├─ Running: git status, git diff, git log (in parallel)
├─ Results summarized
└─ Key findings highlighted
```

### Phase 3: Analysis & Decisions
```
🤔 Decision Making
├─ Options considered (A, B, C)
├─ My choice + rationale
└─ Trade-offs accepted
```

### Phase 4: Execution
```
⚙️ Execution
├─ Step 1: Tool call → Result
├─ Step 2: Tool call → Result
└─ Step 3: Tool call → Result
```

### Phase 5: Verification
```
✅ Verification
├─ Final state check
├─ Workflow summary
└─ Success metrics
```

## Teaching Mode (--teach flag)

Adds interactive learning checkpoints:

```bash
/sc:show-workflow --teach commit and push changes
```

**Extra features:**
- 📝 Quiz questions after each phase
- 🤔 "What if?" scenario discussions
- ⏸️ Checkpoints (pause and confirm before continuing)
- 🎓 Learning summary at the end
- 📊 Progress saved to `learning_progress/`

## Example Output

```
🎯 Task Analysis

**User Request:** "commit and push changes"

**Sub-tasks:**
1. Check git status
2. Stage files
3. Generate commit message
4. Create commit
5. Handle divergence
6. Push to remote

**Starting workflow...**

🔍 Phase 2: State Discovery

Running discovery in parallel...

[git status]
[git diff --staged]
[git log -5]

📊 Discovery Results:
- 3 files changed (all unstaged)
- Branch behind origin/master
- Commit style: Conventional Commits

🤔 Phase 3: Decision Making

**Decision: What to commit?**
- Option A: All changes → Risk: unrelated files
- Option B: Ask user → ✅ Chosen (safer)
- Option C: Abort → Breaks workflow

**Rationale:** No staged changes, need user intent

⚙️ Phase 4: Execution

### Step 1: Ask User
<AskUserQuestion> → User chose "Stage all"

### Step 2: Stage Files
<git add ...> → ✅ Success

### Step 3: Create Commit
<git commit -m "..."> → ✅ Success (c53329b)

✅ Phase 5: Verification

<git status> → "ahead by 1 commit"

**Workflow Summary:**
- Files: 3 changed, 477 insertions
- Tools: Bash (8x), AskUserQuestion (1x)
- Time: ~45 seconds
- Key decisions: Rebase over merge, heredoc format
```

## When to Use

| Use Case | Command | Why |
|----------|---------|-----|
| Learn git workflow | `/sc:show-workflow --teach commit` | Understand full flow |
| Debug CI/CD | `/sc:show-workflow test and deploy` | See where it fails |
| Understand refactor | `/sc:show-workflow refactor X` | See decision process |
| Learn new pattern | `/sc:show-workflow --teach add Y` | Interactive learning |
| Document workflow | `/sc:show-workflow complex task` | Generate documentation |

## vs Other Commands

| Command | Best For | Transparency |
|---------|----------|--------------|
| `/sc:git commit` | Just get it done | Low (standard output) |
| `/sc:show-workflow commit` | See how it works | **High (phase-by-phase)** |
| `/sc:show-workflow --teach commit` | Learn the workflow | **Very High (+quizzes)** |

## Pro Tips

1. **First time?** Use `--teach` flag for interactive learning
2. **Debugging?** Run without `--teach` for faster execution
3. **Complex task?** Break it down: `/sc:show-workflow step 1`, then `step 2`
4. **Want to understand?** Pay attention to "Decision Making" phase—shows the WHY
5. **Teaching others?** Use `--teach` mode, it's designed for pedagogy

## What You'll Learn

By using `/sc:show-workflow`, you'll understand:

- **Tool coordination** → How multiple tools work together
- **Parallel execution** → When to run operations concurrently
- **Decision making** → How Claude chooses between options
- **Error recovery** → What happens when tools fail
- **Git workflows** → State discovery, commit, push, rebase
- **FastAPI patterns** → Router → Service → Database layer
- **Testing strategies** → TestClient, fixtures, coverage
- **Refactoring approach** → Analysis → Plan → Execute → Verify

## Customization

Want to adapt it for your workflows?

1. Read `.claude/commands/show-workflow.md`
2. Find the "Phase Structure" section
3. Add your own phases or modify existing ones
4. Test with `/sc:show-workflow [your task]`

## Example Workflows to Try

```bash
# Git operations
/sc:show-workflow commit and push changes
/sc:show-workflow create a pull request
/sc:show-workflow resolve merge conflicts

# FastAPI development
/sc:show-workflow add a new endpoint
/sc:show-workflow add error handling
/sc:show-workflow add pagination

# Testing
/sc:show-workflow write tests for endpoint
/sc:show-workflow increase test coverage
/sc:show-workflow debug failing tests

# Refactoring
/sc:show-workflow extract service layer
/sc:show-workflow improve error handling
/sc:show-workflow optimize database queries

# DevOps
/sc:show-workflow set up CI/CD pipeline
/sc:show-workflow deploy to production
/sc:show-workflow roll back deployment
```

## Feedback

After using `/sc:show-workflow`:

1. ✅ What was helpful?
2. ❌ What was confusing?
3. 💡 What would make it better?

Your feedback improves the command for everyone!
