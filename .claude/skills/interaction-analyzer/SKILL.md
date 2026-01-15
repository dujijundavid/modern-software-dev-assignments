---
name: interaction-analyzer
description: Analyze AI conversation patterns to identify inefficiencies and generate improvement recommendations with optimized prompts and workflows. Use when user provides corrective feedback, multiple failed attempts occurred, user asks "why did this take so long?", task required excessive turns, or detecting optimization patterns. Provides LLM-powered pattern recognition (not rule-based), three-layer output (user report + AI optimization + reusable assets), and covers code quality, workflow optimization, and best practices.
---

# Interaction Analyzer

智能对话分析系统，通过 LLM 驱动的模式识别，自动检测 AI 交互中的低效模式，提供可操作的改进建议。

## Quick Start

When triggered, analyze the conversation to identify inefficiencies:

1. **Detect patterns** - Use LLM semantic understanding (not rules)
2. **Categorize issues** - Map to problem patterns in [problem-patterns.md](references/problem-patterns.md)
3. **Generate recommendations** - Provide workflow and prompt improvements
4. **Create assets** - Generate reusable prompts and templates

## When to Use

**Automatic triggers** (AI-side detection):
- User provides corrective feedback ("no", "not that", "wrong scope")
- Multiple tool retries for same task
- Excessive turn count for task complexity
- Scope changes during execution

**Manual triggers** (user-side invocation):
- `/analyze` - Analyze current conversation
- `/analyze --scope=last_n_turns` - Analyze recent turns
- "Why did this take so long?" - Explicit efficiency question
- "What went wrong?" - Post-mortem analysis

## Analysis Dimensions

Use LLM semantic understanding to check for issues in these dimensions:

### 1. Goal Clarity
- Was the user's intent clear from the start?
- Did AI ask clarifying questions when needed?
- Did the output format match user expectations?

### 2. Tool Selection
- Were specialized tools used before generic ones?
- Could independent operations be parallelized?
- Was the most specific agent/expert selected?

### 3. Execution Order
- Was scope confirmed before investigation?
- Were assumptions validated early?
- Did implementation start before understanding?

### 4. Communication Efficiency
- How many corrections were needed?
- Was there excessive back-and-forth?
- Did AI gather context before acting?

### 5. Context Management
- Did scope creep occur?
- Was there unnecessary context switching?
- Were key information pieces missed?

## Output Structure

Generate three layers of output:

### Layer 1: User Report (Markdown)
```markdown
## Conversation Analysis

### Issues Detected
| Problem | Severity | Root Cause |
|---------|----------|------------|
| Unclear goal | Medium | Didn't confirm output format |

### Recommendations
- Ask clarifying question before starting
- Confirm: "Status check or document generation?"

### Before vs After
- Before: 5 turns, multiple corrections
- After: 2 turns, direct execution
```

### Layer 2: AI Optimization (Structured)
```yaml
improvements:
  - priority: 1
    issue: "Scope not confirmed"
    suggestion: "Ask: 'Claude Code or Claude Desktop?'"
  - priority: 2
    issue: "Suboptimal tools"
    suggestion: "Use 'claude mcp list' before find/cat"
```

### Layer 3: Reusable Assets
- Generate optimized prompt template
- Create workflow checklist
- Document anti-patterns to avoid

## Reference Materials

Load these references as needed:

- **[problem-patterns.md](references/problem-patterns.md)** - Common inefficiency patterns
  - Use when categorizing detected issues
  - Provides severity levels and detection strategies

- **[workflow-templates.md](references/workflow-templates.md)** - Optimized workflows
  - Use when generating improvement suggestions
  - Contains decision frameworks and tool selection guides

- **[prompt-templates.md](references/prompt-templates.md)** - Optimized prompts
  - Use when creating reusable prompt assets
  - Covers common task types with structure

## Analysis Process

1. **Review conversation history**
   - Count user corrections
   - Identify tool retries
   - Note scope changes

2. **Map to problem patterns**
   - Use [problem-patterns.md](references/problem-patterns.md) categories
   - Assign severity (Low/Medium/High)
   - Identify root causes

3. **Generate recommendations**
   - Reference [workflow-templates.md](references/workflow-templates.md)
   - Suggest specific workflow improvements
   - Recommend better tool choices

4. **Create reusable assets**
   - Generate optimized prompt using [prompt-templates.md](references/prompt-templates.md)
   - Create workflow checklist
   - Document lessons learned

## Extended Analysis

### Code Quality Analysis
When task involved code changes:
- Check for security vulnerabilities
- Identify performance issues
- Note best practice deviations
- Suggest appropriate agents (@code-reviewer, @python-security-expert)

### Workflow Optimization
When task involved multiple steps:
- Identify repetitive manual steps
- Suggest automation opportunities
- Recommend parallel execution patterns
- Propose agent coordination strategies

### Best Practice Recommendations
Based on project context:
- Recommend domain-specific experts
- Suggest project-specific patterns
- Reference established conventions
- Provide learning resources

## Output Location

When generating reusable assets:

- Prompts: `.claude/prompts/` or project-specific location
- Workflows: `.claude/workflows/` or integrate into existing docs
- Analysis: `docs/conversation-analysis.md` or user-specified location

## Key Principles

1. **LLM-Powered, Not Rule-Based** - Use semantic understanding, not keyword matching
2. **Constructive Feedback** - Focus on improvements, not criticism
3. **Actionable Output** - Provide specific, implementable suggestions
4. **Asset Generation** - Create reusable value from analysis
5. **Multi-Layer Output** - Serve both user understanding and AI improvement

## Examples

### Example 1: System Check Inefficiency
```
Detected: 4 turns to identify correct config location
Pattern: Wrong scope first (Claude Desktop vs Code)
Severity: Medium
Recommendation: Run `claude mcp list` to confirm product
Asset: Generate system-check.md prompt template
```

### Example 2: Code Investigation Inefficiency
```
Detected: Read 5 entire files when grep would suffice
Pattern: Suboptimal tool priority
Severity: Low
Recommendation: Use Grep first, then targeted Read
Asset: Add code-investigation.md to prompt templates
```

### Example 3: Scope Creep
```
Detected: Bug fix turned into refactoring
Pattern: Scope creep
Severity: Medium
Recommendation: Define and defend scope upfront
Asset: Create scope-definition checklist
```
