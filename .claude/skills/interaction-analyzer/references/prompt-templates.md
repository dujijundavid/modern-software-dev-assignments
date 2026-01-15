# Prompt Templates

Optimized prompt templates for common tasks to prevent inefficiencies.

## Template 1: System Status Analysis

```
Analyze the current Claude Code system configuration and generate a status document.

Steps:
1. Run `claude mcp list` to get MCP server status
2. Run `claude --version` for version information
3. Read .claude/settings.local.json for project permissions
4. Check ~/.claude/commands/ for available skills
5. Integrate findings into a structured Markdown document

Document structure:
- Version information
- MCP servers (status table)
- Available skills/commands
- Configuration file locations
- System architecture diagram (optional)

Save to: docs/claude-code-status.md

Assumptions:
- User wants a document (not just terminal output)
- Focus on Claude Code, not Claude Desktop
- Include both status and configuration paths
```

## Template 2: Code Investigation

```
Investigate {code_feature} in the codebase.

Context:
- Target: {specific_class/function/pattern}
- Scope: {single_file / entire_codebase / specific_directory}
- Goal: {understand / modify / debug}

Approach:
1. Use Serena's find_symbol to locate the target
2. Use get_symbols_overview for file structure
3. Read relevant symbol bodies (not entire files)
4. Use find_referencing_symbols to understand usage
5. Summarize findings with file:line references

Output:
- Location of relevant code
- How it works
- Dependencies and relationships
- Notes for {modification/understanding/debugging}
```

## Template 3: Multi-Agent Coordination

```
Coordinate multiple agents to complete {task}.

Agents:
- Agent A: {responsibility} (works in {directory})
- Agent B: {responsibility} (works in {directory})
- Agent C: {responsibility} (validation)

Coordination strategy:
1. Define clear ownership boundaries (no overlapping files)
2. Establish shared contract (e.g., API schema, interface)
3. Run agents in parallel where possible
4. Agent C validates A and B's work
5. If validation fails, rollback and retry
6. If all pass, merge results

Success criteria:
- All agents complete without errors
- Validation passes
- No merge conflicts
- Tests pass
```

## Template 4: Feature Implementation

```
Implement {feature_description} following these constraints:

Requirements:
- Functionality: {what it should do}
- Integration: {where it fits in existing system}
- Compatibility: {backward compatibility requirements}

Before implementing:
1. Use EnterPlanMode to design approach
2. Get user approval on:
   - Files to modify
   - API changes (if any)
   - Breaking changes (if any)

Implementation:
- Follow existing patterns in the codebase
- Make minimal, focused changes
- Use domain-specific agents (e.g., @fastapi-expert)
- Add tests for new functionality

After implementing:
- Run tests
- Use @code-reviewer before committing
- Update documentation if API changed
```

## Template 5: Debug Workflow

```
Debug {issue_description}.

Information gathering:
1. Get exact error message or unexpected behavior
2. Understand expected vs actual output
3. Identify when issue started (recent changes?)

Investigation:
1. Use Grep to search for error context
2. Check git diff for recent changes
3. Use Serena to find relevant code
4. Form hypothesis about root cause

Verification:
1. Test hypothesis with targeted checks
2. Isolate minimal reproducible case
3. Confirm fix resolves issue

Fix implementation:
- Minimal change principle
- Add test to prevent regression
- Document if issue was subtle
```

## Template 6: Document Generation

```
Generate {document_type} for {subject}.

Target audience: {technical / non-technical / mixed}
Output format: {README / API docs / guide / internal doc}

Process:
1. Understand scope:
   - What should be covered?
   - What depth is appropriate?
   - Are there existing docs to follow?

2. Gather information:
   - Use /sc:index for project overview (if applicable)
   - Read relevant source code
   - Check for existing patterns

3. Structure document:
   - Create outline first
   - Fill in sections systematically
   - Add examples where helpful

4. Review:
   - Check clarity and completeness
   - Verify technical accuracy
   - Ensure consistent style

Output location: {path}
```

## Template 7: Code Quality Review

```
Review code quality for {component/scope}.

Check for:
- Security vulnerabilities (SQL injection, XSS, auth)
- Performance issues (inefficient queries, blocking calls)
- Code smells (duplication, complexity, poor naming)
- Best practices (following project conventions)
- Error handling (edge cases, failures)

Tools to use:
- @code-reviewer for comprehensive review
- @python-security-expert for security
- @performance-optimizer for performance

Output:
- Severity-tagged findings
- Specific file:line references
- Actionable recommendations
- Priority order for fixes
```

## Template 8: Test Strategy

```
Design test strategy for {feature/component}.

Test categories:
1. Unit tests: {what to test}
2. Integration tests: {what to test}
3. Edge cases: {what to test}
4. Error conditions: {what to test}

Test framework: {pytest / jest / other}

Coverage goals:
- Minimum coverage percentage
- Critical paths to cover
- Edge cases to include

Test structure:
- Use fixtures for setup
- Test isolation (no shared state)
- Clear test names
- Arrange-Act-Assert pattern

Use @python-testing-expert for implementation guidance.
```

## Template 9: Refactoring Plan

```
Plan refactoring for {code_area}.

Current issues:
- {specific problems identified}

Refactoring goals:
- {what improvement is desired}

Approach:
1. Understand current structure (use code-archaeologist)
2. Identify improvement opportunities
3. Plan changes with minimal risk
4. Ensure tests cover refactored code
5. Execute incrementally

Principles:
- Don't change behavior, only structure
- Run tests after each change
- Commit small, logical chunks
- Keep functionality working throughout

Use /refactor skill for systematic cleanup.
```

## Template 10: Analysis Request

```
Analyze {subject} with focus on {aspect}.

Analysis type:
- [ ] Code quality
- [ ] Architecture
- [ ] Performance
- [ ] Security
- [ ] Workflow optimization

Scope:
- Files/directories to include
- Depth of analysis
- Output format preference

Analysis approach:
1. Use appropriate specialist agent
2. Gather relevant data
3. Apply domain-specific heuristics
4. Generate actionable findings

Output:
- Executive summary
- Detailed findings
- Recommendations prioritized by impact
- File:line references for issues
```

## Template 11: Parallel Execution

```
Execute the following operations in parallel (no dependencies):

Operation 1: {description}
- Tool: {tool_name}
- Target: {file/path}

Operation 2: {description}
- Tool: {tool_name}
- Target: {file/path}

Operation 3: {description}
- Tool: {tool_name}
- Target: {file/path}

After all complete:
- Aggregate results
- Check for conflicts
- Provide unified output
```

## Template 12: Interactive Planning

```
Help me plan {task}.

I need to clarify:
1. What is the primary goal?
2. What are the constraints?
3. What are the edge cases to consider?

Options I'm considering:
- Option A: {description} - {pros/cons}
- Option B: {description} - {pros/cons}

Use AskUserQuestion to help me decide on unclear aspects.
```

## Usage Guidelines

### When to use templates
- For common, repeatable tasks
- When task structure is predictable
- To ensure consistent quality

### When NOT to use templates
- Highly novel situations
- Tasks requiring creativity
- When template doesn't fit

### Customization
- Replace {placeholders} with specific values
- Adjust steps based on context
- Add/remove steps as needed
- Keep core structure intact

### Template maintenance
- Update templates based on learnings
- Add new templates for discovered patterns
- Remove unused templates
- Share effective templates with team
