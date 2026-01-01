# Learning Session: Multi-Agent Design Patterns

**Date**: 2025-01-01
**Duration**: ~30 minutes
**Starting Level**: Intermediate (heard of concepts, wanted deeper understanding)
**Ending Level**: Advanced (can identify patterns and apply them)
**Session Type**: Concept Learning

## Concepts Covered

### Orchestrator Pattern
- **Status**: ✅ Understood
- **Confidence**: 8/10
- **Quiz Score**: 2/2 correct
- **Key Insight**: Orchestrator coordinates but doesn't implement. Uses handoff protocol to delegate tasks to specialized agents.

### Handoff Protocol
- **Status**: ✅ Understood
- **Confidence**: 7/10
- **Quiz Score**: 1/2 correct (partial on implementation details)
- **Key Insight**: Communication mechanism between agents. Single-direction delegation + memory as shared state is simple but effective.
- **Knowledge Gap**: Bidirectional handoffs and failure recovery mechanisms need exploration

### Specialized Agent Patterns
- **Status**: ✅ Understood
- **Confidence**: 7/10
- **Quiz Score**: 2/2 correct
- **Key Insight**: Role-based (frontend, backend, security experts) vs Capability-based (code-reviewer, performance-optimizer) vs Workflow-stage agents (TestAgent, CodeAgent in TDD)

## Questions & Answers

**Q1**: How does Orchestrator differ from "one agent does everything"?

**A1**: User answered: "b. 单个agent 做test driven dev 可能会出现: (1) 测试编写逻辑与代码编写逻辑不一致 (2) Agent 上下文过长 (3) 单一 agent 可能无法同时掌握所有技术栈"

**Feedback**: ✓ Excellent analysis! You identified three key issues:
1. **Role confusion**: Same agent switching between tester/coder mindsets
2. **Context overflow**: Too much responsibility → prompt bloat
3. **Skill limitations**: No agent is expert at everything

The Orchestrator pattern solves this by **delegating** to specialists (TestAgent for tests, CodeAgent for implementation), keeping each agent focused.

**Q2**: Handoff Protocol - How do agents communicate in TDD cycle?

**A2**: User answered: "通过delegate 任务以及memory 作为约束沟通更新信息。"

**Feedback**: ✓ Correct! The handoff uses:
1. **Task delegation**: Orchestrator calls Task with specific subagent_type
2. **Memory as constraint**: TestAgent's output (failing tests) becomes CodeAgent's input constraint
3. **Context preservation**: Orchestrator maintains session context

This creates a "relay race" where each agent passes a baton (test results → implementation code).

**Q3**: Handoff design - What if CodeAgent fails to fix the test?

**A3**: User answered: "d) a+b+c (All options)"

**Feedback**: Exactly! Real systems need all three:
- **Retry**: Give CodeAgent another chance with error details
- **Fallback**: Orchestrator tries a simpler approach or different agent
- **Escalate**: Notify user if automated resolution fails

**Q4**: Which agent pattern does tdd-cycle use?

**A4**: User answered: "a"

**Feedback**: ✓ Correct! It's **Role-based**:
- `code-reviewer` for code quality
- `python-testing-expert` for pytest

The agents are defined by their **role/expertise** domain.

**Q5**: Which pattern for code archaeology vs frontend work?

**A5**: User answered: "a"

**Feedback**: ✓ Correct! Different patterns for different needs:
- **Code archaeology**: Capability-based (`code-archaeologist` capability)
- **Frontend**: Role-based (`frontend-developer` role)

**Q6**: Feature-dev agents - what pattern?

**A6**: User answered: "workflow stage agents"

**Feedback**: ✓ Correct! Feature-dev has:
- `code-explorer` → `code-architect` → `code-reviewer` → `test-runner`
Each agent handles a **stage** in the feature development workflow.

**Q7**: Workflow vs Role-based agents - difference?

**A7**: User answered: "d) Workflow + role 其实区别没有很大。分析代码变更coding agent调用git diff 之类的..."

**Feedback**: ✓ Insightful observation! The **boundary is fuzzy** because:
1. Both use agent specialization
2. Workflow stages often map to roles (e.g., testing stage → tester role)
3. **Key difference**: Workflow is about **sequence/orchestration**, role is about **domain expertise**

Your example is perfect: "coding agent calls git diff" - this is a workflow action performed by a role-based agent.

## Visualizations Learned

**Orchestrator Pattern (ASCII)**:
```
┌──────────────────┐
│   Orchestrator   │
│  (Task Tool)     │
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
┌───┴───┐ ┌──┴─────┐
│Agent A│ │Agent B │
└───────┘ └────────┘
```

**Handoff Protocol (Sequence)**:
```
[Orchestrator] → [TestAgent]
       ↓              ↓
   [Failing Test] ← [Write test]
       ↓
[Orchestrator] → [CodeAgent]
       ↓              ↓
   [Passing Test] ← [Fix code]
       ↓
[User] ← [Results]
```

## Spaced Repetition Schedule

| Review Date | Concept | Reason | Confidence Goal |
|-------------|---------|--------|-----------------|
| 2025-01-04 | Handoff Protocol | Review failure recovery patterns | 8/10 |
| 2025-01-08 | All three patterns | Weekly consolidation - apply to week5 | 8/10 |
| 2025-01-15 | Multi-agent systems | Full integration - design own system | 9/10 |

## Next Learning Steps

1. **[ ] Practice**: Analyze week5 multi-agent implementation and identify which patterns it uses
2. **[ ] Explore**: Bidirectional handoffs (agents communicating back to orchestrator)
3. **[ ] Connect**: Compare multi-agent patterns with single-agent prompt chaining (Week 1)
4. **[ ] Apply**: Design a multi-agent workflow for a new feature

## System Improvements Made

During this session, identified critical issue:
- **Mermaid diagrams don't render in Claude Code conversations**
- **Solution**: Implemented environment-aware visualization
  - Conversations: ASCII art
  - Documentation: Mermaid (for VSCode/GitHub rendering)
- **Files updated**:
  - `.claude/commands/learning-mode.md`
  - `skills/learning-mode/SKILL.md`
  - `skills/learning-mode/references/mermaid-patterns.md`

## Notes

**Key realization**: Multi-agent systems are about **appropriate delegation**, not just parallelization. The Orchestrator's job is to:
1. Break down complex tasks
2. Match tasks to specialist agents
3. Coordinate handoffs and memory
4. Handle failures and retries

**User insight**: "Workflow + Role 其实区别没有很大" - the boundaries between patterns are permeable. Real systems often blend multiple patterns based on needs.

**Next session focus**: Week5 multi-agent architecture - how does it implement these patterns?
