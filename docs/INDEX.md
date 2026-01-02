# CS146S Documentation Index

Comprehensive documentation for CS146S Modern Software Developer course. Organized by **theme**, not by week - for practical reference and continuous learning.

---

## Quick Navigation

### Core Documentation (8 Theme Files)

| # | Theme | Focus | Lines |
|---|-------|-------|-------|
| [01](01_prompt_engineering.md) | Prompt Engineering | K-shot, CoT, tool calling, 4-Layer Model | 716 |
| [02](02_llm_integration.md) | LLM Integration | Structured output, architecture, error handling | 712 |
| [03](03_mcp_protocol.md) | MCP Protocol | FastMCP, async, tools, resources, prompts | 759 |
| [04](04_multi_agent_systems.md) | Multi-Agent Systems | SubAgents, handoff, TDD with agents | 1005 |
| [05](05_testing_strategies.md) | Testing Strategies | Pyramid, LLM testing, MCP testing | 890 |
| [06](06_automation_design.md) | Automation Design | Hierarchy, principles, real examples | 925 |
| [07](07_learning_journey.md) | Learning Journey | Skills, mistakes, growth over 4 months | 479 |
| [08](08_quick_reference.md) | Quick Reference | Commands, patterns, cheat sheets | 270 |

---

## By Theme

### 🎯 Prompt Engineering
**[01_prompt_engineering.md](01_prompt_engineering.md)**

Core techniques for effective LLM prompting:
- K-shot prompting with real examples
- Chain-of-thought reasoning
- Tool calling patterns
- 4-Layer Prompt Model (Role, Task, Format, Constraints)
- Universal principles (Recency Bias, Semantic Isolation)
- HTTPStatus reversal case study (5 iterations)

**Best for**: Learning how to craft effective prompts

---

### 🔌 LLM Integration
**[02_llm_integration.md](02_llm_integration.md)**

Production patterns for LLM-powered applications:
- Structured output with Pydantic
- Layered architecture (Router/Service/Database)
- Error handling strategies
- Post-processing pipelines
- Real example: Action item extractor

**Best for**: Building production LLM applications

---

### 🌐 MCP Protocol
**[03_mcp_protocol.md](03_mcp_protocol.md)**

Model Context Protocol for AI integrations:
- MCP architecture (Tools, Resources, Prompts)
- FastMCP framework guide
- Async/await patterns
- Complete weather server example (91 lines)
- Testing and deployment
- Best practices & common pitfalls

**Best for**: Building MCP servers

---

### 🤖 Multi-Agent Systems
**[04_multi_agent_systems.md](04_multi_agent_systems.md)**

Coordinating multiple AI agents:
- SubAgent patterns (sequential, parallel, pool)
- Handoff protocols
- TDD with TestAgent + CodeAgent
- Real examples: TDD Cycle, Architect Hub
- Design flaws & improvements
- Scaling strategies

**Best for**: Designing multi-agent workflows

---

### 🧪 Testing Strategies
**[05_testing_strategies.md](05_testing_strategies.md)**

Testing pyramid for LLM applications:
- 70/20/10 distribution (Unit/Integration/E2E)
- LLM testing (mocks, semantic assertions)
- MCP testing (async sessions, tool validation)
- Test patterns (parametrized, fixtures, mocks)
- Real benchmark: 60x speedup with mocks

**Best for**: Writing fast, reliable tests

---

### ⚡ Automation Design
**[06_automation_design.md](06_automation_design.md)**

Design principles for automation:
- Automation hierarchy (Levels 1-4)
- The Three Questions (bottleneck, leverage, compounding)
- Real examples: TDD Cycle, Architect Hub
- Design principles & anti-patterns
- Evaluation rubric (12+/20 target)

**Best for**: Building scalable automations

---

### 📈 Learning Journey
**[07_learning_journey.md](07_learning_journey.md)**

4-month learning progression:
- Skills development by topic (with confidence levels)
- 10 critical mistakes & lessons learned
- Growth insights from Week 1 to Week 4
- What I'd do differently
- Next steps

**Best for**: Reviewing progress and key insights

---

### ⚡ Quick Reference
**[08_quick_reference.md](08_quick_reference.md)**

Command & pattern cheat sheet:
- Prompting patterns (K-shot, CoT, 4-Layer)
- LLM integration (Pydantic, mocks)
- MCP commands (uv, FastMCP)
- Testing (pytest, fixtures)
- Multi-agent (handoff, TDD)
- Debugging tips table

**Best for**: Fast lookup during development

---

## How to Use This Documentation

### For Learning
1. Start with **[Learning Journey](07_learning_journey.md)** to see the progression
2. Read theme docs in order: Prompting → LLM → MCP → Multi-Agent
3. Review **[Mistakes](07_learning_journey.md#critical-mistakes-consolidated)** to avoid common pitfalls

### For Reference
1. Use **[Quick Reference](08_quick_reference.md)** for commands and patterns
2. Jump to specific theme docs for deep dives
3. Check **[Testing Strategies](05_testing_strategies.md)** when writing tests

### For Implementation
1. Design with **[Automation Design](06_automation_design.md)** principles
2. Implement using theme-specific guides
3. Test with **[Testing Strategies](05_testing_strategies.md)** patterns
4. Review **[Learning Journey](07_learning_journey.md)** for lessons learned

---

## Documentation Metrics

**Total Files**: 8 theme files (from 81 files)
**Reduction**: 69% fewer files
**Organization**: Theme-based (not week-based)
**Structure**: Flat `docs/` (simple, fast navigation)

**Quality Metrics**:
- ✅ No duplication (each concept explained once)
- ✅ Practical (examples > theory)
- ✅ Concise (300-500 lines per file, except comprehensive guides)
- ✅ Theme-driven (organized by what you need to find)
- ✅ Cross-referenced (links between related themes)

---

## External References

**Technical Setup**:
- [Claude Best Practices](../claude-best-practices/) - Technical configuration and patterns

**Course Materials**:
- [Course README](../README.md) - Course overview and setup
- [CLAUDE.md](../CLAUDE.md) - AI team configuration

**Official Documentation**:
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)

---

## Philosophy

This documentation follows the **Stanford AI Engineering Mindset**:

> **Build systems, not just code.**

- Extract **精华** (essence), delete noise
- Organize by **theme**, not by week
- **Practical** over theoretical
- **One explanation** per concept
- **Flat structure** for fast access

Each theme file consolidates multiple weeks of learning into a single, practical reference.

---

**Last Updated**: 2026-01-02
**Course**: CS146S Modern Software Developer (Stanford)
**Instructor**: Mihail Eric
