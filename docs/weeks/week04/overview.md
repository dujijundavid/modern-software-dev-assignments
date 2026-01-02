---
week: 4
title: "Week 4: Slash Commands & SubAgents"
type: concept
status: completed
created: 2025-12-31
updated: 2026-01-02
related:
  - week:4:implementation.md
  - week:4:reflection.md
tags: [week-4, concepts, slash-commands, subagents, automation]
---

# Week 4: Slash Commands & SubAgents

> **Navigation**: [CS146S Docs](../../INDEX.md) > [Weeks](../) > [Week 4](./) > Overview

## Learning Objectives

- **Master the 4-Layer Prompt Model** for designing effective slash commands
- **Understand SubAgents collaboration patterns** for specialized AI workflows
- **Build production-ready automations** using Claude Code features
- **Apply critical analysis** to AI-assisted development workflows
- **Design reusable, composable systems** rather than one-off scripts

## Key Concepts

### Concept 1: 4-Layer Prompt Model

**Description**: The 4-Layer Prompt Model is a cognitive framework for designing slash commands, not just a format template. Each layer addresses different cognitive challenges:

- **Layer 1 (YAML)**: Machine-readable metadata for tool availability and command discovery
- **Layer 2 (Persona)**: Defines role boundaries to prevent role confusion
- **Layer 3 (Process)**: Structured workflow with quality gates
- **Layer 4 (Output)**: Standardized output templates for better user experience

**Why it matters**: This model ensures commands are discoverable, maintainable, and provide consistent user experiences. It bridges the gap between machine requirements and human expectations.

**Key points**:
- Each layer serves a specific cognitive purpose
- From machine-readable to user-experience complete chain
- Not just formatting, but a design philosophy
- Requires critical analysis, not just template application

**Example**:
```yaml
---
name: architect-hub
description: "Module refactoring tool for structural changes"
category: development
tools: [Read, Write, Edit, Bash, Grep, Glob]
---
```

### Concept 2: SubAgents Collaboration Pattern

**Description**: SubAgents are specialized AI assistants with their own system prompts, tools, and context. They work together through structured handoffs rather than natural language conversation.

**Why it matters**: SubAgents enable:
- **Specialization**: Each agent focuses on one domain, reducing cognitive load
- **Verification loops**: Agents validate each other's work, ensuring quality
- **Role separation**: Prevents role conflicts and responsibility confusion

**Key points**:
- **Handoff is a protocol**: Structured information transfer, not conversation
- **Verification cycles**: Multi-agent validation prevents errors
- **Orchestrator manages flow**: Coordinates without directly implementing
- **First principles thinking**: Understand why separation matters

**Example**:
```markdown
## TestAgent → CodeAgent Handoff

### Feature: DELETE /notes/{id}

### Tests Written
- `test_delete_note_success` - Verifies deletion and database removal
- `test_delete_note_not_found` - Verifies 404 response

### Implementation Requirements
1. Return 204 on success
2. Return 404 if note not found
3. Remove note from database
```

### Concept 3: TDD Cycle with SubAgents

**Description**: Using SubAgents to enforce Test-Driven Development discipline by separating TestAgent and CodeAgent responsibilities.

**Why it matters**: TDD often fails in practice because developers lack discipline. SubAgents enforce the workflow:
- **TestAgent**: Only writes tests, never implementation
- **CodeAgent**: Only writes implementation, never modifies tests
- **Verification loop**: TestAgent validates CodeAgent's work

**Key points**:
- **Cognitive conflict prevention**: Testing and implementation require different mindsets
- **Responsibility separation**: Each agent focuses on their domain
- **Quality assurance**: Natural verification loop between agents
- **Completeness standard**: Only TestAgent can sign off on completion

### Concept 4: Critical Analysis in AI Design

**Description**: The ability to identify design flaws in AI automations and propose concrete improvements.

**Why it matters**: First-generation AI automations often have hidden flaws. Critical analysis prevents deploying broken systems.

**Key points**:
- **Identify defects**: Command interface confusion, lack of error handling
- **Propose improvements**: Structured parameters, decision frameworks
- **Validate with reality**: Use real scenarios, not fictional examples
- **Iterate continuously**: Design is never complete

## Prerequisites

- **Week 1-3 completion**: Familiarity with FastAPI, pytest, and basic workflow
- **Claude Code installed**: Access to slash commands and subagents
- **Python environment**: Conda environment with required dependencies
- **Git familiarity**: Understanding of branches and version control

**Setup commands**:
```bash
# Activate environment
conda activate cs146s

# Navigate to week4
cd week4/

# Install pre-commit hooks (optional)
pre-commit install

# Run the application
make run

# Run tests
make test
```

## Resources

- **Primary**: [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Official Anthropic documentation on slash commands and CLAUDE.md patterns
- **Primary**: [SubAgents Overview](https://docs.anthropic.com/en/docs/claude-code/sub-agents) - Official documentation on SubAgents collaboration patterns
- **Supplementary**: [skill-design-best-practices.md](../../claude-best-practices/03-create/skill-design-best-practices.md) - 4-Layer Prompt Model deep dive
- **Supplementary**: [subagent-system.md](../../claude-best-practices/02-understand/subagent-system.md) - SubAgents theoretical foundation
- **Reference**: [tdd-first-principles.md](../../claude-best-practices/02-understand/tdd-first-principles.md) - TDD with SubAgents rationale

## Related Patterns

- [Week 2: LLM Integration](../week02/overview.md) - Week 4 builds on Week 2's LLM extraction work
- [Week 5: Warp Automation](../week05/overview.md) - Week 5 extends Week 4's automation concepts
- [AI Engineering Mindset](../../CLAUDE.md#-ai-engineering-mindset-the-mihail-eric-framework) - The three questions framework applied

## Quick Links

- [Implementation Details](./implementation.md) - Technical approach and decisions
- [Reflection](./reflection.md) - Learning outcomes and lessons learned
- [Weekly Deliverable](../../week4/writeup.md) - Original submission writeup
- [Assignment](../../week4/week4_assignment.md) - Week 4 assignment description

## AI Engineering Mindset

**The Three Questions**:

1. **What's the bottleneck?**
   - Module refactoring requires manual import updates (error-prone)
   - TDD discipline breaks down without enforcement
   - Testing and implementation require different mindsets

2. **What's the leverage point?**
   - Slash commands for repeatable workflows
   - SubAgents for enforced role separation
   - Handoff protocols for structured communication

3. **How to compound value?**
   - Composable automations that work together
   - Reusable patterns across different domains
   - Self-improving systems that learn from mistakes

**Automation Level**: Level 3 (Composable System)
- Evidence: SubAgents with handoff protocols
- Next level: Level 4 (Self-Improving) - Add error recovery and learning

## Starter Application

Week 4 includes a minimal full-stack "developer's command center":
- **Backend**: FastAPI with SQLite (SQLAlchemy)
- **Frontend**: Static UI (no Node toolchain needed)
- **Testing**: pytest with basic tests
- **Quality**: Pre-commit hooks (black + ruff)
- **Purpose**: Playground for experimenting with automations

### Structure
```
backend/                # FastAPI application
frontend/               # Static UI served by FastAPI
data/                   # SQLite database + seed
docs/                   # TASKS for agent-driven workflows
```

### Quickstart
```bash
# From week4/ directory
make run        # Start application (http://localhost:8000)
make test       # Run tests
make format     # Format with black
make lint       # Lint with ruff
```

---
*[Template: weekly_overview.md - Last updated: 2026-01-02]*
