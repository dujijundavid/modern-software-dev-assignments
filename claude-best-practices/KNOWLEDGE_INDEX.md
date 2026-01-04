# Claude Best Practices - Knowledge Index

> Generated: 2026-01-05 | Token Efficiency: ~94% reduction (≈60K → ≈3.6K)
>
> **Purpose**: This index provides instant context without loading all documentation. Use it to locate specific topics, then read only the relevant files.
>
> 更新提示（人工维护）：
> - 手动更新时间：2026-01-05
> - 文件计数：28（`find claude-best-practices -type f ! -name '.DS_Store' | wc -l`）
> - 节省率假设：全文约 6 万 tokens，索引约 3.6 千 tokens，约 94% 减少

---

## 📁 Structure Overview

```
claude-best-practices/
├── 01-setup/           # Project configuration for AI
├── 02-understand/      # System architecture understanding
├── 03-create/          # Custom skill development
├── 04-deep-dive/       # Advanced topic analysis
├── 05-learning_mode_design/  # Learning patterns
├── 06-analysis-tools/  # Analysis & strategic thinking
└── serena-mcp/         # Serena memory system
```

---

## 🎯 Quick Navigation by Intent

### "I want to configure my project"
→ [01-setup/](01-setup/)
| File | Use Case + Output |
|------|-------------------|
| [project-index-usage.md](01-setup/project-index-usage.md) | First/iterative index build; playbook to get ~94% token savings |
| [claude-md-best-practices.md](01-setup/claude-md-best-practices.md) | Team-aligned CLAUDE.md with roles, process, and validation checklist |
| [claude-code-architecture.md](01-setup/claude-code-architecture.md) | Quick map of Skills/Commands/Subagents/Super Claude boundaries and call chain |
| [skills-system-guide.md](01-setup/skills-system-guide.md) | How to install/extend/share skills, directory layout, and trigger behavior |

### "I want to understand how Claude Code works"
→ [02-understand/](02-understand/)
| File | Use Case + Output |
|------|-------------------|
| [subagent-system.md](02-understand/subagent-system.md) | When designing/choosing subagents; specialization, delegation, parallelism |
| [superclaude-architecture.md](02-understand/superclaude-architecture.md) | Deep dive on routing/orchestration layer; command system and subagent dispatch |
| [ai-engineering-principles.md](02-understand/ai-engineering-principles.md) | ROI and token optimization framing with worked math examples |
| [tdd-first-principles.md](02-understand/tdd-first-principles.md) | Why split TestAgent/CodeAgent; handoff format and TDD enforcement rationale |

### "I want to create custom skills/commands"
→ [03-create/](03-create/)
| File | Use Case + Output |
|------|-------------------|
| [skill-design-best-practices.md](03-create/skill-design-best-practices.md) | Naming, structure, validation checklist; ready-to-publish skill skeleton |
| [document-skills-guide.md](03-create/document-skills-guide.md) | How to call docx/pptx/pdf/xlsx skills; limits and best practices |

### "I want to master specific features"
→ [04-deep-dive/](04-deep-dive/)
| File | Use Case + Output |
|------|-------------------|
| [sc-pm-explained.md](04-deep-dive/sc-pm-explained.md) | Full /sc:pm workflow, memory use, quality gates |
| [index-repo-analysis.md](04-deep-dive/index-repo-analysis.md) | Prompt breakdown and token strategy for /sc:index-repo |
| [context7-mcp-guide.md](04-deep-dive/context7-mcp-guide.md) | How to fetch latest library docs via Context7 MCP; pitfalls and patterns |
| [learning-prompts-collection.md](04-deep-dive/learning-prompts-collection.md) | 100+ practice prompts across 8 themes for drilling skills |
| [prompt-layer-design.md](04-deep-dive/prompt-layer-design.md) | Persona/Process/Output/Validation 4-layer prompt template with examples |

### "I want to design learning modes"
→ [05-learning_mode_design/](05-learning_mode_design/)
| File | Use Case + Output |
|------|-------------------|
| [commands-vs-skills.md](05-learning_mode_design/commands-vs-skills.md) | Decision guide: when to use commands vs skills; naming, sharing, trigger differences |

### "I want to analyze business/strategy documents"
→ [06-analysis-tools/](06-analysis-tools/)
| File | Command/Topic | Use Case + Output |
|------|---------------|-------------------|
| [README.md](06-analysis-tools/README.md) | Overview | Map available analysis tools and entry points |
| [sc-brainstorm-guide.md](06-analysis-tools/sc-brainstorm-guide.md) | `/sc:brainstorm` | Interactive requirements discovery script and templates |
| [business-panel-guide.md](06-analysis-tools/business-panel-guide.md) | `/sc:business-panel` | Multi-expert business analysis structure and validation checklist |

### "I want to master Serena (memory system)"
→ [serena-mcp/](serena-mcp/)
| File | Use Case + Output |
|------|-------------------|
| [README.md](serena-mcp/README.md) | 10-minute Serena overview and quick start |
| [01-architecture-overview.md](serena-mcp/01-architecture-overview.md) | Component map and boundaries when evaluating Serena |
| [02-configuration-guide.md](serena-mcp/02-configuration-guide.md) | project.yml reference for configuring/launching the server |
| [03-memory-system-design.md](serena-mcp/03-memory-system-design.md) | Memory namespace design templates and persistence strategy |
| [04-cross-machine-sync.md](serena-mcp/04-cross-machine-sync.md) | Git sync and ignore strategy for multi-device collaboration |
| [05-advanced-patterns.md](serena-mcp/05-advanced-patterns.md) | Advanced MCP integration patterns and examples |

### Other root docs
| File | Use Case + Output |
|------|-------------------|
| [README.md](README.md) | Main navigation hub for all topics |
| [KNOWLEDGE_INDEX.md](KNOWLEDGE_INDEX.md) | This index; fast lookup without loading all docs |
| [NOTION_MCP_ERRORS.md](NOTION_MCP_ERRORS.md) | Known Notion MCP error cases and fixes |

---

## 🧠 Core Concepts Summary

### Prompt Engineering 4-Layer Model

| Layer | Content | Validation |
|-------|---------|------------|
| **Layer 1: Persona** | "You are a [role]..." | Does AI behave as expected? |
| **Layer 2: Process** | Phase 1 → 2 → 3 | Does AI follow steps? |
| **Layer 3: Output** | `{field}` templates | Does output match format? |
| **Layer 4: Validation** | `[ ]` checklist | Does AI check quality? |

**Source**: [04-deep-dive/prompt-layer-design.md](04-deep-dive/prompt-layer-design.md)

---

### Token Efficiency Strategies

| Strategy | Effect | Use Case |
|----------|--------|----------|
| **Create index** | 94% savings | Large projects |
| **Modular indexing** | On-demand loading | Modular projects |
| **Incremental updates** | Reduce rebuilds | Frequent changes |
| **Compress redundancy** | Reduce noise | Document-heavy |

**ROI Math**:
```
Sessions to break even = Creation_cost / (Full_tokens - Index_tokens)
Example: 2000 / (58000 - 3000) = 0.036 → 1 session!
```

**Source**: [02-understand/ai-engineering-principles.md](02-understand/ai-engineering-principles.md)

---

### Claude Code Three Cores

| Core | Purpose | Key File |
|------|---------|----------|
| **Configuration** | Behavior guide | CLAUDE.md |
| **Index** | Structure guide | PROJECT_INDEX.json |
| **Commands** | Interaction interface | .claude/commands/ |

---

### Serena Four Components

| Component | Purpose | Key File |
|-----------|---------|----------|
| **Configuration** | Project-level config | .serena/project.yml |
| **Memory** | Persistent knowledge | .serena/memories/ |
| **MCP Tools** | Read/write interface | MCP server tools |
| **Git Sync** | Cross-device collaboration | .serena/.gitignore |

---

## 🔧 Quick Reference

### MCP vs Subagent Decision Tree

```
Need external API/service?
  ├─ Yes → MCP Server Skill (Python + FastMCP)
  └─ No → Need AI reasoning?
             ├─ Yes → Subagent Skill (YAML + Prompt)
             └─ No → Direct function/script
```

**Source**: [03-create/skill-design-best-practices.md](03-create/skill-design-best-practices.md)

---

### Naming Conventions

| Type | Pattern | Examples |
|------|---------|----------|
| MCP Server | `{name}` | `weather`, `notion-integration` |
| MCP Tool | `{verb}_{noun}` | `get_alerts`, `create_page` |
| Subagent | `{role}-{expert}` | `fastapi-expert`, `code-reviewer` |
| Slash Command | `/sc:{action}` | `/sc:implement`, `/sc:test` |

---

### Memory Schema (Serena)

```
session/         # Session state
  ├── context      # Complete snapshot
  ├── last         # Previous session
  └── checkpoint   # Progress snapshots

plan/            # Planning artifacts
  ├── [feature]/hypothesis
  ├── [feature]/architecture
  └── [feature]/rationale

learning/        # Knowledge capture
  ├── patterns/[name]
  ├── solutions/[error]
  └── mistakes/[timestamp]
```

**Source**: [serena-mcp/03-memory-system-design.md](serena-mcp/03-memory-system-design.md)

---

## 📚 Learning Path (15 Days)

### Day 1-3: Setup
1. [project-index-usage.md](01-setup/project-index-usage.md) - 94% token savings
2. [claude-md-best-practices.md](01-setup/claude-md-best-practices.md) - Define AI behavior
3. [skills-system-guide.md](01-setup/skills-system-guide.md) - Extend AI capabilities

### Day 4-7: Understanding
1. [subagent-system.md](02-understand/subagent-system.md) - Specialization
2. [superclaude-architecture.md](02-understand/superclaude-architecture.md) - Architecture
3. [ai-engineering-principles.md](02-understand/ai-engineering-principles.md) - ROI & optimization

### Day 8-10: Creation
1. [skill-design-best-practices.md](03-create/skill-design-best-practices.md) - Custom skills
2. [document-skills-guide.md](03-create/document-skills-guide.md) - Document handling

### Day 11-14: Serena
1. [01-architecture-overview.md](serena-mcp/01-architecture-overview.md) - System architecture
2. [02-configuration-guide.md](serena-mcp/02-configuration-guide.md) - Configuration
3. [03-memory-system-design.md](serena-mcp/03-memory-system-design.md) - Memory organization

### Day 15+: Deep Dive
1. [sc-pm-explained.md](04-deep-dive/sc-pm-explained.md) - PM agent
2. [index-repo-analysis.md](04-deep-dive/index-repo-analysis.md) - Prompt engineering
3. [05-advanced-patterns.md](serena-mcp/05-advanced-patterns.md) - Advanced patterns
4. [learning-prompts-collection.md](04-deep-dive/learning-prompts-collection.md) - 100+ prompts
5. [sc-brainstorm-guide.md](06-analysis-tools/sc-brainstorm-guide.md) - Requirements discovery
6. [business-panel-guide.md](06-analysis-tools/business-panel-guide.md) - Business analysis

---

## 🎯 Quick Checklist

### Before Writing a Prompt
- [ ] Goal: Does AI know "what success looks like"?
- [ ] Steps: Complex tasks broken into phases?
- [ ] Output: Expected format defined?
- [ ] Validation: How to check quality?
- [ ] ROI: Is value quantified?

### Before Configuring Serena
- [ ] project.yml configured correctly?
- [ ] .serena/.gitignore excludes only /cache?
- [ ] memories/ has organized structure?
- [ ] Git tracks configuration files?

### Before Creating a Skill
- [ ] MCP vs Subagent decision made?
- [ ] Name follows conventions?
- [ ] Description includes 3 elements?
- [ ] Has validation checklist?

---

## 📖 File Inventory (28 files, excluding .DS_Store)

### Setup (4 files)
- `01-setup/project-index-usage.md`
- `01-setup/claude-md-best-practices.md`
- `01-setup/claude-code-architecture.md`
- `01-setup/skills-system-guide.md`

### Understanding (4 files)
- `02-understand/subagent-system.md`
- `02-understand/superclaude-architecture.md`
- `02-understand/ai-engineering-principles.md`
- `02-understand/tdd-first-principles.md`

### Creation (2 files)
- `03-create/skill-design-best-practices.md`
- `03-create/document-skills-guide.md`

### Deep Dive (5 files)
- `04-deep-dive/prompt-layer-design.md`
- `04-deep-dive/index-repo-analysis.md`
- `04-deep-dive/context7-mcp-guide.md`
- `04-deep-dive/sc-pm-explained.md`
- `04-deep-dive/learning-prompts-collection.md`

### Learning Mode Design (1 file)
- `05-learning_mode_design/commands-vs-skills.md`

### Analysis Tools (3 files)
- `06-analysis-tools/sc-brainstorm-guide.md`
- `06-analysis-tools/business-panel-guide.md`
- `06-analysis-tools/README.md`

### Serena (6 files)
- `serena-mcp/README.md`
- `serena-mcp/01-architecture-overview.md`
- `serena-mcp/02-configuration-guide.md`
- `serena-mcp/03-memory-system-design.md`
- `serena-mcp/04-cross-machine-sync.md`
- `serena-mcp/05-advanced-patterns.md`

### Root (3 files)
- `README.md` (main navigation hub)
- `KNOWLEDGE_INDEX.md` (this index)
- `NOTION_MCP_ERRORS.md` (Notion MCP known issues)

---

## 🔍 Search by Topic

| Topic | Primary Files |
|-------|---------------|
| **Prompt Design** | [04-deep-dive/prompt-layer-design.md](04-deep-dive/prompt-layer-design.md), [02-understand/ai-engineering-principles.md](02-understand/ai-engineering-principles.md) |
| **Token Optimization** | [01-setup/project-index-usage.md](01-setup/project-index-usage.md), [04-deep-dive/index-repo-analysis.md](04-deep-dive/index-repo-analysis.md) |
| **MCP Development** | [03-create/skill-design-best-practices.md](03-create/skill-design-best-practices.md), [04-deep-dive/context7-mcp-guide.md](04-deep-dive/context7-mcp-guide.md) |
| **Memory Systems** | [serena-mcp/README.md](serena-mcp/README.md), [serena-mcp/03-memory-system-design.md](serena-mcp/03-memory-system-design.md) |
| **AI Agents** | [02-understand/subagent-system.md](02-understand/subagent-system.md), [04-deep-dive/sc-pm-explained.md](04-deep-dive/sc-pm-explained.md) |
| **Test-Driven Development** | [02-understand/tdd-first-principles.md](02-understand/tdd-first-principles.md) |
| **Custom Commands** | [01-setup/skills-system-guide.md](01-setup/skills-system-guide.md), [03-create/skill-design-best-practices.md](03-create/skill-design-best-practices.md) |
| **Requirements Discovery** | [06-analysis-tools/sc-brainstorm-guide.md](06-analysis-tools/sc-brainstorm-guide.md) |
| **Business Analysis** | [06-analysis-tools/business-panel-guide.md](06-analysis-tools/business-panel-guide.md) |
| **Command vs Skill Decision** | [05-learning_mode_design/commands-vs-skills.md](05-learning_mode_design/commands-vs-skills.md) |
| **Architecture Overview** | [01-setup/claude-code-architecture.md](01-setup/claude-code-architecture.md), [02-understand/superclaude-architecture.md](02-understand/superclaude-architecture.md) |

---

## 💡 Key Insights

1. **~94% Token Savings**: Index reduces ≈60K → ≈3.6K tokens/会话（估算）
2. **4-Layer Prompts**: Persona → Process → Output → Validation
3. **MCP vs Subagent**: External APIs = MCP, AI reasoning = Subagent
4. **Serena Memory**: Hierarchical namespace (session/, plan/, learning/)
5. **ROI Break-even**: 1 session pays for index creation cost

---

**Status**: Ready for use. Last updated: 2026-01-05
**Total Files**: 28 (excluding .DS_Store)
