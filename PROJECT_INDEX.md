# CS146S: Modern Software Developer - Project Index

> Generated: 2025-12-30
> Course: Stanford CS146S Fall 2025
> Goal: Train top-tier AI Engineers through 8-week intensive curriculum

---

## Token Efficiency

| 方式 | Token 消耗 | 说明 |
|------|-----------|------|
| **读取全代码库** | ~58,000 tokens | 每次会话的原始成本 |
| **读取本索引** | ~3,000 tokens | **节省 94%** |

---

## Project Structure

```
modern-software-dev-assignments/
+-- week1/                    # Prompt Engineering 基础
|   +-- k_shot_prompting.py
|   +-- chain_of_thought.py
|   +-- tool_calling.py
|   +-- rag.py
|   +-- reflexion.py
|   +-- self_consistency_prompting.py
|
+-- week2/                    # FastAPI + LLM 集成
|   +-- app/
|   |   +-- routers/          # API endpoints (action_items.py, notes.py)
|   |   +-- services/         # Business logic (extract.py)
|   |   +-- db.py             # Database layer
|   |   +-- schemas.py        # Pydantic models
|   |   +-- main.py           # FastAPI app entry
|   +-- tests/                # 6 test files (~85% coverage)
|
+-- week3/                    # MCP Server
|   +-- server/main.py        # Notion MCP server
|   +-- weather_server/
|       +-- weather.py        # Weather MCP server
|       +-- test_server.py
|
+-- week4/                    # Claude Code Automation
|   +-- backend/              # FastAPI app (refactored)
|   +-- frontend/             # Static UI
|   +-- data/                 # SQLite + seed
|   +-- docs/TASKS.md
|
+-- week5/                    # Warp Agentic Development
|   +-- backend/              # FastAPI app
|   +-- frontend/             # Static UI
|   +-- docs/TASKS.md
|
+-- week6/                    # Security Analysis
|   +-- backend/              # FastAPI app
|   +-- frontend/             # Static UI
|
+-- week7/                    # AI Code Review
|   +-- backend/              # FastAPI app
|   +-- frontend/             # Static UI
|   +-- docs/TASKS.md
|
+-- week8/                    # Multi-Stack Build
|   +-- [3 tech stack versions]
|
+-- learning_notes/           # Learning notes treasure trove
|   +-- 00_learning_strategy.md    # BPRT learning cycle
|   +-- week1/                       # 8 files
|   +-- week2/                       # 10 files
|   |   +-- fundamentals/
|   |   +-- practice/
|   |   +-- reference/
|   +-- week3/                       # 3 files
|   +-- prompts/                     # 8 prompt templates
|
+-- .claude/                  # Claude Code configuration
|   +-- commands/             # Custom slash commands
|   +-- SUBAGENT_GUIDE.md
|
+-- .serena/                  # Serena MCP integration
|   +-- memories/             # Shared context across sessions
|   +-- config.json           # MCP server settings
|
+-- claude-best-practices/    # Best practices collection
|   +-- learning-prompts/     # Learning prompts guide
|   +-- project-patterns/     # Project patterns (5 guides)
|   +-- prompt-engineering/   # Prompt engineering guides
|
+-- CLAUDE.md                 # AI configuration (with team config)
+-- pyproject.toml            # Poetry 2.2.1 dependency management
+-- PROJECT_INDEX.md          # This file
+-- PROJECT_INDEX.json        # Machine-readable index
+-- README.md                 # Project overview
```

---

## 8-Week Learning Path

| Week | Theme | Core Skills | Main Tech | Key Files |
|------|-------|-------------|-----------|-----------|
| **1** | Prompt Engineering | K-shot, CoT, Tool Calling, RAG | Ollama, JSON Schema | [week1/*.py](week1/) |
| **2** | LLM-Powered Apps | FastAPI + LLM Integration | FastAPI, SQLAlchemy, Ollama | [week2/app/services/extract.py](week2/app/services/extract.py) |
| **3** | MCP Server | Model Context Protocol | MCP, Notion API | [week3/server/main.py](week3/server/main.py) |
| **4** | Claude Code | Automation Workflows | Slash Commands, SubAgents | [.claude/commands/*](.claude/commands/) |
| **5** | Warp Dev | Multi-AI Collaboration | Warp Drive, Multi-Agent | [week5/docs/TASKS.md](week5/docs/TASKS.md) |
| **6** | Security | SAST/SCA Analysis | Semgrep | [week6/backend/](week6/backend/) |
| **7** | AI Review | Code Review Comparison | Graphite Diamond | [week7/docs/TASKS.md](week7/docs/TASKS.md) |
| **8** | Multi-Stack | Full-Stack Development | Bolt.new + 3 stacks | [week8/](week8/) |

### Skills Pyramid

```
           AI System Design & Orchestration  (Week 3-8)
                    AI-Human Collaborative Dev     (Week 4-7)
                    Prompt Engineering Basics       (Week 1-2)
```

---

## Learning Notes Index

### Core Methodology

| File | Purpose | Importance |
|------|---------|------------|
| [00_learning_strategy.md](learning_notes/00_learning_strategy.md) | BPRT learning cycle + prompts |
| [ai_builder_context.md](learning_notes/ai_builder_context.md) | AI Builder cognitive framework |

### Week 1: Prompt Engineering

| File | Content |
|------|---------|
| 01_pre_learning_concepts.md | Concept preview |
| 02_ai_agent_interaction_guide.md | Agent interaction |
| 03_case_study_httpstatus_reversal.md | Case study |
| 04_quick_reference.md | Quick reference |
| 05_chain_of_thought_deep_dive.md | CoT deep dive |

### Week 2: LLM Integration (Most Complete)

| File | Content | Value |
|------|---------|-------|
| [WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/_archive/WEEK2_LEARNING_SUMMARY.md) | 875-line summary |
| [testing_llm_functions_guide.md](learning_notes/week2/fundamentals/03_testing_concepts.md) | LLM testing guide |
| [python_import_system_guide.md](learning_notes/week2/reference/imports_guide.md) | Import system |
| fundamentals/ | Architecture, LLM basics, testing |
| practice/ | Exception handling, LLM integration, refactoring |
| reference/ | Code patterns, command reference, troubleshooting |

### Week 3: MCP Server

| File | Content |
|------|---------|
| 01_pre_learning_concepts.md | MCP concepts |
| 从零开始构建MCP服务器.md | MCP build tutorial |

### Prompt Templates (prompts/)

| File | Purpose |
|------|---------|
| 01_pre_learning.md | Concept understanding (before) |
| 02_collaborative_coding.md | Assignment collaboration (during) |
| 03_critical_review.md | Critical review (after) |
| 04_note_generation.md | Note generation (summary) |
| 05_spaced_review.md | Spaced repetition (periodic) |
| 06_mini_project.md | Project-based learning (deep) |

---

## Tech Stack Overview

### Core Dependencies (pyproject.toml)

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

### Toolchain

| Tool | Purpose | Config File |
|------|---------|-------------|
| **Poetry 2.2.1** | Dependency management | [pyproject.toml](pyproject.toml) |
| **pytest** | Testing framework | `[tool.pytest.ini_options]` |
| **black** | Code formatter | `[tool.black]` |
| **ruff** | Code linter | `[tool.ruff]` |
| **pre-commit** | Git hooks | `.pre-commit-config.yaml` |

### AI Tools

| Tool | Purpose | Introduced |
|------|---------|------------|
| **Ollama** | Local LLM | Week 1 |
| **Claude Code** | AI coding assistant | Week 4 |
| **Warp** | AI terminal | Week 5 |
| **Semgrep** | Security scanning | Week 6 |
| **Graphite** | AI code review | Week 7 |
| **Bolt.new** | AI app generation | Week 8 |

---

## AI Engineer Skills Pyramid

### Level 1: Prompt Engineering (Week 1-2)
- K-shot prompting
- Chain-of-Thought
- Tool Calling
- RAG
- Reflexion
- Structured Output (JSON Schema)

### Level 2: AI-Human Collaboration (Week 3-7)
- MCP Server Development
- Claude Code Automation
- Multi-Agent Workflows
- Security Analysis
- AI Code Review

### Level 3: AI System Design (Week 8)
- Multi-Stack Development
- AI Full-Stack
- Bolt.new App Generation

---

## Quick Start

### Environment Setup

```bash
# 1. Create Conda environment
conda create -n cs146s python=3.12 -y
conda activate cs146s

# 2. Install Poetry (if needed)
curl -sSL https://install.python-poetry.org | python -

# 3. Install dependencies
poetry install

# 4. Start Ollama (Week 1-2)
ollama serve && ollama pull llama3.1:8b
```

### Running Tests

```bash
# Fast tests (skip LLM integration)
pytest week2/tests/ -m "not slow"

# Full tests (including LLM)
pytest week2/tests/

# Coverage report
pytest week2/tests/ --cov=week2/app --cov-report=html
```

### Starting Applications

```bash
# Week 2-7: FastAPI apps
cd week2  # or week4, week5, week6, week7
make run  # or python -m uvicorn app.main:app --reload

# Access
# Frontend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Claude Code Commands

```bash
/week              # Get weekly assignment help
/explore-week      # Deep dive into week state
/test-week         # Run and analyze tests
/mcp-server        # MCP server help
/refactor          # Systematic code cleanup
```

---

## Key Learning Resources

### Internal Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Learning Strategy | [learning_notes/00_learning_strategy.md](learning_notes/00_learning_strategy.md) | BPRT cycle |
| Week 2 Example | [learning_notes/week2/_archive/WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/_archive/WEEK2_LEARNING_SUMMARY.md) | Note template |
| AI Config | [CLAUDE.md](CLAUDE.md) | AI team config |
| Serena Config | [.serena/](.serena/) | MCP integration |

### External Resources

| Resource | Link | Purpose |
|----------|------|---------|
| Course | [themodernsoftware.dev](https://themodernsoftware.dev) | Course home |
| Claude Code | [docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code) | Claude Code guide |
| MCP Protocol | [modelcontextprotocol.io](https://modelcontextprotocol.io) | MCP spec |
| FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) | FastAPI docs |

---

## Project Statistics

| Metric | Count |
|--------|-------|
| **Week folders** | 8 |
| **Python files** | ~90 |
| **Markdown docs** | ~70 |
| **Test files** | ~20 |
| **Learning notes** | ~25 |
| **Custom commands** | 7 |
| **Claude best practices** | 12 |
| **Serena memories** | 10 |

---

## Usage Tips

### For AI Agents

1. **Read this index first** - Understand structure before coding
2. **Use `/week` command** - Get week-specific context
3. **Use `code-reviewer`** - Before any commits
4. **Use `/test-week`** - Run tests before finishing

### For Learners

1. **Follow BPRT cycle** - Build → Prompt → Reflect → Teach
2. **Reference Week 2 notes** - Best example of learning notes
3. **Use prompt templates** - In [learning_notes/prompts/](learning_notes/prompts/)
4. **Generate summaries** - After each week

---

## Next Steps

### For Beginners

1. Read [00_learning_strategy.md](learning_notes/00_learning_strategy.md)
2. Study [WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/_archive/WEEK2_LEARNING_SUMMARY.md) as example
3. Complete environment setup (see Quick Start)
4. Use `/week` command for current week

### For Advanced Users

1. Explore [.claude/commands/](.claude/commands/) custom commands
2. Read [SUBAGENT_GUIDE.md](.claude/SUBAGENT_GUIDE.md) for subagents
3. Use prompt templates for deep learning
4. Review periodically (every 2-3 weeks with Prompt 5)

---

**Index Version:** 1.1
**Last Updated:** 2025-12-30
**Maintained by:** AI Agent (Claude Code)
