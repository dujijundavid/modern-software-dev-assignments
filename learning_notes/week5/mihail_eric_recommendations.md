# Mihail Eric's Recommendations - Week 5

## 🎓 AI Engineering Mindset & Agentic Development

This document compiles all recommendations and insights from Prof. Mihail Eric for Week 5: Agentic Development with Warp.

---

## 🧠 Core Principles

### The Three Questions (Always Ask Before Acting)

```
🤔 1️⃣ What's the bottleneck?
   哪里是重复性、低价值的工作？

🤔 2️⃣ What's the leverage point?
   如何让这个自动化可复用、可组合？

🤔 3️⃣ How to compound value?
   这个自动化如何与其他自动化产生 1+1>3 的效果？
```

**Apply to every task**: Before writing any code, answer these three questions.

---

## 📈 The Automation Hierarchy

```
Level 1: One-off Script    → 解决一次问题
Level 2: Reusable Function → 解决一类问题
Level 3: Composable System → 可以与其他自动化组合
Level 4: Self-Improving    → 能够发现和优化自己的瓶颈
```

**Goal**: Always aim for Level 3+ (Composable Systems)

---

## 🎯 Before Writing Code, Ask

- ✅ **Is this task repeatable?** If yes, design for automation
- ✅ **Can this be parameterized?** Make it configurable, not hardcoded
- ✅ **What's the input/output contract?** Define clear interfaces
- ✅ **How will this fail?** Add error handling and rollback
- ✅ **Can this run concurrently?** Design for parallel execution

---

## 🔄 Week 5 Thinking Framework

```
┌─────────────────────────────────────────────────┐
│  Week 5 思考框架 (Thinking Framework)            │
└─────────────────────────────────────────────────┘

1️⃣ 观察 (Observe)
   - 当前工作流中有哪些重复性步骤？
   - 哪些任务需要上下文切换？
   - 哪些错误你犯了不止一次？

2️⃣ 定义 (Define)
   - 如果只能自动化一件事，是什么？
   - 这个自动化的输入/输出是什么？
   - 如何让它可复用？

3️⃣ 构建 (Build)
   - 设计 Warp saved prompt/rule
   - 测试它是否可复现
   - 记录边界情况

4️⃣ 组合 (Compose)
   - 哪些自动化可以链式调用？
   - 多代理如何并发而不冲突？
   - 失败时如何回滚？

5️⃣ 反思 (Reflect)
   - 这个自动化真的节省时间了吗？
   - 它的可维护性如何？
   - 下次如何改进？
```

---

## 👥 Multi-Agent Coordination Strategy

### Coordination Pattern

```yaml
Multi-Agent Workflow:
  - Define clear ownership (which agent owns what)
  - Use git branches/worktrees for isolation
  - Share contracts (schemas, interfaces) not implementation
  - Design failure recovery (what if Agent A fails?)
  - Maximize parallelism, minimize coordination overhead
```

### Anti-Patterns to Avoid

❌ **Don't**: Let agents edit the same files simultaneously
✅ **Do**: Use git worktrees or clear ownership boundaries

❌ **Don't**: Run agents without validation checkpoints
✅ **Do**: Have agent C (tests) validate before merging

❌ **Don't**: Mix concerns (e.g., agent edits both backend and frontend)
✅ **Do**: One concern per agent, clear interfaces

❌ **Don't**: Hard-code values (e.g., port 8000, localhost)
✅ **Do**: Parameterize everything (use env vars, config)

---

## 📊 Automation Evaluation Rubric

Score each automation before submitting:

```
📊 Automation Scorecard

Reusability (1-5):
  1 = One-off, hardcoded
  3 = Can be used for similar tasks with minor tweaks
  5 = Fully parameterized, works for any similar task

Composability (1-5):
  1 = Standalone, can't combine with others
  3 = Can be chained manually
  5 = Designed to compose, has clear input/output contracts

Autonomy (1-5):
  1 = Requires constant human intervention
  3 = Runs autonomously with supervision
  5 = Fully autonomous, handles edge cases and self-recovers

Robustness (1-5):
  1 = Fails silently or catastrophically
  3 = Fails gracefully with errors
  5 = Handles errors, rolls back, reports issues

Total Score: ___ / 20
Goal: 12+ for each automation
```

---

## 🎯 Recommended Automation Priority

### Tier 1 (Foundation - Do First)
- Environment Setup & Health Check ⭐
- Test Runner with Coverage
- Format + Lint Pipeline

### Tier 2 (High Leverage)
- API Response Standardization (Task 7)
- Pagination Pattern (Task 8)
- Error Handling Wrapper

### Tier 3 (Feature-Level)
- Notes Search (Task 2)
- Bulk Operations (Task 4)
- Extraction Logic (Task 6)

### Tier 4 (Complex/Advanced)
- Frontend Migration to React (Task 1)
- Tags Feature (Task 5)
- Vercel Deployment (Task 11)

---

## 💡 Pro Tips from Prof. Eric

### 1. Start Small, Then Scale
- First automation: something you'll use daily
- Second automation: something that helps others
- Third automation: something that combines 1 + 2

### 2. Document as You Build
- Don't "document later" — you won't
- Write the docs before writing the automation
- Update docs when you find edge cases

### 3. Test Your Automations
- Run them 5 times in a row
- If they fail once, they're not reliable enough
- Add error handling until they pass 5/5 times

### 4. Share and Iterate
- Show your automations to classmates
- Ask: "Would you use this? Why or why not?"
- Improve based on feedback

### 5. Think in Workflows, Not Tasks
- A task is "add pagination to notes endpoint"
- A workflow is "from idea to deployed feature with tests"
- Automate workflows, not just tasks

---

## 🛠️ Example Warp Saved Prompts

### Prompt 1: "Add Pagination to Endpoint"

```
Context: FastAPI backend with SQLAlchemy
Task: Add pagination support to {endpoint}
Input: Endpoint path, model name
Output: Updated endpoint with page/page_size params, returns {items, total}

Pattern:
  1. Add page/page_size query params (default: page=1, page_size=10)
  2. Apply .offset() and .limit() to query
  3. Run COUNT(*) query for total
  4. Return {"items": [...], "total": N, "page": 1, "page_size": 10}
  5. Add tests for edge cases (empty, last page, negative page)
```

### Prompt 2: "Standardize API Response"

```
Context: FastAPI endpoints need consistent error handling
Task: Wrap {endpoint} with standard response envelope

Pattern:
  Success: {"ok": true, "data": {...}}
  Error: {"ok": false, "error": {"code": "NOT_FOUND", "message": "..."}}

Steps:
  1. Create response schemas in schemas.py
  2. Wrap return values in response envelope
  3. Add exception handlers for common errors
  4. Update tests to assert envelope shape
```

### Prompt 3: "Multi-Agent Task Runner"

```
Context: Week 5 multi-agent workflow
Task: Coordinate 3 agents working on different tasks

Agents:
  - Agent A: Backend API (works in backend/)
  - Agent B: Frontend UI (works in frontend/)
  - Agent C: Tests (works in backend/tests/)

Coordination:
  1. Create git worktree for each agent
  2. Define shared contract (e.g., OpenAPI spec)
  3. Run agents in parallel
  4. Agent C validates A and B's work
  5. If C fails, rollback A and B
  6. If all pass, merge worktrees
```

---

## 📝 Writeup Template

For each automation, use this structure:

```markdown
## Automation [N]: [Name]

### Goal
What problem does this solve?

### Design
- Input: ...
- Output: ...
- Steps: ...

### Warp Implementation
- Saved prompt / rule / MCP server: (paste or link)
- How to use: ...

### Before vs After
- Before: [describe manual workflow]
- After: [describe automated workflow]
- Time saved: ...

### Autonomy Level
- Code permissions: (read/write/execute)
- Supervision: (full / partial / none)
- Why: ...

### Multi-Agent Notes (if applicable)
- Agent roles: ...
- Coordination: ...
- Concurrency wins: ...
- Failures encountered: ...

### How I Used It
[Pain point it resolved or accelerated]
```

---

## 🎓 Final Thought

> "The best AI engineers aren't the ones who write the most code. They're the ones who build systems that write, test, and deploy code automatically while they sleep."
>
> — Mihail Eric (paraphrased)

**Your goal in Week 5**: Build one such system.

---

## 📚 Additional Resources

- [Warp Agentic Development Environment](https://www.warp.dev/)
- [Warp University](https://www.warp.dev/university?slug=university)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CS146S Course](https://themodernsoftware.dev)

---

**Compiled**: 2025-01-02
**Week**: 5 - Agentic Development with Warp
**Instructor**: Mihail Eric
**Course**: CS146S - The Modern Software Developer
