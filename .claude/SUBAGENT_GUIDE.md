# Subagent Usage Guide for CS146S

This guide explains how to effectively use Claude Code's subagents for the CS146S Modern Software Developer course.

## Available Subagents

### 1. Explore Agent
**Best for:** Fast codebase exploration, finding files/patterns, understanding architecture

**When to use:**
- Starting a new weekly assignment
- Finding where specific functionality is implemented
- Understanding codebase structure
- Quick searches for keywords or patterns

**How to invoke:**
```
Use the Explore agent to find...
```
Or use custom command: `/explore-week`

**Thoroughness levels:**
- `quick` - Basic searches
- `medium` - Moderate exploration (default)
- `very thorough` - Comprehensive analysis

### 2. Plan Agent
**Best for:** Architecture design, implementation planning, step-by-step strategies

**When to use:**
- Starting a complex feature implementation
- Designing API endpoints
- Planning multi-file changes
- Architectural decisions

**How to invoke:**
```
Use the Plan agent to design an implementation for...
```

### 3. General-Purpose Agent
**Best for:** Complex multi-step research, writing code, open-ended searches

**When to use:**
- Multi-round searches requiring multiple approaches
- Complex implementation tasks
- Research tasks that might evolve
- Tasks requiring creativity in approach

**How to invoke:**
```
Use the general-purpose agent to...
```

### 4. Claude-Code-Guide Agent
**Best for:** Questions about Claude Code features, hooks, slash commands, MCP servers

**When to use:**
- Learning about Claude Code capabilities
- Setting up custom configurations
- Understanding MCP server setup
- Questions about slash commands

**How to invoke:**
```
Use the claude-code-guide agent to explain...
```

## Weekly Subagent Recommendations

| Week | Primary Subagent | Secondary | Typical Tasks |
|------|------------------|-----------|---------------|
| **Week 1** | Explore | General-Purpose | Finding prompting examples, understanding techniques |
| **Week 2** | Plan | Explore | Designing extraction service, finding existing code |
| **Week 3** | General-Purpose | Plan | MCP server implementation, tool design |
| **Week 4** | Claude-Code-Guide | Explore | Learning slash commands, understanding Claude Code |
| **Week 5** | General-Purpose | Plan | Multi-agent workflow design |
| **Week 6** | Explore | General-Purpose | Finding security issues, running Semgrep |
| **Week 7** | Explore | General-Purpose | Analyzing code reviews, comparing AI vs human |
| **Week 8** | Plan | General-Purpose | Multi-stack architecture planning |

## Custom Slash Commands

The following custom commands have been created for this project:

| Command | Purpose |
|---------|---------|
| `/week` | Get help with a specific weekly assignment |
| `/explore-week` | Deep dive into a week's current state |
| `/test-week` | Run and analyze tests for a week |
| `/llm-extract` | Help with LLM extraction (Week 2) |
| `/mcp-server` | Help with MCP server development (Week 3) |
| `/refactor` | Systematic code cleanup and refactoring |

## Task vs. Direct Tool Usage

**Use Task tool (subagents) when:**
- You don't know exact file locations
- Searching requires multiple approaches
- Task is open-ended or exploratory
- Finding patterns across multiple files

**Use direct tools (Read, Grep, Glob) when:**
- You know the exact file path
- Searching for a specific class/function name
- Task is straightforward and targeted

## Best Practices

1. **Start with Explore** when beginning a new week - it quickly shows what exists
2. **Use Plan for complex changes** - ensures good architecture before coding
3. **Leverage General-Purpose for implementation** - it handles multi-step tasks well
4. **Use custom slash commands** for recurring patterns - they encode best practices
5. **Always ask clarifying questions** if the task scope is unclear

## Example Workflows

### Starting a New Week
```
/explore-week → Review what's implemented → /week [specific task]
```

### Implementing a Feature
```
/week → Plan agent design → General-Purpose implementation → /test-week
```

### Debugging
```
/explore-week [to understand issue] → General-Purpose fix → /test-week
```

### Refactoring
```
/refactor → Analyze → Propose changes → Get approval → /test-week
```
