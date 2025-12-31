# Week 5 — Multi-Agent Workflows with Claude Code

> ***We recommend reading this entire document before getting started.***

This week, your task is to build an **Agent Orchestration System** - a developer command center that tracks and manages multi-agent workflows. You will design and implement multi-agent coordination patterns that go beyond single-agent automation (Week 4) to practice orchestrating multiple specialized agents working together.

This is an **Expert-level** assignment that prepares you for the Week 8 capstone by teaching you to:
- Design agent handoff protocols and coordination patterns
- Manage agent state and context sharing between agents
- Implement fault tolerance when agents fail or return unexpected results
- Build reproducible multi-agent workflows

## Multi-Agent Coordination Patterns

You will work with three fundamental coordination patterns:

### Sequential Pattern
Agents work one after another, each handing off to the next.
- Example: `TestAgent` → `CodeAgent` → `ReviewAgent`
- Use case: CI/CD pipelines, TDD workflows, document generation

### Parallel Pattern
Multiple agents work independently on separate tasks simultaneously.
- Example: 3 `RefactorAgent` instances working on different files
- Use case: Bulk refactoring, parallel testing, distributed analysis

### Hierarchical Pattern
An orchestrator agent coordinates specialist agents.
- Example: `OrchestratorAgent` delegates to `TestAgent`, `CodeAgent`, `DocsAgent`
- Use case: Feature development, complex workflows requiring coordination

## Learn about Claude Code Multi-Agent Development

To gain a deeper understanding of multi-agent workflows in Claude Code, please review:

1. **SubAgents overview**: [docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

2. **Existing patterns in your repository**:
   - `.claude/commands/tdd-cycle.md` - Sequential orchestration example
   - `.claude/subagents/tdd-test-agent.md` - Specialist agent with handoff protocol
   - `.claude/subagents/tdd-code-agent.md` - Specialist agent with verification

## Explore the Starter Application

The starter application is a **Multi-Agent Execution Tracker** - a minimal full-stack app designed to:
- Track agent execution history across projects
- Display agent coordination patterns (sequential, parallel, hierarchical)
- Provide a visual interface for monitoring agent handoffs and results
- Store execution logs in a structured database for analysis

### Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent orchestration workflows
```

### Quickstart

1) Activate your conda environment.

```bash
conda activate cs146s
```

2) (Optional) Install pre-commit hooks

```bash
pre-commit install
```

3) Run the app (from `week5/` directory)

```bash
make run
```

4) Open `http://localhost:8000` for the frontend and `http://localhost:8000/docs` for the API docs.

5) Explore the starter application to understand:
   - Agent Registry: View available agents and their capabilities
   - Execution Timeline: See agent runs with handoff relationships
   - Pattern Library: Documentation of coordination patterns

### Testing
Run the tests (from `week5/` directory)
```bash
make test
```

### Formatting/Linting
```bash
make format
make lint
```

## Part I: Build Multi-Agent Automations (Choose 2 or more)

Select two or more coordination patterns to implement. Your automations must demonstrate multi-agent coordination beyond what you built in Week 4.

### Option A: Sequential Workflow Agent Chain

Build a sequential workflow where agents hand off tasks in a defined order.

**Example: CI/CD Pipeline Orchestrator**
- `TestAgent` runs tests
- If passing → `BuildAgent` builds application
- If passing → `DeployAgent` deploys to staging
- `MonitorAgent` checks health and reports status

**Deliverable**: Slash command `/ci-pipeline` that orchestrates this chain with proper handoff messages and error handling at each step.

**Requirements**:
- Each agent has a clear, specialized role
- Handoff messages include context for the next agent
- If an agent fails, the chain stops with clear error reporting
- Document the before/after workflow comparison

### Option B: Parallel Task Distribution

Build a system that distributes independent tasks to multiple agents working simultaneously.

**Example: Bulk Refactor Orchestrator**
- Analyze codebase for refactor opportunities (3+ files)
- Spawn 3+ `RefactorAgent` instances, each working on a different file
- Collect results from all agents
- Run test suite to verify nothing broke
- Roll back all changes if tests fail

**Deliverable**: Slash command `/bulk-refactor` that demonstrates parallel execution with result aggregation and rollback capability.

**Requirements**:
- Agents work independently without clobbering each other
- Results are collected and aggregated
- Test suite validates all changes
- Rollback mechanism if validation fails

### Option C: Hierarchical Orchestrator

Build a coordinator agent that manages specialist agents.

**Example: Feature Development Orchestrator**
- `OrchestratorAgent` breaks down feature request into subtasks
- Delegates to `TestAgent` (write tests)
- Delegates to `CodeAgent` (implement)
- Delegates to `DocsAgent` (update documentation)
- Delegates to `ReviewAgent` (code review)
- Aggregates results and provides completion summary

**Deliverable**: Slash command `/feature-dev` with hierarchical coordination and task breakdown.

**Requirements**:
- Orchestrator analyzes request and assigns subtasks
- Specialist agents have clear responsibilities
- Orchestrator aggregates and validates results
- Final summary includes all agent outputs

### Option D: Agent Memory System with MCP

Integrate MCP servers for agent communication persistence.

**Example: Enhanced TDD Cycle with Notion MCP**
- `TestAgent` writes handoff message to Notion database
- `CodeAgent` reads previous agent's state from Notion
- Each agent logs execution results to Notion
- Build execution timeline visualization from stored logs

**Deliverable**: Enhanced `/tdd-cycle` command with persistent agent memory via Notion MCP.

**Requirements**:
- Each agent writes state to Notion before handoff
- Next agent loads previous state from Notion
- Execution logs include timestamp, inputs, outputs
- Visualization of agent coordination from stored data

## Part II: Apply to Build Agent Dashboard

Now that you've built 2+ multi-agent automations, use them to build the actual Agent Orchestration System. Choose features from `week5/docs/TASKS.md` to implement.

The dashboard should:
1. **Track Agent Execution**: Log each agent run with timestamp, inputs, outputs, duration
2. **Display Coordination Patterns**: Visualize how agents work together
3. **Provide Metrics**: Success rates, execution times, handoff patterns
4. **Enable Workflow Templates**: Pre-defined multi-agent workflows that can be executed

### Integration Requirements

Your implementation must integrate with your existing infrastructure:
- **TDD Agents**: Use or extend `test-agent`, `code-agent`, `tdd-cycle`
- **SuperClaude Skills**: Leverage `sc:workflow`, `sc:pm`, `sc:implement` where appropriate
- **Serena MCP**: Use project memory for agent communication tracking
- **MCP Servers**: Integrate Notion, Web Reader, or image analysis for advanced features

## Constraints and Scope

- Work primarily in `week5/` (backend, frontend, logic, tests)
- You may extend `.claude/commands/` and `.claude/subagents/` for your automations
- Document any cross-week changes in your writeup
- Focus on multi-agent COORDINATION, not single-agent automation (that was Week 4)

## Deliverables

1) **Two or more multi-agent automations**:
   - Slash commands in `.claude/commands/*.md`
   - Subagent configurations in `.claude/subagents/*.md`
   - Clear documentation of coordination patterns used

2) **Agent Dashboard Implementation**:
   - Backend endpoints for agent registry, execution logs, workflow templates
   - Frontend visualization of agent coordination
   - Integration with existing TDD agents and infrastructure

3) **Write-up** (`week5/week5_writeup.md`) including:
   - Design pattern & inspiration for each automation
   - Technical design (goals, inputs/outputs, agents, steps)
   - Implementation details (files, agent configuration, coordination logic, error handling)
   - Before vs. after (manual workflow vs. automated workflow)
   - Multi-agent coordination notes (roles, strategy, challenges, failures)
   - Integration with existing infrastructure
   - Screenshots/diagrams of agent coordination
   - Learning reflection

## SUBMISSION INSTRUCTIONS

1. Make sure you have all changes pushed to your remote repository for grading.
2. **Make sure you've added both brentju and febielin as collaborators on your assignment repository.**
3. Submit via Gradescope.
