# CS146S: Modern Software Developer - Project Index

> Generated: 2025-12-30
> Last Updated: 2026-01-08 (v1.4)
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
|   +-- week1_assignment.md   # Assignment spec (renamed for clarity)
|   +-- k_shot_prompting.py
|   +-- chain_of_thought.py
|   +-- tool_calling.py
|   +-- rag.py
|   +-- reflexion.py
|   +-- self_consistency_prompting.py
|
+-- week2/                    # FastAPI + LLM 集成
|   +-- week2_assignment.md   # Assignment spec (renamed)
|   +-- week2_writeup.md      # Week summary (renamed)
|   +-- app/
|   |   +-- routers/          # API endpoints (action_items.py, notes.py)
|   |   +-- services/         # Business logic (extract.py)
|   |   +-- db.py             # Database layer
|   |   +-- schemas.py        # Pydantic models
|   |   +-- main.py           # FastAPI app entry
|   +-- tests/                # 6 test files (~85% coverage)
|
+-- week3/                    # MCP Server
|   +-- week3_assignment.md   # Assignment spec (renamed)
|   +-- server/main.py        # Notion MCP server (450 lines)
|   +-- weather_server/
|       +-- weather.py        # Weather MCP server (FastMCP)
|       +-- test_server.py
|
+-- week4/                    # Claude Code Automation
|   +-- week4_assignment.md   # Assignment spec (renamed)
|   +-- week4_writeup.md      # Week summary (renamed)
|   +-- backend/              # FastAPI app (refactored)
|   +-- frontend/             # Static UI
|   +-- data/                 # SQLite + seed
|   +-- docs/TASKS.md
|
+-- week5/                    # Warp Agentic Development
|   +-- week5_assignment.md   # Assignment spec (renamed)
|   +-- week5_writeup.md      # Week summary (renamed)
|   +-- backend/              # FastAPI app
|   +-- frontend/             # Static UI
|   +-- docs/TASKS.md
|
+-- week6/                    # Security Analysis
|   +-- week6_assignment.md   # Assignment spec (renamed)
|   +-- week6_writeup.md      # Week summary (renamed)
|   +-- backend/              # FastAPI app
|   +-- frontend/             # Static UI
|
+-- week7/                    # AI Code Review
|   +-- week7_assignment.md   # Assignment spec (renamed)
|   +-- week7_writeup.md      # Week summary (renamed)
|   +-- backend/              # FastAPI app
|   +-- frontend/             # Static UI
|   +-- docs/TASKS.md
|
+-- week8/                    # Multi-Stack Build
|   +-- week8_assignment.md   # Assignment spec (renamed)
|   +-- week8_writeup.md      # Week summary (renamed)
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
+-- claude-best-practices/    # Best practices collection (20+ guides)
|   +-- README.md                  # Navigation hub (updated)
|   +-- 01-setup/                  # Setup guides (3 files)
|   |   +-- project-index-usage.md
|   |   +-- claude-md-best-practices.md
|   |   +-- skills-system-guide.md
|   +-- 02-understand/             # Architecture guides (3 files)
|   |   +-- subagent-system.md
|   |   +-- superclaude-architecture.md
|   |   +-- ai-engineering-principles.md
|   +-- 03-create/                 # Creation guides (2 files)
|   |   +-- skill-design-best-practices.md
|   |   +-- document-skills-guide.md
|   +-- 04-deep-dive/              # Deep dive guides (5 files)
|   |   +-- sc-pm-explained.md
|   |   +-- index-repo-analysis.md
|   |   +-- context7-mcp-guide.md
|   |   +-- prompt-layer-design.md
|   |   +-- learning-prompts-collection.md
|   +-- 05-learning_mode_design/   # Learning mode design docs
|   +-- serena-mcp/                # Serena MCP guides (6 files)
|       +-- README.md
|       +-- 01-architecture-overview.md
|       +-- 02-configuration-guide.md
|       +-- 03-memory-system-design.md
|       +-- 04-cross-machine-sync.md
|       +-- 05-advanced-patterns.md
|
+-- .claude/                  # Claude Code configuration
|   +-- commands/             # Custom slash commands (10 files)
|   |   +-- week.md           # /week - Weekly assignment help
|   |   +-- explore-week.md   # /explore-week - Week analysis
|   |   +-- test-week.md      # /test-week - Run tests
|   |   +-- llm-extract.md    # /llm-extract - Week 2 helper
|   |   +-- mcp-server.md     # /mcp-server - Week 3 helper
|   |   +-- refactor.md       # /refactor - Code cleanup
|   |   +-- review-pr.md      # /review-pr - PR review
|   |   +-- tdd-cycle.md      # /tdd-cycle - TDD workflow
|   +-- subagents/            # TDD subagents (2 files)
|   +-- settings.local.json   # Local settings
|   +-- SUBAGENT_GUIDE.md
|
+-- .serena/                  # Serena MCP integration
|   +-- project.yml           # Serena project config
|   +-- memories/             # Shared context (12 files)
|       +-- weekly_assignments.md
|       +-- architecture_decisions.md
|       +-- tech_stack.md
|       +-- llm_integration_patterns.md
|
+-- learning_progress/        # Learning progress tracking
|   +-- index.md
|   +-- multi_agent_design_patterns_2025-01-01.md
|
+-- CLAUDE.md                 # AI configuration (with team config)
+-- META_LEARNING.md          # Learning framework & capability levels
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
| **3** | MCP Server | Model Context Protocol | MCP, Notion/NWS API | [week3/server/main.py](week3/server/main.py) (Notion), [week3/weather_server/weather.py](week3/weather_server/weather.py) (Weather) |
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

## File Naming Convention (Updated 2025-12-30)

**Before**: Generic names caused confusion
- `assignment.md` → ambiguous which week
- `writeup.md` → unclear association

**After**: Week-prefixed for clarity
- `week1_assignment.md` - Clear week association
- `week2_writeup.md` - Easy identification
- `week3_assignment.md` - Targeted file discovery

**Benefits for AI Agents**:
- ✅ Precise file search: `week4_assignment.md` vs `assignment.md`
- ✅ Reduced noise when exploring specific weeks
- ✅ Better context isolation for learning
- ✅ Faster file discovery in large codebases

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

## Claude Best Practices Collection

**Location**: [claude-best-practices/](claude-best-practices/)
**Updated**: 2026-01-08
**Purpose**: Comprehensive guide for Claude Code and SuperClaude mastery

### Navigation Structure

```
claude-best-practices/
├── README.md                      # 🎯 Navigation hub (start here!)
│
├── 01-setup/                      # 【我要配置项目】
│   ├── project-index-usage.md     # 94% token savings
│   ├── claude-md-best-practices.md # AI behavior config
│   └── skills-system-guide.md     # Extend AI capabilities
│
├── 02-understand/                 # 【我要理解系统】
│   ├── subagent-system.md         # Subagent delegation
│   ├── superclaude-architecture.md # Overall architecture
│   └── ai-engineering-principles.md # ROI, token optimization
│
├── 03-create/                     # 【我要创建/开发】
│   ├── skill-design-best-practices.md # Create custom skills
│   └── document-skills-guide.md   # Use document skills
│
├── 04-deep-dive/                  # 【我要深入学习】
│   ├── sc-pm-explained.md         # /sc:pm analysis
│   ├── index-repo-analysis.md     # /sc:index-repo deep dive
│   ├── context7-mcp-guide.md      # Context7 integration
│   ├── prompt-layer-design.md     # Prompt layer design
│   └── learning-prompts-collection.md # 100+ prompts
│
├── 05-learning_mode_design/       # 【Learning Mode Design】
│   ├── commands-vs-skills.md      # Commands vs Skills comparison
│   └── [more design docs...]
│
└── serena-mcp/                    # 【Serena MCP 系统】
    ├── README.md                  # Serena overview
    ├── 01-architecture-overview.md
    ├── 02-configuration-guide.md
    ├── 03-memory-system-design.md
    ├── 04-cross-machine-sync.md
    └── 05-advanced-patterns.md
```

### Key Concepts Covered

| Topic | Files | Focus |
|-------|-------|-------|
| **Setup** | 3 files | Configuration, indexing, skills |
| **Architecture** | 3 files | Subagents, system design, principles |
| **Creation** | 2 files | Skill design, document processing |
| **Deep Dive** | 5 files | Command internals, MCP integration |
| **Learning Mode** | 1+ files | Learning mode design patterns |
| **Serena** | 6 files | Memory system, cross-machine sync |

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
pytest-cov = "^7.0.0"          # Coverage reporting
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
/tdd-cycle         # Test-Driven Development workflow
```

---

## Key Learning Resources

### Internal Resources

| Resource | Path | Purpose |
|----------|------|---------|
| Learning Strategy | [learning_notes/00_learning_strategy.md](learning_notes/00_learning_strategy.md) | BPRT cycle |
| META_LEARNING | [META_LEARNING.md](META_LEARNING.md) | Capability levels framework |
| Week 2 Example | [learning_notes/week2/_archive/WEEK2_LEARNING_SUMMARY.md](learning_notes/week2/_archive/WEEK2_LEARNING_SUMMARY.md) | Note template |
| AI Config | [CLAUDE.md](CLAUDE.md) | AI team config |
| Serena Config | [.serena/](.serena/) | MCP integration |
| Claude Best Practices | [claude-best-practices/README.md](claude-best-practices/README.md) | System guides |

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
| **Python files** | 89 |
| **Markdown docs** | 132 |
| **Test files** | ~20 |
| **Learning notes** | ~30 |
| **Custom commands** | 10 |
| **Claude best practices** | 25+ |
| **Serena memories** | 12 |
| **MCP servers** | 2 (Notion, Weather) |
| **Largest week** | week5 (159M) |
| **Latest commit** | 2026-01-08 |

---

## Usage Tips

### For AI Agents

1. **Read this index first** - Understand structure before coding
2. **Use week-specific files** - `week4_assignment.md` is more precise than `assignment.md`
3. **Use `/week` command** - Get week-specific context
4. **Use `code-reviewer`** - Before any commits
5. **Use `/test-week`** - Run tests before finishing

### For Learners

1. **Follow BPRT cycle** - Build → Prompt → Reflect → Teach
2. **Reference Week 2 notes** - Best example of learning notes
3. **Use prompt templates** - In [learning_notes/prompts/](learning_notes/prompts/)
4. **Explore Claude best practices** - In [claude-best-practices/README.md](claude-best-practices/README.md)
5. **Generate summaries** - After each week

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
3. Use [claude-best-practices/](claude-best-practices/) for deep learning
4. Review periodically (every 2-3 weeks with Prompt 5)

---

**Index Version:** 1.4
**Last Updated:** 2026-01-08
**Changes**: Added META_LEARNING.md reference, updated learning_mode_design section, added latest commit info, updated statistics
**Maintained by:** AI Agent (Claude Code)
