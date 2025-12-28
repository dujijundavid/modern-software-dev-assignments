# Agent Communication Log

Record of interactions with AI agents (Claude Code, subagents) and effective prompts.

---

## 2025-12-28: Multi-Machine Git Collaboration

### Task: Setup .serena/ for Git sharing

**Agent Used:** @Explore (subagent)

**Prompt:**
```
Explore the repository structure to understand the current Git configuration for multi-machine collaboration. Focus on:
1. Current .gitignore setup
2. CLAUDE.md status
3. .serena/ directory structure
4. What's currently tracked
```

**Result:** Excellent analysis
- Identified `.serena/` was completely ignored
- Found `.serena/.gitignore` only excludes `/cache`
- Clarified CLAUDE.md already tracked

**Performance:** ⭐⭐⭐⭐⭐ (5/5)
- Comprehensive file structure analysis
- Clear categorization of shareable vs machine-specific
- Provided verification commands

---

### Task: Design .gitignore strategy

**Agent Used:** @Plan (subagent)

**Prompt:**
```
Design a detailed implementation plan for multi-machine Git collaboration focusing on .serena/ directory.

## Context from Exploration
[detailed context about current state]

## Requirements
1. Allow sharing of .serena configuration and memory files across machines
2. Keep machine-specific cache out of version control
3. Provide verification commands to ensure correct behavior
4. Explain the reasoning behind each .gitignore rule
```

**Result:** Solid implementation plan
- Provided exact .gitignore changes
- Included verification commands
- Explained negation pattern mechanics

**Performance:** ⭐⭐⭐⭐ (4/5)
- Good technical depth
- Could have included more edge cases

**Lessons Learned:**
- Provide full context from previous exploration
- Ask for verification commands explicitly
- Request explanations for each technical decision

---

## 2025-12-28: Serena Memory System Expansion

### Task: Analyze memory gaps

**Agent Used:** PM Agent + Tech Lead (parallel)

**Prompt:**
```
From a PROJECT MANAGEMENT perspective, analyze what content should be tracked as Serena memory for:
- Team collaboration
- Cross-session continuity
- Knowledge preservation
- Onboarding new members

Provide 3-5 specific proposals with memory name, content description, value, and beneficiaries.
```

**Result (PM Agent):** Excellent project management perspective
- Identified 5 key memory categories
- Focused on collaboration and continuity
- Provided clear value propositions

**Performance:** ⭐⭐⭐⭐⭐ (5/5)
- Understood project management needs deeply
- Structured proposals with practical examples
- Prioritized by impact

---

**Prompt (Tech Lead):**
```
From a TECHNICAL LEADERSHIP perspective, analyze what technical content should be tracked as Serena memory for:
- Architecture decisions
- Development workflow
- Testing strategies
- Common issues/solutions
- Performance considerations
```

**Result (Tech Lead):** Strong technical analysis
- 5 technical memories proposed
- Focused on code quality and consistency
- Included security and testing patterns

**Performance:** ⭐⭐⭐⭐⭐ (5/5)
- Deep technical understanding
- Considered long-term maintainability
- Provided implementation priorities

**Lessons Learned:**
- Parallel PM + Tech analysis provides comprehensive view
- Both perspectives needed for balanced memory system
- Always ask for priority/ordering when getting multiple proposals

---

## Effective Prompt Patterns

### For Code Analysis
```
Analyze [specific area] focusing on:
1. [Aspect 1]
2. [Aspect 2]
3. [Aspect 3]

Provide:
- Current state assessment
- Issues identified
- Recommended improvements
- Code examples if applicable
```

### For Architecture Decisions
```
Design [system/component] with consideration for:
- Scalability
- Maintainability
- Testability
- Security

Provide:
1. Architecture options (at least 2)
2. Trade-offs for each option
3. Recommended approach with rationale
4. Implementation steps
```

### For Testing Strategy
```
Design comprehensive test strategy for [component]:
- Unit test coverage
- Integration test scenarios
- Edge cases to consider
- Mocking strategy for external dependencies

Include:
- Test structure recommendations
- Fixture patterns
- Coverage targets
```

### For Debugging Help
```
Issue: [symptom description]

Context:
- What I was doing: [action]
- Expected behavior: [expected]
- Actual behavior: [actual]
- Error message: [error if any]

Investigation requested:
1. Root cause analysis
2. Potential fixes
3. Prevention strategies
```

---

## Agent Selection Guide

| Task Type | Best Agent | Example |
|-----------|------------|---------|
| Codebase exploration | @Explore | "What files handle routing?" |
| FastAPI development | @fastapi-expert | "Add new endpoint with auth" |
| Testing | @python-testing-expert | "Improve test coverage for X" |
| Security review | @python-security-expert | "Check for SQL injection" |
| Performance | @performance-optimizer | "Profile slow database queries" |
| Architecture | @tech-lead-orchestrator | "Design multi-agent system" |
| Documentation | @documentation-specialist | "Create API documentation" |
| Code review | @code-reviewer | "Review before committing" |

---

## Collaboration Best Practices

### When to Use Multiple Agents
1. **Complex tasks requiring multiple perspectives**
   - Example: PM + Tech Lead for memory system design
   - Benefit: Comprehensive analysis from different angles

2. **Sequential development workflow**
   - Example: code-archaeologist → fastapi-expert → python-testing-expert → code-reviewer
   - Benefit: Each agent specializes in their phase

### When to Use Single Agent
1. **Focused, well-defined tasks**
   - Example: "Add unit tests for function X"
   - Benefit: Faster, more direct

2. **Exploratory research**
   - Example: "How does the current auth system work?"
   - Benefit: Single source of truth

---

## Agent Performance Observations

### High Performers (5/5)
- **@Explore**: Excellent codebase navigation and summarization
- **@fastapi-expert**: Deep framework knowledge, practical solutions
- **@code-reviewer**: Thorough, security-aware reviews

### Reliable Performers (4/5)
- **@python-testing-expert**: Solid testing expertise, sometimes needs clarification on async
- **@python-security-expert**: Good security analysis, could be more proactive
- **@Plan agent**: Good planning, may need multiple iterations

### Use with Guidance (3/5)
- **General-purpose agents**: Good for broad tasks, but specialists preferred for technical work

---

## Communication Patterns That Work

### Pattern 1: Progressive Refinement
```
1. Start with @Explore to understand current state
2. Use @Plan to design approach
3. Use specialist (@fastapi-expert, etc.) for implementation
4. Use @code-reviewer before committing
```

### Pattern 2: Parallel Investigation
```
1. Launch multiple @Explore agents in parallel for different areas
2. Synthesize findings
3. Proceed with implementation
```

### Pattern 3: Specialist Collaboration
```
1. @fastapi-expert designs API
2. @python-testing-expert designs tests
3. @python-security-expert reviews security
4. @code-reviewer final review
```

---

## Tips for Better Agent Collaboration

1. **Provide context upfront** - Include background, constraints, what you've tried
2. **Be specific about output format** - Ask for code examples, step-by-step plans, etc.
3. **Use experts for technical work** - Specialists beat generalists for FastAPI, testing, security
4. **Always review before committing** - @code-reviewer catches issues specialists miss
5. **Iterate when needed** - Don't expect perfection on first try, refine based on results
