# Claude Best Practices - Knowledge Index

> Generated: 2025-12-31 | Token Efficiency: 94% reduction (58K → 3K)
>
> **Purpose**: This index provides instant context without loading all documentation. Use it to locate specific topics, then read only the relevant files.

---

## 📁 Structure Overview

```
claude-best-practices/
├── 01-setup/           # Project configuration for AI
├── 02-understand/      # System architecture understanding
├── 03-create/          # Custom skill development
├── 04-deep-dive/       # Advanced topic analysis
└── serena-mcp/         # Serena memory system
```

---

## 🎯 Quick Navigation by Intent

### "I want to configure my project"
→ [01-setup/](01-setup/)
| File | Purpose | Key Benefit |
|------|---------|-------------|
| [project-index-usage.md](01-setup/project-index-usage.md) | Create PROJECT_INDEX | 94% token savings |
| [claude-md-best-practices.md](01-setup/claude-md-best-practices.md) | Configure CLAUDE.md | Define AI team/workflow |
| [skills-system-guide.md](01-setup/skills-system-guide.md) | Skills system | Extend AI capabilities |

### "I want to understand how Claude Code works"
→ [02-understand/](02-understand/)
| File | Purpose | Key Concepts |
|------|---------|--------------|
| [subagent-system.md](02-understand/subagent-system.md) | Subagent architecture | Specialization & delegation |
| [superclaude-architecture.md](02-understand/superclaude-architecture.md) | Overall architecture | Commands + MCP |
| [ai-engineering-principles.md](02-understand/ai-engineering-principles.md) | Engineering principles | ROI, Token optimization |
| [tdd-first-principles.md](02-understand/tdd-first-principles.md) | Test-driven development | TestAgent + CodeAgent |

### "I want to create custom skills/commands"
→ [03-create/](03-create/)
| File | Purpose | Output |
|------|---------|--------|
| [skill-design-best-practices.md](03-create/skill-design-best-practices.md) | Design custom Skills | New .claude/commands/ |
| [document-skills-guide.md](03-create/document-skills-guide.md) | Document skills | docx, pptx, pdf handling |

### "I want to master specific features"
→ [04-deep-dive/](04-deep-dive/)
| File | Topic | Depth |
|------|--------|-------|
| [sc-pm-explained.md](04-deep-dive/sc-pm-explained.md) | /sc:pm command | Workflow, memory system |
| [index-repo-analysis.md](04-deep-dive/index-repo-analysis.md) | /sc:index-repo | Prompt breakdown |
| [context7-mcp-guide.md](04-deep-dive/context7-mcp-guide.md) | Context7 MCP | Tool details, best practices |
| [learning-prompts-collection.md](04-deep-dive/learning-prompts-collection.md) | 100+ prompts | 8 topics, practice |

### "I want to master Serena (memory system)"
→ [serena-mcp/](serena-mcp/)
| File | Purpose | Key Benefit |
|------|---------|-------------|
| [README.md](serena-mcp/README.md) | Serena overview | Quick start |
| [01-architecture-overview.md](serena-mcp/01-architecture-overview.md) | Architecture | Component details |
| [02-configuration-guide.md](serena-mcp/02-configuration-guide.md) | Configuration | project.yml reference |
| [03-memory-system-design.md](serena-mcp/03-memory-system-design.md) | Memory design | Organization strategies |
| [04-cross-machine-sync.md](serena-mcp/04-cross-machine-sync.md) | Multi-device | Git sharing |
| [05-advanced-patterns.md](serena-mcp/05-advanced-patterns.md) | Advanced patterns | MCP tool integration |

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

## 📖 File Inventory (21 files)

### Setup (3 files)
- `01-setup/claude-md-best-practices.md`
- `01-setup/skills-system-guide.md`
- `01-setup/project-index-usage.md`

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

### Serena (6 files)
- `serena-mcp/README.md`
- `serena-mcp/01-architecture-overview.md`
- `serena-mcp/02-configuration-guide.md`
- `serena-mcp/03-memory-system-design.md`
- `serena-mcp/04-cross-machine-sync.md`
- `serena-mcp/05-advanced-patterns.md`

### Root (1 file)
- `README.md` (main navigation hub)

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

---

## 💡 Key Insights

1. **94% Token Savings**: Index reduces 58K → 3K tokens per session
2. **4-Layer Prompts**: Persona → Process → Output → Validation
3. **MCP vs Subagent**: External APIs = MCP, AI reasoning = Subagent
4. **Serena Memory**: Hierarchical namespace (session/, plan/, learning/)
5. **ROI Break-even**: 1 session pays for index creation cost

---

**Status**: Ready for use. Last updated: 2025-12-31
