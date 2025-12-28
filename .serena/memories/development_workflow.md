# Development Workflow

Established patterns and tools for efficient development workflow.

---

## Environment Setup

### Dual-Tool Approach: Conda + Poetry

**Why Both?**
- **Conda**: Manages Python runtime environment (3.12.7)
- **Poetry**: Manages project dependencies and packaging (2.2.1)

### Initial Setup

```bash
# Create conda environment
conda create -n cs146s python=3.12.7
conda activate cs146s

# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

# Install project dependencies
cd modern-software-dev-assignments
poetry install
```

### Daily Workflow

```bash
# Activate environment
conda activate cs146s

# Verify setup
python --version  # Should show 3.12.7
poetry --version  # Should show 2.2.1
```

---

## Code Quality Tools

### Black (Code Formatter)

**Configuration (pyproject.toml):**
```toml
[tool.black]
line-length = 100
target-version = ['py312']
include = '\.pyi?$'
```

**Usage:**
```bash
# Format all code
poetry run black .

# Format specific file
poetry run black week2/app/main.py

# Check what would be formatted (dry-run)
poetry run black --check .
```

**Pre-commit Integration:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.12
```

---

### Ruff (Linter)

**Configuration (pyproject.toml):**
```toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "UP", "B"]  # Error, Flake, Import, Upgrade, Bugbear
ignore = ["E501"]  # Line too long (Black handles this)
target-version = "py312"
```

**Usage:**
```bash
# Lint all code
poetry run ruff check .

# Fix auto-fixable issues
poetry run ruff check --fix .

# Check specific file
poetry run ruff check week2/app/main.py
```

**Rule Categories:**
| Rule | Description | Example |
|------|-------------|---------|
| E | Pyflakes errors | Unused imports |
| F | Pyflakes warnings | Undefined names |
| I | Import sorting | Organize imports |
| UP | Upgrade syntax | Modern Python patterns |
| B | Bugbear | Common bugs |

---

### Pre-commit Hooks

**Installation:**
```bash
# Install pre-commit
poetry run pip install pre-commit

# Install hooks
pre-commit install
```

**Configuration (.pre-commit-config.yaml):**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "week1/app", "week2/app"]
```

**Manual Run:**
```bash
# Run all hooks on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run
```

---

## Local Development

### Starting Ollama

```bash
# Start Ollama service
ollama serve

# In another terminal, verify
ollama list

# Pull model if needed
ollama pull llama3.1:8b
```

### Running FastAPI

```bash
# Run with uvicorn (hot reload enabled)
poetry run uvicorn week2.app.main:app --reload --port 8000

# Run without reload
poetry run uvicorn week2.app.main:app --port 8000

# Run with debug logging
poetry run uvicorn week2.app.main:app --log-level debug
```

### Database Initialization

```bash
# SQLite database auto-creates on first run
# Tables created by SQLAlchemy on app startup

# To reset database
rm week2/database.db
poetry run uvicorn week2.app.main:app
```

---

## Debugging

### Log Level Adjustment

```python
import logging

# Set in code
logging.basicConfig(level=logging.DEBUG)

# Or for FastAPI
import uvicorn
uvicorn.run(app, log_level="debug")
```

### Python Debugger (pdb)

```python
import pdb; pdb.set_trace()  # Set breakpoint

# Or use ipdb (better)
import ipdb; ipdb.set_trace()
```

### FastAPI Auto-Docs

```
# Interactive API documentation
http://localhost:8000/docs    # Swagger UI
http://localhost:8000/redoc   # ReDoc
```

---

## Git Workflow

### Commit Message Convention

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `docs`: Documentation changes
- `test`: Test additions/changes
- `chore`: Maintenance tasks

**Examples:**
```
feat(week2): add LLM action item extraction endpoint

Implement POST /notes/{id}/extract that uses Ollama to extract
action items from note content. Includes error handling and
input validation.

Closes #42
```

```
fix(db): resolve SQLite locking in concurrent tests

Use separate in-memory databases for each test fixture to
prevent locking issues.
```

### Branch Strategy

```
master (main)
  ↑
  └── week2-llm-integration (feature branch)
        ↑
        └── extract-endpoint (sub-feature)
```

### Pull Request Process

```bash
# 1. Create feature branch
git checkout -b week2-llm-integration

# 2. Make changes and commit
git add .
git commit -m "feat(week2): add extraction endpoint"

# 3. Push and create PR
git push origin week2-llm-integration
# Create PR on GitHub

# 4. After review and merge
git checkout master
git pull origin master
git branch -d week2-llm-integration
```

---

## Testing Workflow

### During Development

```bash
# Run unit tests only (fast)
pytest -m "not slow" -q

# Run tests for current week
pytest week2/tests/ -v

# Run with coverage
pytest week2/tests/ --cov=week2/app --cov-report=term-missing
```

### Before Committing

```bash
# Run all tests
pytest -v

# Run pre-commit hooks
pre-commit run --all-files

# Format code
poetry run black .
poetry run ruff check --fix .
```

### Continuous Integration

```yaml
# .github/workflows/test.yml (example)
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install poetry
      - run: poetry install
      - run: pytest --cov
```

---

## AI Agent Workflow

### Recommended Sequence

```
1. @code-archaeologist
   ↓ Explore unfamiliar code
   
2. @fastapi-expert or @python-expert
   ↓ Design and implement
   
3. @python-testing-expert
   ↓ Add/improve tests
   
4. @code-reviewer
   ↓ Review before commit (ALWAYS!)
   
5. Commit
```

### Example Commands

```
# Exploration
"Use @code-archaeologist to analyze the database layer in week2/app/db.py"

# Implementation
"Use @fastapi-expert to add a DELETE endpoint for notes with proper error handling"

# Testing
"Use @python-testing-expert to improve test coverage for the extraction service"

# Review
"Use @code-reviewer to review the week2 changes before committing"
```

---

## Common Tasks

### Adding a New Endpoint

```bash
# 1. Create route handler
# week2/app/routers/notes.py

# 2. Add business logic
# week2/app/services/notes.py

# 3. Add tests
# week2/tests/test_routes.py

# 4. Run tests
pytest week2/tests/ -v

# 5. Format and lint
poetry run black .
poetry run ruff check --fix .

# 6. Commit
git add .
git commit -m "feat(week2): add DELETE /notes/{id} endpoint"
```

### Upgrading Dependencies

```bash
# Check what's outdated
poetry show --outdated

# Update specific package
poetry add package-name@latest

# Update all (careful!)
poetry update

# Check for vulnerabilities
pip-audit
```

### Database Migration

```bash
# When schema changes, create migration
# week2/app/db/migrations/002_add_completed_column.py

# Run migration
poetry run python -m week2.app.db.migrate
```

---

## Deployment Considerations

### Environment Variables

```bash
# Production .env (don't commit)
DATABASE_URL=postgresql://user:pass@host/db
OLLAMA_BASE_URL=http://ollama:11434
LOG_LEVEL=INFO
```

### Production vs Development

```python
import os

if os.getenv("ENVIRONMENT") == "production":
    # Production settings
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    LOG_LEVEL = "INFO"
else:
    # Development settings
    DEBUG = True
    DATABASE_URL = "sqlite:///database.db"
    LOG_LEVEL = "DEBUG"
```

---

## Keyboard Shortcuts (VS Code)

| Action | Shortcut |
|--------|----------|
| Command Palette | Cmd+Shift+P |
| Format document | Shift+Opt+F |
| Go to file | Cmd+P |
| Find in files | Cmd+Shift+F |
| Toggle terminal | Cmd+J |
| Split editor | Cmd+\ |

---

## Quick Reference

```bash
# Daily commands
conda activate cs146s              # Activate environment
poetry run uvicorn main:app --reload  # Start server
pytest -m "not slow" -q           # Run tests
poetry run black .                # Format code
poetry run ruff check --fix .     # Lint code

# Commit workflow
pre-commit run --all-files        # Run hooks
git add .                         # Stage changes
git commit -m "type(scope): msg"  # Commit
git push                          # Push to remote

# AI agents
@code-archaeologist              # Explore code
@fastapi-expert                  # FastAPI tasks
@python-testing-expert           # Testing tasks
@code-reviewer                   # Review before commit
```
