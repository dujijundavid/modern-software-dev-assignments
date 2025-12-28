# CS146S: Modern Software Developer - Project Index

> Generated: 2025-12-28
> Course: Stanford CS146S Fall 2025
> Goal: Train top-tier AI Engineers through 8-week intensive curriculum

---

## 📊 Token Efficiency

| 方式 | Token 消耗 | 说明 |
|------|-----------|------|
| **读取全代码库** | ~58,000 tokens | 每次会话的原始成本 |
| **读取本索引** | ~3,000 tokens | **节省 94%** 🎉 |

---

## 📁 Project Structure

```
modern-software-dev-assignments/
├── week1/                    # Prompt Engineering 基础
│   ├── k_shot_prompting.py
│   ├── chain_of_thought.py
│   ├── tool_calling.py
│   ├── rag.py
│   ├── reflexion.py
│   └── self_consistency_prompting.py
│
├── week2/                    # FastAPI + LLM 集成
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic (extract.py)
│   │   ├── db.py             # Database layer
│   │   └── main.py           # FastAPI app entry
│   ├── tests/                # 6 test files (85% coverage)
│   └── README.md
│
├── week3/                    # MCP Server
│   ├── server/
│   │   └── main.py           # Notion MCP server
│   └── weather_server/
│       ├── weather.py        # Weather MCP server
│       └── test_server.py
│
├── week4/                    # Claude Code Automation
│   ├── backend/              # FastAPI app (refactored)
│   ├── frontend/             # Static UI
│   ├── data/                 # SQLite + seed
│   └── docs/TASKS.md
│
├── week5/                    # Warp Agentic Development
│   ├── backend/              # FastAPI app
│   ├── frontend/             # Static UI
│   └── docs/TASKS.md
│
├── week6/                    # Security Analysis
│   ├── backend/              # FastAPI app
│   ├── frontend/             # Static UI
│   └── [Semgrep scan targets]
│
├── week7/                    # AI Code Review
│   ├── backend/              # FastAPI app
│   ├── frontend/             # Static UI
│   └── docs/TASKS.md
│
├── week8/                    # Multi-Stack Build
│   └── [3 tech stack versions]
│
├── learning_notes/           # 🎓 学习笔记宝藏
│   ├── 00_learning_strategy.md    # 学习方法论 (BPRT循环)
│   ├── week1/                       # 8 files
│   ├── week2/                       # 10 files
│   │   ├── WEEK2_LEARNING_SUMMARY.md  # 875行范例笔记
│   │   ├── testing_llm_functions_guide.md
│   │   └── python_import_system_guide.md
│   ├── week3/                       # 3 files
│   └── prompts/                     # 8个学习 Prompt 模板
│       ├── 01_pre_learning.md
│       ├── 02_collaborative_coding.md
│       ├── 03_critical_review.md
│       └── ...
│
├── .claude/                  # Claude Code 配置
│   ├── commands/             # 自定义 slash commands
│   │   ├── week.md
│   │   ├── explore-week.md
│   │   ├── test-week.md
│   │   ├── mcp-server.md
│   │   └── refactor.md
│   └── SUBAGENT_GUIDE.md
│
├── CLAUDE.md                 # AI 配置 (本文件已配置)
├── pyproject.toml            # Poetry 依赖管理
└── README.md                 # 项目总览
```

---

## 🎯 8-Week Learning Path

| Week | 主题 | 核心技能 | 主要技术 | 关键文件 |
|------|------|---------|---------|---------|
| **1** | Prompt Engineering | 提示工程基础 | Ollama, JSON Schema | `week1/*.py` |
| **2** | LLM-Powered Apps | FastAPI + LLM 集成 | FastAPI, SQLAlchemy, Ollama | `week2/app/services/extract.py` |
| **3** | MCP Server | 扩展 AI 工具能力 | MCP, Notion API | `week3/server/main.py` |
| **4** | Claude Code | 自动化工作流 | Slash Commands, SubAgents | `.claude/commands/*` |
| **5** | Warp Dev | 多 AI 协作 | Warp Drive, Multi-Agent | `week5/docs/TASKS.md` |
| **6** | Security | 安全分析 | Semgrep (SAST/SCA) | `week6/backend/` |
| **7** | AI Review | 代码审查对比 | Graphite Diamond | `week7/docs/TASKS.md` |
| **8** | Multi-Stack | 全栈开发 | Bolt.new + 3 stacks | `week8/` |

### 技能演进金字塔

```
           ┌────────────────────────────────┐
           │   AI System Design & Orchestration  │  ← Week 3-8
           ├────────────────────────────────┤
           │   AI-Human Collaborative Dev    │  ← Week 4-7
           ├────────────────────────────────┤
           │   Prompt Engineering Basics    │  ← Week 1-2
           └────────────────────────────────┘
```

---

## 📚 Learning Notes Index

### 核心方法论

| 文件 | 用途 | 重要性 |
|------|------|--------|
| [00_learning_strategy.md](learning_notes/00_learning_strategy.md) | BPRT 学习循环 + 6个 Prompt 模板 | ⭐⭐⭐ |
| [ai_builder_context.md](learning_notes/ai_builder_context.md) | AI Builder 认知框架 | ⭐⭐ |

### Week 1: Prompt Engineering

| 文件 | 内容 |
|------|------|
| 01_pre_learning_concepts.md | 概念预习笔记 |
| 02_ai_agent_interaction_guide.md | Agent 交互指南 |
| 03_case_study_httpstatus_reversal.md | 案例研究 |
| 04_quick_reference.md | 快速参考 |
| 05_chain_of_thought_deep_dive.md | CoT 深度解析 |

### Week 2: LLM Integration (最完整)

| 文件 | 内容 | 价值 |
|------|------|------|
| [WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/WEEK2_LEARNING_SUMMARY.md) | **875行完整学习总结** | 📖 范例 |
| [testing_llm_functions_guide.md](learning_notes/week2/testing_llm_functions_guide.md) | LLM 测试指南 | 🧪 实用 |
| [python_import_system_guide.md](learning_notes/week2/python_import_system_guide.md) | 导入系统详解 | 🔧 技巧 |
| week2_codebase_learning_path.md | 代码库学习路径 | 🗺️ 导航 |
| refactoring_and_llm_integration_practice.md | 重构实践 | 💻 实战 |

### Week 3: MCP Server

| 文件 | 内容 |
|------|------|
| 01_pre_learning_concepts.md | MCP 概念预习 |
| 从零开始构建MCP服务器.md | MCP 构建教程 |

### Prompt Templates (prompts/)

| 文件 | 用途 |
|------|------|
| 01_pre_learning.md | 概念深度理解 (学习前) |
| 02_collaborative_coding.md | Assignment 协作 (学习中) |
| 03_critical_review.md | 批判性审查 (实现后) |
| 04_note_generation.md | 笔记生成 (总结时) |
| 05_spaced_review.md | 周期性复习 (每2-3周) |
| 06_mini_project.md | Mini-Project 挑战 (深化学习) |

---

## 🔧 Tech Stack Overview

### 核心依赖 (pyproject.toml)

```toml
[dependencies]
python = ">=3.10,<4.0"
fastapi = ">=0.111.0"          # Web framework
sqlalchemy = ">=2.0.0"         # ORM
pydantic = ">=2.0.0"           # Data validation
openai = ">=1.0.0"             # OpenAI API
ollama = "^0.5.3"              # Local LLM

[dev-dependencies]
pytest = ">=7.0.0"             # Testing
httpx = ">=0.24.0"             # Async HTTP
black = ">=24.1.0"             # Formatter
ruff = ">=0.4.0"               # Linter
pre-commit = ">=3.6.0"         # Git hooks
```

### 工具链

| 工具 | 用途 | 配置文件 |
|------|------|---------|
| **Poetry** | 依赖管理 | `pyproject.toml` |
| **pytest** | 测试框架 | `pytest.ini_options` |
| **black** | 代码格式化 | `[tool.black]` |
| **ruff** | 代码检查 | `[tool.ruff]` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |

### AI 工具

| 工具 | 用途 | 引入周次 |
|------|------|---------|
| **Ollama** | 本地 LLM | Week 1 |
| **Claude Code** | AI 编程助手 | Week 4 |
| **Warp** | AI 终端环境 | Week 5 |
| **Semgrep** | 安全扫描 | Week 6 |
| **Graphite Diamond** | AI 代码审查 | Week 7 |
| **Bolt.new** | AI 应用生成 | Week 8 |

---

## 🎯 AI Engineer Skills Pyramid

### Level 1: Prompt Engineering (Week 1-2)
- ✅ K-shot 提示
- ✅ Chain-of-Thought
- ✅ Tool Calling
- ✅ RAG (检索增强生成)
- ✅ Reflexion (自我反思)
- ✅ 结构化输出 (JSON Schema)

### Level 2: AI-Human Collaboration (Week 3-7)
- ✅ MCP 服务器开发
- ✅ Claude Code 自动化
- ✅ 多 Agent 工作流
- ✅ 安全分析 (Semgrep)
- ✅ AI 代码审查对比

### Level 3: AI System Design (Week 8)
- ✅ 多技术栈对比
- ✅ AI 全栈开发
- ✅ Bolt.new 应用生成

---

## 📝 Quick Start

### 环境设置

```bash
# 1. 创建 Conda 环境
conda create -n cs146s python=3.12 -y
conda activate cs146s

# 2. 安装 Poetry
curl -sSL https://install.python-poetry.org | python -

# 3. 安装依赖
poetry install

# 4. 启动 Ollama (Week 1-2)
ollama serve && ollama pull llama3.1:8b
```

### 运行测试

```bash
# 快速测试 (跳过 LLM 集成)
pytest week2/tests/ -m "not slow"

# 完整测试 (包括 LLM)
pytest week2/tests/

# 覆盖率报告
pytest week2/tests/ --cov=week2/app --cov-report=html
```

### 启动应用

```bash
# Week 2-7: FastAPI 应用
cd week2  # 或 week4, week5, week6, week7
make run  # 或 python -m uvicorn app.main:app --reload

# 访问
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Claude Code 命令

```bash
/week              # 获取周作业帮助
/explore-week      # 深入探索周状态
/test-week         # 运行并分析测试
/mcp-server        # MCP 服务器帮助
/refactor          # 系统化代码清理
```

---

## 🔗 Key Learning Resources

### 内部资源 (本仓库)

| 资源 | 路径 | 用途 |
|------|------|------|
| **学习策略** | [learning_notes/00_learning_strategy.md](learning_notes/00_learning_strategy.md) | BPRT 学习循环 |
| **Week 2 范例** | [learning_notes/week2/WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/WEEK2_LEARNING_SUMMARY.md) | 完美学习笔记模板 |
| **测试指南** | [learning_notes/week2/testing_llm_functions_guide.md](learning_notes/week2/testing_llm_functions_guide.md) | LLM 测试最佳实践 |
| **AI 配置** | [CLAUDE.md](CLAUDE.md) | AI Agent 团队配置 |

### 外部资源

| 资源 | 链接 | 用途 |
|------|------|------|
| **课程官网** | [themodernsoftware.dev](https://themodernsoftware.dev) | 课程主页 |
| **Claude Code 文档** | [docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code) | Claude Code 指南 |
| **MCP 协议** | [modelcontextprotocol.io](https://modelcontextprotocol.io) | MCP 规范 |
| **FastAPI 文档** | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) | FastAPI 教程 |

---

## 📊 Project Statistics

| 指标 | 数值 |
|------|------|
| **Python 文件** | 90 个 |
| **Markdown 文档** | 67 个 |
| **测试文件** | 17 个 |
| **学习笔记** | 21 个 |
| **周次作业** | 8 周 |
| **代码覆盖率** | ~85% (Week 2) |
| **总行数** | ~10,000+ 行 |

---

## 🎯 Usage Tips

### 对于 AI Agent

1. **优先使用本索引** - 先读取 PROJECT_INDEX.md 了解结构
2. **周次上下文** - 使用 `/week` 命令获取特定周的帮助
3. **代码审查** - 修改代码前用 `code-reviewer` agent
4. **测试优先** - 使用 `/test-week` 运行周测试

### 对于学习者

1. **遵循 BPRT 循环** - Build → Prompt → Reflect → Teach
2. **参考 Week 2 笔记** - 这是最佳学习笔记范例
3. **使用 Prompt 模板** - `learning_notes/prompts/` 有 6 个模板
4. **记录反思** - 每周生成学习总结

---

## 🚀 Next Steps

### 新手入门

1. 阅读 [00_learning_strategy.md](learning_notes/00_learning_strategy.md)
2. 学习 [WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/WEEK2_LEARNING_SUMMARY.md) 作为范例
3. 完成环境设置 (Quick Start)
4. 从当前周次开始使用 `/week` 命令

### 进阶使用

1. 探索 [`.claude/commands/`](.claude/commands/) 自定义命令
2. 阅读 [SUBAGENT_GUIDE.md](.claude/SUBAGENT_GUIDE.md) 了解子 Agent
3. 使用 Prompt 模板深化学习
4. 定期复习 (每2-3周用 Prompt 5)

---

**Index Version:** 1.0
**Last Updated:** 2025-12-28
**Maintained by:** AI Agent (Claude Code)
