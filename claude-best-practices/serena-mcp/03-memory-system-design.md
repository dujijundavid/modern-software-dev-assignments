# Serena 内存系统设计

> 持久化项目知识、决策和学习的完整指南

---

## 目录

1. [内存文件类型和用途](#内存文件类型和用途)
2. [标准化模板设计](#标准化模板设计)
3. [记忆组织原则](#记忆组织原则)
4. [写作规范和示例](#写作规范和示例)
5. [与 CLAUDE.md 的配合](#与-claude-md-的配合)
6. [动态更新策略](#动态更新策略)

---

## 内存文件类型和用途

### 1.1 完整内存类型分类

```
.serena/memories/
│
├── ============ 项目级内存 ============
├── project_context_and_goals.md      # 项目愿景、目标、成功标准
├── architecture_decisions.md         # 技术决策和权衡
├── tech_stack.md                     # 技术栈定义和版本
├── weekly_assignments.md             # 每周作业规划和进度
│
├── ============ 开发级内存 ============
├── code_patterns.md                  # 代码模式和约定
├── development_workflow.md           # 开发流程规范
├── testing_strategies.md             # 测试策略和覆盖目标
│
├── ============ 知识级内存 ============
├── common_issues_solutions.md        # 常见问题和解决方案
├── llm_integration_patterns.md       # LLM 集成模式
├── security_considerations.md        # 安全考虑和最佳实践
│
└── ============ 协作级内存 ============
    ├── agent_communication_log.md    # AI 代理交互历史
    ├── learning_progress.md          # 学习进度追踪
    └── session_history.md            # 会话历史记录
```

### 1.2 内存类型详解

#### 项目级内存 (Project Memories)

| 文件 | 用途 | 更新频率 | 维护者 |
|------|------|----------|--------|
| **project_context_and_goals.md** | 项目愿景、目标、成功标准 | 季度/月度 | PM Agent |
| **architecture_decisions.md** | 技术选择、权衡、理由 | 按需 | Tech Lead |
| **tech_stack.md** | 技术栈、版本、依赖 | 按需 | Python Expert |
| **weekly_assignments.md** | 每周作业规划 | 每周 | PM Agent |

#### 开发级内存 (Development Memories)

| 文件 | 用途 | 更新频率 | 维护者 |
|------|------|----------|--------|
| **code_patterns.md** | 编码规范、设计模式 | 每月 | Code Reviewer |
| **development_workflow.md** | 开发流程、工具使用 | 双周 | DevOps Expert |
| **testing_strategies.md** | 测试策略、覆盖目标 | 双周 | Testing Expert |

#### 知识级内存 (Knowledge Memories)

| 文件 | 用途 | 更新频率 | 维护者 |
|------|------|----------|--------|
| **common_issues_solutions.md** | 错误和解决方案 | 实时 | Any Agent |
| **llm_integration_patterns.md** | LLM 调用模式 | 按需 | ML Expert |
| **security_considerations.md** | 安全模式和漏洞 | 按需 | Security Expert |

#### 协作级内存 (Collaboration Memories)

| 文件 | 用途 | 更新频率 | 维护者 |
|------|------|----------|--------|
| **agent_communication_log.md** | 代理交互历史 | 实时 | PM Agent |
| **learning_progress.md** | 学习里程碑 | 每周 | PM Agent |
| **session_history.md** | 会话总结 | 每次会话 | PM Agent |

### 1.3 现有内存文件示例

#### project_context_and_goals.md 结构

```markdown
# Project Context and Goals

High-level project vision, objectives, and success criteria.

---

## Course: CS146S Modern Software Developer

**Philosophy:** Learn by doing. Build real AI-powered applications progressing from basic prompting to sophisticated multi-agent systems over 8 weeks.

**Instructor:** Stanford CS Department
**Duration:** 8 weeks
**Format:** Weekly assignments with increasing complexity

---

## Learning Journey

[...]

---

## Project Vision

Build an **AI-powered productivity assistant** that:
1. Extracts action items from unstructured text (notes, emails, documents)
2. Manages tasks with intelligent prioritization
3. Integrates with external tools (Notion, calendars, etc.)
4. Learns from user behavior to improve recommendations

---

## Technical Architecture

[ASCII diagram]

---

## Personal Goals

### Primary Goals (Must Achieve)
1. ✅ Master prompt engineering for reliable LLM outputs
2. 🟡 Build production-ready FastAPI applications with proper error handling

### Secondary Goals (Should Achieve)
5. 🟡 Develop clean, maintainable code following Python best practices
6. 🟡 Learn security patterns for AI applications

---

## Success Criteria

| Week | Criterion | Target | Status |
|------|-----------|--------|--------|
| 1 | Prompt engineering mastery | 8+ prompt patterns | ✅ Complete |
| 2 | LLM integration working | Action item extraction | 🟡 In progress |
```

#### architecture_decisions.md 结构

```markdown
# Architecture Decisions

Record of significant architectural choices with rationale and implications.

---

## Database Architecture

### Decision: SQLite with Custom Exception Hierarchy

**Context:** Need reliable database operations with proper error handling for a FastAPI application.

**Options Considered:**
1. Direct sqlite3 with try/except
2. SQLAlchemy with default exceptions
3. SQLAlchemy with custom exception hierarchy ✅ **CHOSEN**

**Rationale:**
- Custom exceptions provide domain-specific error semantics
- Enables global exception handlers for consistent API responses
- Separates database errors from business logic errors

**Implementation:**
```python
# app/db/exceptions.py
class DatabaseError(Exception):
    """Base database error"""
    pass

class NotFoundError(DatabaseError):
    """Resource not found in database"""
    pass
```

**Implications:**
- Pros: Clean error handling, type-safe error catching
- Cons: Additional boilerplate for custom exception classes

**Alternatives for Future:**
- PostgreSQL for production scaling
- Connection pooling for high concurrency

---

## Decision Log Template

For future architectural decisions, use this template:

```markdown
### Decision: [Title]

**Context:** [What problem are we solving?]

**Options Considered:**
1. [Option 1]
2. [Option 2]
3. [Option 3] ✅ **CHOSEN**

**Rationale:**
- [Reason 1]
- [Reason 2]

**Implementation:**
[Code snippet or architecture diagram]

**Implications:**
- Pros: [List advantages]
- Cons: [List disadvantages]
```
```

#### code_patterns.md 结构

```markdown
# Code Patterns and Conventions

## Database Layer
- Custom exceptions: `DatabaseError`, `NotFoundError`
- SQLAlchemy 2.0+ async patterns
- Service layer pattern for business logic

## API Structure
- Routers in: `app/routers/`
- Services in: `app/services/`
- Global exception handlers in FastAPI apps

## Testing
- Test paths configured for weeks 1-8
- pytest with async test support
- TestClient for endpoint testing

## Error Handling
- Consistent error response format
- HTTP status codes aligned with REST best practices
```

---

## 标准化模板设计

### 2.1 通用记忆模板

```markdown
# {Title}

> {Brief description (1-2 sentences)}

---

## Metadata

| 字段 | 值 |
|------|-----|
| **创建时间** | {YYYY-MM-DD} |
| **最后更新** | {YYYY-MM-DD} |
| **维护者** | {Role/Agent Name} |
| **状态** | {Draft | Active | Deprecated} |
| **相关记忆** | [{Link 1}]({path 1}), [{Link 2}]({path 2}) |

---

## Purpose

{Why this memory exists, what problem it solves}

---

## Content

{Main content of the memory}

---

## Examples

### Example 1: {Example Title}

**Context**: {When this pattern applies}

**Problem**: {What problem does it solve?}

**Solution**: {How to apply this pattern}

```python
# Code example
{code}
```

**Result**: {Expected outcome}

---

## Common Pitfalls

| Pitfall | Why it happens | How to avoid |
|---------|---------------|--------------|
| {Pitfall 1} | {Reason} | {Solution} |
| {Pitfall 2} | {Reason} | {Solution} |

---

## Related Resources

### Internal
- [{Memory 1}]({path 1})
- [{Memory 2}]({path 2})

### External
- [{Resource 1}]({url 1})
- [{Resource 2}]({url 2})

---

## Changelog

| 日期 | 变更 | 作者 |
|------|------|------|
| {YYYY-MM-DD} | {Initial creation} | {Author} |
| {YYYY-MM-DD} | {Change description} | {Author} |

---

## Tags

{tag1}, {tag2}, {tag3}
```

### 2.2 决策记录模板 (ADR)

```markdown
# ADR-{number}: {Decision Title}

**Date**: {YYYY-MM-DD}
**Status**: {Proposed | Accepted | Deprecated | Superseded}
**Decision Maker**: {Role/Agent}

---

## Context

{What is the issue that we're facing that needs a decision?}

---

## Decision

{What is the change that we're proposing and/or doing?}

---

## Status

{Proposed | Accepted | Rejected | Deprecated | Superseded by [ADR-number]}

---

## Consequences

### Positive
- {Benefit 1}
- {Benefit 2}

### Negative
- {Drawback 1}
- {Drawback 2}

### Neutral
- {Note 1}
- {Note 2}

---

## Alternatives Considered

### Option 1: {Title}
- **Pros**: {Pros}
- **Cons**: {Cons}

### Option 2: {Title}
- **Pros**: {Pros}
- **Cons**: {Cons}

### Option 3 (Chosen): {Title}
- **Pros**: {Pros}
- **Cons**: {Cons}
- **Rationale**: {Why this option was chosen}

---

## References

- [{Link 1}]({url 1})
- [{Link 2}]({url 2})
```

### 2.3 问题解决方案模板

```markdown
# {Problem Title}

> {Brief problem description}

---

## Problem Statement

**Symptom**: {What did you observe?}

**Error Message** (if applicable):
```
{error message}
```

**Context**:
- What I was doing: {action}
- Expected behavior: {expected}
- Actual behavior: {actual}

---

## Root Cause

{Why did this problem occur?}

---

## Solution

### Option 1: {Solution Title} ✅ Recommended

**Steps**:
1. {Step 1}
2. {Step 2}

```python
# Code example
{code}
```

**Pros**: {Advantages}
**Cons**: {Disadvantages}

### Option 2: {Alternative Solution}

**Steps**:
1. {Step 1}
2. {Step 2}

---

## Prevention

{How to prevent this problem in the future}

---

## Related Issues

- [{Issue 1}]({link 1})
- [{Issue 2}]({link 2})

---

## References

- [{Resource 1}]({url 1})
```

---

## 记忆组织原则

### 3.1 按主题分类

```
原则: 每个记忆文件有明确的主题

良好示例:
✓ architecture_decisions.md    # 主题: 架构决策
✓ testing_strategies.md        # 主题: 测试策略
✓ code_patterns.md             # 主题: 代码模式

不良示例:
✓ notes.md                     # 主题不明确
✓ stuff.md                     # 太泛
✓ misc.md                      # 垃圾文件
```

### 3.2 按层次结构

```
原则: 相关记忆应该链接

project_context_and_goals.md
    │
    ├─► tech_stack.md          # 从上下文引用技术栈
    ├─► architecture_decisions.md  # 从上下文引用决策
    └─► weekly_assignments.md  # 从上下文引用作业

architecture_decisions.md
    │
    └─► code_patterns.md       # 决策影响代码模式
```

### 3.3 按访问频率

```
高频访问 (每次会话):
├── session_history.md         # 恢复上下文
├── code_patterns.md           # 参考编码规范
└── testing_strategies.md      # 测试指导

中频访问 (每周):
├── project_context_and_goals.md  # 检查目标
├── weekly_assignments.md      # 查看任务
└── learning_progress.md       # 追踪进度

低频访问 (按需):
├── architecture_decisions.md  # 新决策时
├── common_issues_solutions.md  # 遇到问题时
└── security_considerations.md  # 安全审查时
```

---

## 写作规范和示例

### 4.1 命名规范

| 规范 | 示例 | 说明 |
|------|------|------|
| **小写 + 下划线** | `code_patterns.md` | 默认命名 |
| **描述性名称** | `architecture_decisions.md` | 清晰表明内容 |
| **避免缩写** | `testing_strategies.md` 而非 `test_strat.md` | 完整单词 |
| **使用复数** | `common_issues_solutions.md` | 多个条目 |

### 4.2 结构规范

#### 标题层级

```markdown
# H1: 文件标题 (每个文件只有一个)

## H2: 主要章节

### H3: 子章节

#### H4: 细节 (尽量避免更深)

# ❌ 不要: H5 或 H6
```

#### 列表格式

```markdown
# 无序列表 (用于没有优先级的项目)
- Item 1
- Item 2
- Item 3

# 有序列表 (用于步骤或优先级)
1. Step 1
2. Step 2
3. Step 3

# 定义列表 (用于术语)
**Term**
: Definition

# 任务列表 (用于检查清单)
- [ ] Incomplete task
- [x] Completed task
```

#### 代码块格式

```markdown
# 带语言标识的代码块 (推荐)
```python
def example():
    pass
```

# 不带语言标识 (不推荐)
```
def example():
    pass
```
```

### 4.3 内容规范

#### 决策记录示例

```markdown
## Decision: Use FastAPI over Flask

**Date**: 2025-12-28
**Status**: Accepted

### Context
Building a REST API for the action item extraction feature. Need to choose between FastAPI and Flask.

### Options Considered

#### Option 1: Flask
**Pros**:
- Lightweight and flexible
- Large ecosystem
- Familiar to many developers

**Cons**:
- No built-in async support
- Manual API documentation
- Less type safety

#### Option 2: FastAPI ✅ CHOSEN
**Pros**:
- Native async support
- Automatic OpenAPI documentation
- Pydantic data validation
- Type hints throughout

**Cons**:
- More opinionated structure
- Younger framework (though stable)

### Rationale
Chose FastAPI because:
1. Project requires async for LLM calls
2. Automatic API docs save development time
3. Pydantic validation prevents bugs
4. Type hints align with modern Python practices

### Implementation
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Note(BaseModel):
    title: str
    content: str

@app.post("/notes")
async def create_note(note: Note):
    return {"id": 1, **note.dict()}
```

### Implications
- **Positive**: Faster development, better API docs, async from day one
- **Negative**: Learning curve for team unfamiliar with FastAPI
```

#### 代码模式示例

```markdown
## Service Layer Pattern

### Purpose
Separate business logic from HTTP handlers for better testability and reusability.

### Structure

```python
# services/extract.py
class ExtractService:
    """Handles LLM-based action item extraction"""

    def __init__(self, db: Database, llm: LLMClient):
        self.db = db
        self.llm = llm

    async def extract_from_note(self, note_id: int) -> list[ActionItem]:
        """Extract action items from a note"""
        note = await self.db.get_note(note_id)
        items = await self.llm.extract(note.content)
        return await self.db.create_action_items(items)
```

### Usage in Router

```python
# routers/notes.py
from fastapi import Depends
from services.extract import ExtractService

@router.post("/notes/{id}/extract")
async def extract_items(
    id: int,
    service: ExtractService = Depends()
):
    return await service.extract_from_note(id)
```

### Benefits
- **Testability**: Mock service for testing
- **Reusability**: Use service in multiple endpoints
- **Separation**: HTTP logic separate from business logic

### When to Use
- Complex business logic
- Multiple endpoints need same logic
- Need to test independently of HTTP layer
```

---

## 与 CLAUDE.md 的配合

### 5.1 职责划分

```
CLAUDE.md: 静态配置 (行为指南)
├── AI 团队角色定义
├── 工作流模式
├── Slash 命令定义
└── 代理选择规则

Serena memories: 动态知识 (项目学习)
├── 架构决策记录
├── 代码模式积累
├── 问题解决方案
└── 项目进度追踪
```

### 5.2 配合示例

#### 场景: 新功能开发

```yaml
步骤 1: AI 读取 CLAUDE.md
  - 发现: "FastAPI tasks → fastapi-expert"
  - 发现: "Always run code-reviewer before committing"

步骤 2: AI 读取 Serena memories
  - 读取: code_patterns.md (Service Layer Pattern)
  - 读取: architecture_decisions.md (FastAPI decision)
  - 读取: testing_strategies.md (pytest patterns)

步骤 3: 执行开发
  - 使用: fastapi-expert 实现功能
  - 遵循: Service Layer Pattern
  - 应用: pytest async patterns

步骤 4: 记录学习
  - 写入: architecture_decisions.md (新决策)
  - 写入: common_issues_solutions.md (遇到的问题)
```

### 5.3 交叉引用

```markdown
# 在 CLAUDE.md 中引用 Serena

## Key Project Patterns
For detailed patterns, see `.serena/memories/code_patterns.md`:
- Service layer pattern
- Database exception hierarchy
- Async I/O patterns
```

```markdown
# 在 Serena 中引用 CLAUDE.md

## Testing Strategy
Follow the AI team assignments in CLAUDE.md:
- Use @python-testing-expert for test improvements
- Target >80% coverage
- Use dependency overrides for test isolation
```

---

## 动态更新策略

### 6.1 更新触发条件

| 触发事件 | 更新的记忆 | 负责的 Agent |
|----------|-----------|-------------|
| **架构决策** | architecture_decisions.md | Tech Lead |
| **新的代码模式** | code_patterns.md | Code Reviewer |
| **问题解决** | common_issues_solutions.md | Any Agent |
| **测试改进** | testing_strategies.md | Testing Expert |
| **安全发现** | security_considerations.md | Security Expert |
| **会话结束** | session_history.md | PM Agent |
| **每周完成** | learning_progress.md | PM Agent |

### 6.2 更新流程

```yaml
标准更新流程:
  1. 识别需要更新的记忆
  2. 读取现有内容
  3. 追加或修改内容
  4. 更新 metadata (日期、作者)
  5. Git 提交变更

示例:
  用户: "我们决定使用 PostgreSQL 替代 SQLite"
    ↓
  AI:
    1. 识别: 这是架构决策
    2. 读取: architecture_decisions.md
    3. 追加: 新的 ADR 记录
    4. 更新: 最后更新日期
    5. 提交: "docs(serena): record PostgreSQL migration decision"
```

### 6.3 维护策略

#### 定期维护 (每周)

```bash
# 整理任务
- [ ] Review session_history.md for patterns
- [ ] Update learning_progress.md milestones
- [ ] Clean up outdated content
- [ ] Verify links between memories
```

#### 深度维护 (每月)

```bash
# 归档任务
- [ ] Archive completed weekly_assignments.md
- [ ] Consolidate related memories
- [ ] Update deprecated patterns
- [ ] Review and update tags
```

---

## 相关文档

| 主题 | 文档 |
|------|------|
| **架构概览** | [01-architecture-overview.md](01-architecture-overview.md) |
| **配置指南** | [02-configuration-guide.md](02-configuration-guide.md) |
| **跨机器同步** | [04-cross-machine-sync.md](04-cross-machine-sync.md) |

---

**下一步**: 阅读 [跨机器协作指南](04-cross-machine-sync.md) 了解多设备同步策略
