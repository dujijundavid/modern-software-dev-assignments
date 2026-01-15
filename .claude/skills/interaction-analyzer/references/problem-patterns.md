# Problem Patterns

Common inefficiency patterns in AI interactions, categorized by detection dimension.

## Detection Dimensions

### 1. Goal Clarity (目标清晰度)

**Pattern**: Unclear User Intent
- **Symptoms**: Multiple clarifications, scope creep, pivoting objectives
- **Examples**:
  - "Check my system" → user wanted status document, not troubleshooting
  - "Fix this bug" → user actually wanted refactoring
- **Root Causes**:
  - Ambiguous initial request
  - AI didn't ask clarifying questions
  - Assumptions made without verification
- **Detection**: Count clarifications, track objective shifts

**Pattern**: Mismatched Output Format
- **Symptoms**: Generated wrong format (code vs docs, JSON vs Markdown)
- **Examples**:
  - User wanted summary, AI generated full analysis
  - User wanted quick check, AI generated comprehensive report
- **Root Causes**: Not confirming expected output upfront
- **Detection**: Format-related corrections

### 2. Tool Selection (工具选择)

**Pattern**: Suboptimal Tool Priority
- **Symptoms**: Used generic tools when specialized ones available
- **Examples**:
  - Used `find` + `cat` instead of `claude mcp list`
  - Used `Read` on multiple files instead of `Grep`
  - Used generic `python-expert` instead of `fastapi-expert`
- **Root Causes**: Didn't check available specialized tools first
- **Detection**: Retrying same task with different tool

**Pattern**: Sequential When Parallel Possible
- **Symptoms**: Multiple independent tool calls in sequence
- **Examples**:
  - Reading 3 files one by one instead of parallel
  - Running independent bash commands sequentially
- **Root Causes**: Not identifying independent operations
- **Detection**: Multiple tool calls with no dependencies

### 3. Execution Order (执行顺序)

**Pattern**: Wrong Scope First
- **Symptoms**: Investigated wrong product/scope initially
- **Examples**:
  - Checked Claude Desktop config when user meant Claude Code
  - Looked at system-level instead of project-level
- **Root Causes**: Didn't confirm scope/context upfront
- **Detection**: Scope corrections from user

**Pattern**: Premature Implementation
- **Symptoms**: Started coding before understanding requirements
- **Examples**:
  - Built feature before clarifying edge cases
  - Generated code before confirming architecture
- **Root Causes**: Jumped to solution without analysis
- **Detection**: Major rewrites or clarifications mid-task

### 4. Communication Efficiency (沟通效率)

**Pattern**: Excessive Back-and-Forth
- **Symptoms**: High turn count for simple task
- **Examples**:
  - Simple config check took 5+ turns
  - Basic question required multiple clarifications
- **Root Causes**:
  - Information gaps
  - Not gathering context before starting
- **Detection**: Turn count vs task complexity ratio

**Pattern**: Information Asymmetry
- **Symptoms**: AI knows something user doesn't (or vice versa)
- **Examples**:
  - AI assumed knowledge user lacked
  - User didn't provide crucial context
- **Root Causes**: Insufficient context gathering
- **Detection**: "I didn't know that" patterns

### 5. Context Management (上下文管理)

**Pattern**: Scope Creep
- **Symptoms**: Task expanded beyond original boundaries
- **Examples**:
  - "Fix this bug" → ended up refactoring entire module
  - "Check config" → ended up analyzing whole system
- **Root Causes**: Not defining and defending scope
- **Detection**: Task completion markers missed

**Pattern**: Context Switching
- **Symptoms**: Jumped between unrelated tasks
- **Examples**:
  - Mixed frontend and backend work without clear boundary
  - Switched between debugging and feature building
- **Root Causes**: Poor task prioritization and batching
- **Detection**: Rapid topic switches in conversation

## Extended Patterns (Code Quality)

### Code Smells
- Duplicated logic across files
- Missing error handling
- Inconsistent patterns
- Security vulnerabilities

### Best Practice Deviations
- Not using project-specific experts
- Ignoring established conventions
- Bypassing safety checks

## Workflow Patterns

### Inefficient Workflows
- Manual repetitive tasks (should be automated)
- Sequential independent tasks (should be parallel)
- Missing abstraction opportunities

### Optimization Opportunities
- Repeated patterns → Create skill
- Common debugging steps → Create script
- Frequent clarifications → Update documentation

## Pattern Matching Strategy

When analyzing conversation, check for:

1. **Correction Count**: How many times did user say "no", "not that", "wrong"?
2. **Tool Retries**: Same task attempted with different tools?
3. **Scope Changes**: Did objectives shift during execution?
4. **Turn Efficiency**: Complexity achieved vs turns taken
5. **Parallel Missed**: Were there independent operations done sequentially?

## Severity Levels

- **Low**: Minor inefficiency, task completed successfully
- **Medium**: Noticeable friction, user had to correct course
- **High**: Major inefficiency, multiple rounds wasted

Use severity to prioritize suggestions in output.
