# Command Reference

> **Common commands for Week 2 development**

## Testing Commands

### Run Tests

```bash
# Run all tests
poetry run pytest week2/tests/

# Run with verbose output
poetry run pytest week2/tests/ -v

# Run fast tests only (skip slow LLM tests)
poetry run pytest week2/tests/ -m "not slow"

# Run only slow tests (real LLM integration)
poetry run pytest week2/tests/ -m "slow"

# Run specific test file
poetry run pytest week2/tests/test_extract.py

# Run specific test function
poetry run pytest week2/tests/test_extract.py::test_extract_bullets

# Show print output
poetry run pytest week2/tests/ -s
```

### Coverage

```bash
# Generate coverage report
poetry run pytest week2/tests/ --cov=week2/app --cov-report=html

# Coverage in terminal
poetry run pytest week2/tests/ --cov=week2/app --cov-report=term-missing
```

## Server Commands

### Start Development Server

```bash
# Basic start
poetry run uvicorn week2.app.main:app --reload

# Custom port
poetry run uvicorn week2.app.main:app --reload --port 8080

# Custom host
poetry run uvicorn week2.app.main:app --reload --host 0.0.0.0
```

### Production Server

```bash
# Without reload
poetry run uvicorn week2.app.main:app --host 0.0.0.0 --port 8000

# Multiple workers
poetry run uvicorn week2.app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Ollama Commands

### Start Ollama

```bash
# Start Ollama service
ollama serve

# Pull model
ollama pull llama3.1:8b

# List models
ollama list

# Show model info
ollama show llama3.1:8b

# Run model interactively
ollama run llama3.1:8b
```

### Test Ollama

```bash
# Quick test
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Hello, world!"
}'
```

## Poetry Commands

### Package Management

```bash
# Install dependencies
poetry install

# Add dependency
poetry add fastapi

# Add dev dependency
poetry add --group dev pytest

# Update dependencies
poetry update

# Show dependencies
poetry show

# Show dependency tree
poetry show --tree
```

### Running Commands

```bash
# Run command in poetry environment
poetry run pytest
poetry run uvicorn
poetry run python

# Activate shell
poetry shell
```

## Git Commands

### Common Operations

```bash
# Status
git status

# Add files
git add .
git add path/to/file

# Commit
git commit -m "message"

# Push
git push

# Pull
git pull

# Create branch
git checkout -b feature-name

# Switch branch
git checkout existing-branch

# Merge branch
git merge feature-name
```

### Pre-commit

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Run pre-commit manually
poetry run pre-commit run --all-files

# Update hooks
poetry run pre-commit autoupdate
```

## Code Quality Commands

### Formatting

```bash
# Format with Black
poetry run black week2/

# Check formatting
poetry run black --check week2/

# Format specific file
poetry run black week2/app/main.py
```

### Linting

```bash
# Run Ruff linter
poetry run ruff check week2/

# Fix auto-fixable issues
poetry run ruff check --fix week2/

# Specific file
poetry run ruff check week2/app/main.py
```

### Type Checking

```bash
# Run mypy (if configured)
poetry run mypy week2/app/

# Ignore specific errors
poetry run mypy week2/app/ --ignore-missing-imports
```

## Database Commands

### SQLite Operations

```bash
# Open database
sqlite3 week2/database.db

# Common SQL commands
.tables          # List tables
.schema          # Show schema
.schema notes    # Show specific table schema
SELECT * FROM notes;  # Query data
.quit            # Exit
```

### Backup

```bash
# Backup database
cp week2/database.db week2/database.backup.db

# Dump to SQL
sqlite3 week2/database.db .dump > backup.sql
```

## System Commands

### Check Processes

```bash
# Check if server is running
lsof -i :8000

# Kill process on port
kill -9 <PID>

# Find Python processes
ps aux | grep python
```

### Environment

```bash
# Show Python version
poetry run python --version

# Show installed packages
poetry run pip list

# Check Python path
poetry run python -c "import sys; print(sys.path)"
```

## Troubleshooting Commands

### Import Issues

```bash
# Check sys.path
poetry run python -c "import sys; print('\n'.join(sys.path))"

# Test import
poetry run python -c "from week2.app.main import app; print('OK')"

# Run module as script
poetry run python -m week2.app.main
```

### Database Issues

```bash
# Check database file
ls -la week2/database.db

# Check database integrity
sqlite3 week2/database.db "PRAGMA integrity_check;"

# Reset database (caution!)
rm week2/database.db
poetry run python -c "from week2.app.database import init_db; init_db()"
```

### Ollama Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve
```

## API Testing Commands

### Using curl

```bash
# Test extract endpoint
curl -X POST http://127.0.0.1:8000/action-items/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "- Task 1\n- Task 2", "save_note": false}'

# Test list endpoint
curl http://127.0.0.1:8000/action-items

# Test note endpoint
curl http://127.0.0.1:8000/notes/1
```

### Using HTTPie (friendlier)

```bash
# POST request
http POST localhost:8000/action-items/extract \
  text="- Task 1" \
  save_note:=false

# GET request
http GET localhost:8000/action-items
```

## Quick Reference Card

```bash
# === Development Loop ===
# 1. Run tests
poetry run pytest week2/tests/ -m "not slow"

# 2. Start server
poetry run uvicorn week2.app.main:app --reload

# 3. Check code quality
poetry run black week2/ && poetry run ruff check week2/

# === Common Tasks ===
# Add dependency:     poetry add package-name
# Run tests:          poetry run pytest
# Start server:       poetry run uvicorn week2.app.main:app --reload
# Start Ollama:       ollama serve
# Format code:        poetry run black week2/
# Check lint:         poetry run ruff check week2/
```

## Related Files

- Troubleshooting: `reference/troubleshooting.md`
- Code patterns: `reference/code_patterns.md`
