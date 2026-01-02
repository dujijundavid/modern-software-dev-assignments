# Week 5

Minimal full‑stack starter for experimenting with autonomous coding agents.

- FastAPI backend with SQLite (SQLAlchemy)
- Static frontend (no Node toolchain needed)
- Minimal tests (pytest)
- Pre-commit (black + ruff)
- Tasks to practice agent-driven workflows

## Quickstart

### 1) Environment Setup (First time only)

**Option A: Using Conda (Recommended)**

```bash
# Activate conda environment (with auto-initialization)
conda activate cs146s

# OR if conda is not initialized yet:
source ~/miniconda3/etc/profile.d/conda.sh && conda activate cs146s

# Install dependencies
poetry install
```

**Option B: Quick Setup Script**

```bash
# From project root
source scripts/setup_env.sh
```

### 2) Verify Environment

```bash
# Check environment health
python scripts/env_check.py

# Run tests
cd week5 && make test
```

### 3) Run the App

```bash
cd week5 && make run
```

**Note**: The server runs with **auto-reload** enabled. Changes to Python files will automatically restart the server.

**Important**: If you see `Address already in use` error, kill the existing process:

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

Then try `make run` again.

---

### Access Points

- **Frontend**: http://localhost:8000
- **API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

## Structure

```
backend/                # FastAPI app
frontend/               # Static UI served by FastAPI
data/                   # SQLite DB + seed
docs/                   # TASKS for agent-driven workflows
```

## Tests

```bash
cd week5 && make test
```

Run specific test file:
```bash
cd week5 && PYTHONPATH=. poetry run pytest backend/tests/test_notes.py -v
```

Run with coverage:
```bash
cd week5 && PYTHONPATH=. poetry run pytest --cov=backend --cov-report=html
```

## Formatting/Linting

```bash
cd week5 && make format   # Run black and ruff --fix
cd week5 && make lint     # Run ruff check only
```

## Development Workflow

### Typical Session

```bash
# 1. Activate environment
conda activate cs146s

# 2. Check environment health
python scripts/env_check.py

# 3. Run tests
cd week5 && make test

# 4. Start server (with auto-reload)
cd week5 && make run

# 5. Edit code - server auto-reloads on Python file changes

# 6. When done: Ctrl+C to stop server
```

### Server Auto-Reload

The `make run` command uses `--reload` flag, which means:
- ✅ Changes to `.py` files → automatic server restart
- ✅ Changes to `frontend/` files → automatic refresh (no restart needed)
- ⚠️  Changes to database schema → manual restart required

### Troubleshooting

**Problem**: `Address already in use` error
```bash
# Solution: Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Problem**: Tests fail with import errors
```bash
# Solution: Make sure PYTHONPATH is set
cd week5 && PYTHONPATH=. poetry run pytest
```

**Problem**: Poetry not found
```bash
# Solution: Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
# Or run: source scripts/setup_env.sh
```

**Problem**: Wrong Python version
```bash
# Solution: Activate conda environment
conda activate cs146s
python --version  # Should show 3.12.x
```

## Configuration

Copy `.env.example` to `.env` (in `week5/`) to override defaults like the database path.

Example `.env` file:
```bash
# Database
DATABASE_PATH=sqlite:///./data/app.db

# Server
HOST=127.0.0.1
PORT=8000

# Other settings...
```

## Available Make Targets

```bash
make run     # Start development server with auto-reload
make test    # Run all tests
make format  # Format code with black and ruff
make lint    # Check code quality with ruff
make seed    # Seed the database with sample data
```

## Project Structure

```
week5/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app entry point
│   │   ├── db.py            # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── routers/         # API route handlers
│   └── tests/               # Backend tests
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── app.js               # Frontend JavaScript
│   └── styles.css           # CSS styles
├── data/
│   └── app.db               # SQLite database
├── docs/
│   └── TASKS.md             # Available tasks for automation
├── Makefile                 # Convenient make targets
└── README.md                # This file
```

## Week 5 Assignment Focus

This week emphasizes **Agentic Development with Warp**:
- Build automations using Warp Drive (saved prompts, rules, MCP servers)
- Implement multi-agent workflows
- Create reusable development tools
- Document your automation journey

See `week5_assignment.md` for full assignment details.

## 📚 Documentation

For detailed documentation on environment setup and automations, see the [docs/week5/](../docs/week5/) directory:

### Environment Setup
- [Quick Start Guide](../docs/week5/guides/quick-start.md) - Get started in 5 minutes
- [Solution Summary](../docs/week5/environment-setup/solution-summary.md) - Complete environment setup guide
- [Diagnosis Report](../docs/week5/environment-setup/diagnosis-report.md) - Detailed problem diagnosis
- [Python Analysis](../docs/week5/environment-setup/python-analysis.md) - Python version analysis

### Automations
- [Automation 1: Environment Health Check](../docs/week5/automations/automation-1-env-check.md) - First automation complete summary

### Master Index
- [Documentation Index](../docs/INDEX.md) - Complete documentation overview

