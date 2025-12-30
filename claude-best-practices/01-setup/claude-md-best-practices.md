# CLAUDE.md 最佳实践指南

> 本文档深入分析 CLAUDE.md 的最佳实践，包括结构设计、AI 团队配置、与 PROJECT_INDEX.json 的配合等。

---

## 目录

1. [CLAUDE.md 的作用](#claudemd-的作用)
2. [应该包含的部分](#应该包含的部分)
3. [信息组织原则](#信息组织原则)
4. [AI 团队角色定义](#ai-团队角色定义)
5. [与 PROJECT_INDEX.json 配合](#与-project_indexjson-配合)
6. [当前项目分析](#当前项目分析)
7. [改进建议](#改进建议)

---

## CLAUDE.md 的作用

### 核心定位

**CLAUDE.md 是项目给 Claude Code 的"大脑说明书"** - 它告诉 AI 如何思考、如何工作、如何与其他工具协作。

### 三大功能

| 功能 | 说明 | 关键词 |
|------|------|--------|
| **行为指南** | 定义 AI 应该如何表现和响应 | Persona, Constraints, Rules |
| **结构映射** | 描述项目架构和关键模式 | Tech Stack, Patterns, Conventions |
| **工作流编排** | 指定如何使用子代理和命令 | Agents, Commands, Workflows |

---

## 应该包含的部分

### 必备部分 (Must Have)

#### 1. 项目上下文 (Project Context)

```markdown
# CLAUDE.md

This document contains configuration and guidance for Claude Code agents
working on [PROJECT_NAME].

## Project Overview

- **Type**: [Web App / CLI Tool / Library / Course Assignment]
- **Primary Language**: [Python / JavaScript / etc.]
- **Core Framework**: [FastAPI / React / Django / etc.]
```

**原因**: AI 需要知道它工作的环境类型，以便调整其行为模式。

#### 2. 技术栈检测 (Detected Tech Stack)

```markdown
### Detected Tech Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | FastAPI (Python 3.10+) |
| Database | SQLite with SQLAlchemy 2.0+ |
| Frontend | Vanilla JavaScript + HTML/CSS |
| Testing | pytest + httpx |
```

**最佳实践**:
- 使用表格格式便于快速扫描
- 包含版本信息（如有）
- 按层次分类（Backend, Frontend, DevOps, Testing）

#### 3. AI 团队配置 (AI Team Configuration)

```markdown
### AI Team Assignments

| Task | Agent | Notes |
|------|-------|-------|
| **All code changes** | `code-reviewer` | MUST run before committing |
| **FastAPI development** | `fastapi-expert` | Primary for API work |
| **Testing** | `python-testing-expert` | For pytest improvements |
```

**关键原则**:
- 明确优先级：哪个代理优先
- 明确强制性："MUST" vs "should"
- 明确适用场景：何时使用哪个代理

#### 4. 关键模式 (Key Project Patterns)

```markdown
### Key Project Patterns

- **Database**: SQLite with custom exceptions
- **API Structure**: FastAPI routers in `app/routers/`
- **Testing**: pytest with test paths configured
- **Error Handling**: Custom exception handlers
```

**原因**: 这些模式让 AI 理解项目约定，避免偏离团队风格。

---

### 推荐部分 (Should Have)

#### 5. 工作流指南 (Workflow Guide)

```markdown
### Weekly Assignment Workflow

1. **Start**: Use `code-archaeologist` to understand state
2. **Plan**: Use `fastapi-expert` to design implementation
3. **Implement**: Use appropriate specialist
4. **Test**: Use `python-testing-expert`
5. **Review**: ALWAYS use `code-reviewer` before committing
```

#### 6. 自定义命令 (Custom Commands)

```markdown
### Custom Slash Commands Available

| Command | Purpose |
|---------|---------|
| `/week` | Get help with weekly assignments |
| `/explore-week` | Deep dive into week state |
| `/test-week` | Run and analyze tests |
```

#### 7. 示例用法 (Example Usage)

```markdown
### Example Usage

# Implementing a new endpoint
Use @fastapi-expert to add a new notes endpoint

# Improving test coverage
Use @python-testing-expert to increase coverage
```

---

### 可选部分 (Nice to Have)

#### 8. 环境信息
```markdown
### Environment

- **Python**: 3.12.7 (Conda)
- **Package Manager**: Poetry 2.2.1
- **LLM**: Ollama (llama3.1:8b)
```

#### 9. 学习方法论
```markdown
### Learning Methodology

This project follows the BPRT Cycle:
- **Build**: Hands-on implementation
- **Prompt**: Optimize AI interaction
- **Reflect**: Compare outputs
- **Teach**: Create notes
```

---

## 信息组织原则

### 1. 层次化结构 (Hierarchical Structure)

```
CLAUDE.md
├── Header (项目标识)
├── AI Team Config (AI 如何协作)
│   ├── Tech Stack (技术环境)
│   ├── Agent Assignments (谁做什么)
│   └── Selection Priority (优先级)
├── Project Patterns (代码约定)
└── Usage Examples (如何使用)
```

**原则**: 从"谁"到"什么"到"如何"

### 2. 信息密度原则 (Information Density)

| 部分 | 信息密度 | 原因 |
|------|----------|------|
| Tech Stack 表格 | 高 | 快速扫描 |
| Agent Assignments | 高 | 决策指导 |
| Example Usage | 中 | 实战参考 |
| Text Description | 低 | 避免冗长 |

### 3. 可扫描性 (Scannability)

使用以下元素增强可扫描性:

```markdown
# 主标题 (H1)
## 次标题 (H2)
### 三级标题 (H3)

**加粗文本** 强调关键点
`代码字体` 标记技术术语
| 表格 | 结构化数据 |
- 列表 | 并行项目
> 引用 | 重要提示
```

---

## AI 团队角色定义

### 角色定义模板

```markdown
| Task | Agent | Notes |
|------|-------|-------|
| [任务类型] | `[agent-name]` | [使用场景 + 强制性] |
```

### 角色分类体系

#### 1. 强制性角色 (Must-Use)

| Agent | 使用场景 | 强制性标记 |
|-------|----------|-----------|
| `code-reviewer` | 所有代码变更后 | **MUST** |
| `security-expert` | 安全相关代码 | **MUST** |

#### 2. 框架专家 (Framework Specialists)

| Agent | 触发条件 | 优先级 |
|-------|----------|--------|
| `fastapi-expert` | FastAPI 相关任务 | 最高 |
| `django-expert` | Django 相关任务 | 最高 |
| `react-expert` | React 相关任务 | 最高 |

#### 3. 通用专家 (General Specialists)

| Agent | 触发条件 | 优先级 |
|-------|----------|--------|
| `python-expert` | Python 非框架任务 | 高 |
| `testing-expert` | 测试相关 | 高 |
| `performance-optimizer` | 性能问题 | 中 |

### 优先级决策树

```text
开始任务
    │
    ├─ 是否安全相关？ → YES → python-security-expert
    │                 → NO  ↓
    ├─ 是否有框架专家？ → YES → [框架]-expert
    │                 → NO  ↓
    ├─ 是否性能问题？ → YES → performance-optimizer
    │                 → NO  ↓
    └─ 使用通用专家 → python-expert / general-purpose

    (最后必须使用 code-reviewer)
```

---

## 与 PROJECT_INDEX.json 配合

### 职责划分

| 文件 | 主要职责 | 更新频率 |
|------|----------|----------|
| **CLAUDE.md** | AI 行为指南 | 低频（架构变化时） |
| **PROJECT_INDEX.json** | 项目结构映射 | 中频（功能迭代时） |

### 配合模式

#### 模式 1: 索引优先 (Index-First)

```markdown
## CLAUDE.md

For complete project structure, see [PROJECT_INDEX.json](./PROJECT_INDEX.json).

Quick navigation:
- Week 1-2: Prompt Engineering
- Week 3-4: MCP & Claude Code
```

**优点**: CLAUDE.md 保持简洁
**缺点**: 需要额外跳转

#### 模式 2: 关键摘要 + 索引引用 (推荐)

```markdown
## CLAUDE.md

### Weekly Structure Overview

| Week | Theme | Key Files |
|------|-------|-----------|
| 1 | Prompt Engineering | week1/*.py |
| 2 | LLM Apps | week2/app/ |

For detailed file listings and learning notes, see [PROJECT_INDEX.json](./PROJECT_INDEX.json).
```

**优点**: 平衡简洁与信息
**缺点**: 需要维护两处

#### 模式 3: 完全独立 (Independent)

```markdown
## CLAUDE.md

### Project Structure

[完整的项目结构描述...]

### Tech Stack

[完整的技术栈描述...]

[不需要引用 PROJECT_INDEX.json]
```

**优点**: 自包含，无需跳转
**缺点**: 冗余，难以同步维护

### 推荐配合策略

```markdown
## CLAUDE.md

### Navigation Guide

📖 **Structure**: See [PROJECT_INDEX.json](./PROJECT_INDEX.json) for complete file listings
🤖 **AI Team**: Use the agents below based on task type
📋 **Patterns**: Follow the key patterns defined here
🔧 **Commands**: Use custom slash commands for common tasks

---

## AI Team Configuration

[AI 团队配置...]

---

## Key Patterns

[关键模式...]

---

## Quick Reference

| For                   | Use                        |
|-----------------------|----------------------------|
| Project structure     | PROJECT_INDEX.json         |
| Weekly assignments    | /week command              |
| Code exploration      | /explore-week command      |
| Testing               | /test-week command         |
```

---

## 当前项目分析

### 当前 CLAUDE.md 优点

1. ✅ **清晰的 AI 团队配置表格** - 一目了然的任务到代理映射
2. ✅ **技术栈检测信息完整** - 包含版本和环境信息
3. ✅ **工作流指南明确** - Weekly Assignment Workflow 步骤清晰
4. ✅ **自定义命令列表** - 方便用户发现可用功能
5. ✅ **代理优先级明确** - Agent Selection Priority 部分

### 当前 CLAUDE.md 缺点

1. ❌ **缺少项目概览** - 没有高层项目描述
2. ❌ **与 PROJECT_INDEX 关联弱** - 没有引用或导航提示
3. ❌ **缺少约束说明** - 没有明确的限制和禁忌
4. ❌ **错误处理指导缺失** - 没有说明如何处理错误情况
5. ❌ **缺少元数据** - 没有生成日期、版本等信息

---

## 改进建议

### 建议的新结构

```markdown
# CLAUDE.md

## Header Section
- Project metadata (generated date, version)
- Project purpose (1-2 sentences)

## AI Team Configuration
- Tech Stack Detection
- Agent Assignments (with priority)
- Selection Decision Tree
- Workflow Guidelines

## Project Patterns & Conventions
- Code structure patterns
- Naming conventions
- Error handling patterns
- Testing patterns

## Navigation & Resources
- Link to PROJECT_INDEX.json
- Custom commands
- Quick reference

## Constraints & Edge Cases
- What NOT to do
- Error handling guidelines
- When to ask for help
```

### 具体改进点

#### 1. 添加项目概览

```markdown
# CLAUDE.md

**Last Updated**: 2025-12-28
**Version**: 2.0
**Auto-generated by**: team-configurator

---

## Project Overview

This is the CS146S Modern Software Developer course assignments repository.
It contains 8 weeks of progressive learning materials covering AI-assisted
software development, from prompt engineering to multi-agent workflows.

**Course Website**: https://themodernsoftware.dev
**Institution**: Stanford University
**Term**: Fall 2025
```

#### 2. 增强 PROJECT_INDEX 引用

```markdown
## Navigation

### For AI Agents

1. **First**: Read [PROJECT_INDEX.json](./PROJECT_INDEX.json) for project structure
2. **Then**: Use the AI team below for task execution
3. **Finally**: Always run `code-reviewer` before committing

### For Learners

1. Read [learning_notes/00_learning_strategy.md](./learning_notes/00_learning_strategy.md)
2. Use `/week [N]` commands for week-specific help
3. Follow BPRT cycle: Build → Prompt → Reflect → Teach
```

#### 3. 添加约束说明

```markdown
## Constraints & Guidelines

### MUST NOT

- ❌ Skip code-reviewer before commits
- ❌ Modify test files without running tests
- ❌ Add dependencies without updating pyproject.toml
- ❌ Hardcode credentials or API keys

### SHOULD

- ✅ Ask clarifying questions for ambiguous tasks
- ✅ Use existing project patterns
- ✅ Update documentation when adding features
- ✅ Follow PEP 8 for Python code

### WHEN IN DOUBT

- 🤔 Use `/week` command for context
- 🔍 Use `/explore-week` to understand state
- 📖 Reference PROJECT_INDEX.json for structure
```

#### 4. 改进代理选择指南

```markdown
### Agent Selection Decision Tree

```text
                    Start Task
                       │
           ┌───────────┴───────────┐
           │                       │
    Security Related?         No
           │                       │
           ↓                  Framework Specific?
    python-security          │
       -expert              │
                          ├─── Yes → [Framework]-expert
                          │          (fastapi, react, django)
                          │
                          └─── No → Task Type?
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
               Performance?    Testing?     General Code?
                    │               │               │
                    ↓               ↓               ↓
          performance-    python-testing-  python-expert
             optimizer         expert          or
                                   general-purpose
                                    │
                                    ↓
                            code-reviewer
                         (ALWAYS - Mandatory)
```
```

### Quick Reference Card

```markdown
## Quick Reference

| Task | Command | Agent |
|------|---------|-------|
| New feature | `/week` | Plan → [Framework]-expert → Implement |
| Debug issue | `/explore-week` | General-purpose |
| Add tests | `/test-week` | python-testing-expert |
| Refactor code | `/refactor` | [Framework]-expert |
| Review PR | `review-pr` | code-reviewer |
```

---

## 完整示例

基于以上分析，这是一个改进后的 CLAUDE.md 模板：

```markdown
# CLAUDE.md

**Last Updated**: 2025-12-28
**Version**: 2.0
**Auto-generated by**: team-configurator
**Project**: CS146S Modern Software Developer

---

## Project Overview

This repository contains 8 weeks of progressive assignments for the CS146S
Modern Software Developer course at Stanford University. The course teaches
AI-assisted software development, from prompt engineering (Week 1) to
multi-stack development (Week 8).

**Learning Methodology**: BPRT Cycle (Build → Prompt → Reflect → Teach)
**Primary Language**: Python 3.10+
**Core Frameworks**: FastAPI, SQLAlchemy, Ollama LLM

---

## 📖 Navigation

**First Steps**:
- 📁 [PROJECT_INDEX.json](./PROJECT_INDEX.json) - Complete project structure
- 📚 [learning_notes/00_learning_strategy.md](./learning_notes/00_learning_strategy.md) - Learning methodology
- 🤖 [.claude/SUBAGENT_GUIDE.md](./.claude/SUBAGENT_GUIDE.md) - Subagent usage

**Quick Commands**:
- `/week [N]` - Get help with week N assignment
- `/explore-week` - Deep dive into current week state
- `/test-week` - Run and analyze tests

---

## 🤖 AI Team Configuration

**CRITICAL**: You MUST use subagents when available for the task.

### Detected Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Backend | FastAPI | ≥0.111.0 |
| Database | SQLite + SQLAlchemy | ≥2.0.0 |
| LLM | Ollama (llama3.1:8b) | 0.5.3 |
| Testing | pytest + httpx | ≥7.0.0 |
| Quality | Black, Ruff, pre-commit | Latest |

### Agent Assignments (Priority Order)

| Priority | Agent | When to Use | Mandatory |
|----------|-------|-------------|-----------|
| 1 | `code-reviewer` | After ANY code change | **YES** |
| 2 | `python-security-expert` | Security-related code | **YES** |
| 3 | `fastapi-expert` | FastAPI tasks (endpoints, routers) | Recommended |
| 4 | `python-testing-expert` | Test writing/improvement | Recommended |
| 5 | `python-expert` | General Python tasks | Recommended |
| 6 | `performance-optimizer` | Performance issues | As needed |

### Decision Flow

```text
Security Task? → YES → python-security-expert
                  NO
      ↓
FastAPI Task? → YES → fastapi-expert
                  NO
      ↓
Test Task? → YES → python-testing-expert
                  NO
      ↓
Performance? → YES → performance-optimizer
                  NO
      ↓
Use python-expert or general-purpose
      ↓
ALWAYS end with code-reviewer
```

---

## 🏗️ Project Patterns

### Code Structure

```
week[N]/
├── app/
│   ├── main.py          # FastAPI app entry
│   ├── routers/         # API endpoints
│   ├── services/        # Business logic
│   └── models/          # Data models
├── tests/               # pytest tests
├── pyproject.toml       # Dependencies
└── Makefile            # Common commands
```

### Key Conventions

- **Database**: SQLite with custom exceptions (`DatabaseError`, `NotFoundError`)
- **Routers**: One file per resource in `app/routers/`
- **Services**: Business logic in `app/services/`
- **Tests**: Mirror `app/` structure in `tests/`
- **Error Handling**: Custom exception handlers in FastAPI apps

### Testing Pattern

```python
# Standard test pattern
def test_[feature]_[scenario]:
    # Arrange
    ...

    # Act
    ...

    # Assert
    ...
```

---

## 📋 Workflow Guidelines

### Weekly Assignment Workflow

1. **Explore**: Use `/explore-week` to understand current state
2. **Plan**: Use appropriate expert to design implementation
3. **Implement**: Use specialist agent for coding
4. **Test**: Use `/test-week` to verify
5. **Review**: ALWAYS use `code-reviewer` before committing

### Commit Workflow

```text
Code Change
    ↓
[Specialist Agent] Implementation
    ↓
code-reviewer (MANDATORY)
    ↓
Fix Issues (if any)
    ↓
git commit
```

---

## ⚠️ Constraints & Guidelines

### MUST NOT

- ❌ Skip `code-reviewer` before commits
- ❌ Modify tests without running them first
- ❌ Add dependencies without updating `pyproject.toml`
- ❌ Hardcode credentials (use environment variables)
- ❌ Commit `.env` or credential files

### SHOULD

- ✅ Ask clarifying questions for ambiguous tasks
- ✅ Use existing project patterns and conventions
- ✅ Update documentation when adding features
- ✅ Follow PEP 8 for Python code
- ✅ Write tests for new functionality

### WHEN TO ASK FOR HELP

- 🤔 Task scope is unclear
- 🔍 Multiple valid approaches exist
- ⚠️ Security implications unclear
- 📊 Breaking changes needed

---

## 🔧 Custom Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/week [N]` | Week-specific help | Starting a week's work |
| `/explore-week` | Explore week state | Understanding what exists |
| `/test-week` | Run and analyze tests | After code changes |
| `/llm-extract` | LLM extraction help | Week 2 assignments |
| `/mcp-server` | MCP server help | Week 3 assignments |
| `/refactor` | Code cleanup | Improving code quality |

---

## 📚 Key Resources

### Internal

- [PROJECT_INDEX.json](./PROJECT_INDEX.json) - Complete project structure
- [learning_notes/](./learning_notes/) - Weekly learning summaries
- [.claude/commands/](./.claude/commands/) - Custom command definitions

### External

- [Course Website](https://themodernsoftware.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Claude Code Docs](https://docs.anthropic.com/claude-code)
- [MCP Protocol](https://modelcontextprotocol.io)

---

## 📊 Project Statistics

- **Total Weeks**: 8
- **Python Files**: 90
- **Test Files**: 17
- **Code Coverage**: 85%
- **Custom Commands**: 6
- **Learning Notes**: 21

---

*For detailed weekly breakdown, see [PROJECT_INDEX.json](./PROJECT_INDEX.json)*
```

---

## 总结

### CLAUDE.md 设计原则

1. **简洁优先** - 不要重复 PROJECT_INDEX.json 的内容
2. **行动导向** - 告诉 AI "做什么" 而不是 "是什么"
3. **决策支持** - 提供清晰的决策树和优先级
4. **可维护性** - 结构化、模块化、易于更新

### 与其他文件的配合

```text
                    CLAUDE.md
                   (AI 如何工作)
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   PROJECT_INDEX   .claude/      learning_notes/
   (项目结构)      commands/      (学习材料)
                  (交互接口)
```

### 持续改进

CLAUDE.md 应该是:
- **动态的** - 随项目演进而更新
- **反馈驱动的** - 根据使用情况调整
- **可测试的** - 验证 AI 是否遵循指导

---

**最后更新**: 2025-12-28
**下一步**: 根据项目具体需求调整模板
