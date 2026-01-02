# Week 2 Learning Notes

> **Modern Software Developer (CS146S)**
> Topics: LLM Integration, Testing Patterns, Code Refactoring, Exception Handling

---

## Directory Structure

```
week2/
├── fundamentals/          # Core concepts and architecture
│   ├── 00_overview.md
│   ├── 01_architecture.md
│   ├── 02_llm_basics.md
│   └── 03_testing_concepts.md
├── practice/             # Practical guides and patterns
│   ├── llm_integration.md      # LLM integration with structured output
│   ├── testing_patterns.md     # Testing LLM functions (Mock, pytest)
│   ├── refactoring_journey.md  # Code refactoring best practices
│   └── exception_handling.md   # Exception design with Claude Code
├── reference/            # Quick reference materials
│   ├── code_patterns.md        # Common code patterns
│   ├── command_reference.md    # CLI commands reference
│   ├── imports_guide.md        # Python import system guide
│   └── troubleshooting.md      # Common issues and solutions
└── _archive/             # Original learning summary (archived)
    └── WEEK2_LEARNING_SUMMARY.md
```

---

## Quick Start

### For Learning Fundamentals
Start with `fundamentals/` to understand the core concepts:
1. **00_overview.md** - Week 2 project overview
2. **01_architecture.md** - FastAPI + SQLite architecture
3. **02_llm_basics.md** - LLM integration fundamentals
4. **03_testing_concepts.md** - Testing pyramid and strategies

### For Implementation Practice
Use `practice/` guides when working on the code:
- **llm_integration.md** - Implementing LLM extraction
- **testing_patterns.md** - Writing tests with Mock and pytest
- **refactoring_journey.md** - Refactoring for maintainability
- **exception_handling.md** - Designing robust exceptions

### For Quick Reference
Check `reference/` for specific information:
- **code_patterns.md** - Pydantic, routing, database patterns
- **command_reference.md** - Testing, server, Ollama commands
- **imports_guide.md** - Python import system
- **troubleshooting.md** - Common issues and fixes

---

## Key Topics

### LLM Integration
- **Structured Output**: Using JSON Schema with Ollama
- **Temperature Tuning**: Balancing creativity vs consistency
- **System Prompts**: Designing effective prompts
- **Post-Processing**: Cleaning, deduplicating, validating
- **Error Handling**: Graceful degradation when API fails

### Testing Patterns
- **Mock Strategy**: 70% fast unit tests with Mock
- **Integration Tests**: 20% real LLM tests for confidence
- **Semantic Assertions**: Allowing LLM output variation
- **Pytest Marks**: Organizing slow vs fast tests

### Code Refactoring
- **Pydantic Schemas**: Type-safe request/response models
- **Layered Architecture**: Router, Service, Database separation
- **Factory Methods**: Eliminating repetitive construction
- **Database Abstraction**: Returning dict, not Row

### Exception Handling
- **Context-Rich Exceptions**: Carrying resource type, ID
- **Global Handlers**: Centralized error responses
- **Graceful Degradation**: Returning [] instead of crashing

---

## Common Workflows

### Running Tests
```bash
# Fast tests (development)
poetry run pytest week2/tests/ -m "not slow"

# All tests (before commit)
poetry run pytest week2/tests/

# With coverage
poetry run pytest week2/tests/ --cov=week2/app --cov-report=html
```

### Starting Services
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start FastAPI server
poetry run uvicorn week2.app.main:app --reload
```

### Code Quality
```bash
# Format code
poetry run black week2/

# Check linting
poetry run ruff check week2/

# Run pre-commit
poetry run pre-commit run --all-files
```

---

## Learning Path

### Step 1: Understand Fundamentals
Read `fundamentals/` files to grasp the architecture and concepts.

### Step 2: Practice Implementation
Follow `practice/` guides to implement features:
1. Read `llm_integration.md` before implementing extract functions
2. Reference `testing_patterns.md` when writing tests
3. Use `refactoring_journey.md` as a refactoring guide
4. Study `exception_handling.md` for error handling patterns

### Step 3: Reference During Development
Use `reference/` files as quick lookup:
- `code_patterns.md` for code snippets
- `command_reference.md` for commands
- `imports_guide.md` for import issues
- `troubleshooting.md` when stuck

---

## Related Files

- **Project README**: `week2/README.md`
- **Assignment**: `week2/assignment.md`
- **Code**: `week2/app/`
- **Tests**: `week2/tests/`

---

## File Summary

| File | Purpose | When to Use |
|------|---------|-------------|
| `fundamentals/00_overview.md` | Project overview | First time learning |
| `fundamentals/01_architecture.md` | Architecture design | Understanding structure |
| `fundamentals/02_llm_basics.md` | LLM concepts | Before using LLM |
| `fundamentals/03_testing_concepts.md` | Testing fundamentals | Before writing tests |
| `practice/llm_integration.md` | LLM implementation | Implementing extraction |
| `practice/testing_patterns.md` | Testing guide | Writing tests |
| `practice/refactoring_journey.md` | Refactoring guide | Improving code quality |
| `practice/exception_handling.md` | Exception design | Adding error handling |
| `reference/code_patterns.md` | Code snippets | Need pattern example |
| `reference/command_reference.md` | CLI commands | Running tests/server |
| `reference/imports_guide.md` | Import system | Fixing import errors |
| `reference/troubleshooting.md` | Issue resolution | Debugging problems |

---

*Week 2 - Modern Software Developer (CS146S)*
*Date: 2025-12-28*
