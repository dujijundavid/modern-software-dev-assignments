---
description: "Comprehensive PR review following CS146S course standards"
parameters:
  - name: pr_number
    description: "The PR number to review. If not provided, will detect from current branch."
    required: false
  - name: review_depth
    description: "Review depth: 'quick' (files changed only), 'standard' (full review), 'thorough' (with execution)"
    required: false
---

Perform a comprehensive Pull Request review following the CS146S Modern Software Developer course standards.

## When invoked:

1. **PR Identification**
   - If `pr_number` is provided, fetch that PR using `gh pr view {{ pr_number }}`
   - If not provided, detect PR from current branch: `gh pr view --web`
   - If no PR exists, prompt user to create one or review commits instead

2. **Context Gathering**
   - Get PR diff: `gh pr diff {{ pr_number }}`
   - Get commit messages: `gh pr view {{ pr_number }} --json commits`
   - Get changed files: `gh pr diff {{ pr_number }} --name-only`
   - Identify which week(s) are affected by the changes

3. **Review Execution**

   For **quick** reviews:
   - Check file organization and naming
   - Verify basic code style (Black, Ruff)
   - Check for obvious security issues

   For **standard** reviews (default):
   - Run all checks from quick review
   - Verify business logic correctness
   - Check error handling
   - Review test coverage and quality
   - Verify database changes are safe
   - Check API contract compliance

   For **thorough** reviews:
   - Run all checks from standard review
   - Execute the affected week's tests: `pytest week{{ N }}/tests/ -v`
   - Run code reviewer agent on changed files
   - Check for performance issues if relevant
   - Verify integration points

4. **Review Categories**

   Always check:
   - **Security**: SQL injection, XSS, auth bypass, sensitive data exposure
   - **Correctness**: Logic bugs, edge cases, error conditions
   - **Testing**: Coverage, test quality, missing test cases
   - **Style**: Black formatting, Ruff linting, naming conventions
   - **Documentation**: Docstrings, API docs, CLAUDE.md updates if needed
   - **Week-specific**: Each week has different focus areas

5. **Output Format**

   Present review as a structured report:

   ```markdown
   # PR Review: #{{ pr_number }} - {{ title }}

   ## Summary
   [Brief overview of changes and overall assessment]

   ## Files Changed
   [List of affected files with link references]

   ## Findings

   ### Critical Issues (Must Fix)
   - [ ] [issue description]

   ### Suggestions (Should Fix)
   - [ ] [suggestion]

   ### Nice to Have
   - [ ] [minor improvement]

   ## Test Results
   [Test execution summary]

   ## Week-Specific Notes
   [Any notes relevant to the specific week's learning objectives]

   ## Approval Decision
   [Approve / Request Changes / Comment]
   ```

6. **Actions**
   - If critical issues found: Use `gh pr review {{ pr_number }} --request-changes`
   - If suggestions only: Use `gh pr review {{ pr_number }} --comment`
   - If ready to merge: Ask user for confirmation before approving

## Key Review Checks by Week

| Week | Focus Areas |
|------|-------------|
| Week 1 | Prompt quality, CoT structure, RAG retrieval |
| Week 2 | LLM integration, FastAPI patterns, error handling |
| Week 3 | MCP server tools, transport, error handling |
| Week 4 | Command clarity, reusability, documentation |
| Week 5 | Agent coordination, task breakdown |
| Week 6 | Semgrep rules, security patterns |
| Week 7 | Graphite Diamond integration, review quality |
| Week 8 | Multi-stack consistency, cross-platform issues |

## Integration with Existing Commands

This command internally uses:
- `/test-week` for test execution
- `/refactor` for code quality suggestions
- The `code-reviewer` subagent for automated analysis

## Notes

- Always run tests before approving if tests are affected
- Be constructive and educational - this is a learning environment
- Reference course materials when suggesting improvements
- Consider the week's learning objectives when reviewing
