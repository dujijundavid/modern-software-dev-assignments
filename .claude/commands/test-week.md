Run and analyze tests for a specific weekly assignment.

Steps:
1. Ask which week to test if not specified
2. Navigate to that week's directory
3. Run pytest with verbose output and coverage
4. Analyze any failing tests
5. Summarize test coverage
6. If tests fail, help diagnose and fix issues

Use the Bash tool to run:
```
cd week{{ WEEK_NUMBER }} && pytest -v --cov=. --cov-report=term-missing
```

If there are test failures, analyze the output and propose fixes.
