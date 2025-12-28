# Action Item Extractor

> A FastAPI application that extracts actionable items from meeting notes using both rule-based pattern matching and LLM-powered semantic understanding.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Quick Start

Get the app running in under 5 minutes:

```bash
# 1. Install dependencies (from project root)
pip install -e .

# 2. Start Ollama (in a separate terminal)
ollama serve
ollama pull llama3.1:8b

# 3. Initialize database
python -c "from week2.app import db; db.init_db()"

# 4. Start the server
python -m uvicorn week2.app.main:app --reload --port 8000

# 5. Open browser
open http://localhost:8000
```

**That's it!** You can now paste meeting notes and extract action items.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Detailed Setup](#detailed-setup)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

---

## Features

### Dual Extraction Methods

| Method | Technology | Best For | Speed | Accuracy |
|--------|-----------|----------|-------|----------|
| **Rules-based** | Regex patterns | Structured notes with bullets, checkboxes | ⚡ Instant | 70-80% |
| **LLM-powered** | Ollama llama3.1:8b | Unstructured, conversational text | 🐢 2-3s | 85-95% |

#### Rules-Based Patterns
```
- Bullet points:    "- Task", "* Task"
- Checkboxes:       "- [ ] Task", "- [x] Task"
- Keywords:         "todo: Task", "action: Task", "Task (action item)"
```

#### LLM Intelligence
- Understands semantic meaning of action items
- Filters out greetings, context, and descriptive statements
- Removes formatting markers automatically
- Deduplicates similar items
- Handles unstructured text intelligently

### Notes Management

```
┌─────────────────────────────────────────────────────────┐
│                    Notes Lifecycle                       │
├─────────────────────────────────────────────────────────┤
│  1. Paste meeting notes → Extract action items          │
│  2. Save original text → Linked to extracted items      │
│  3. Mark items done → Status updates in real-time       │
│  4. List all notes → View history with timestamps       │
└─────────────────────────────────────────────────────────┘
```

### Type Safety & Validation

- **Pydantic v2** schemas for all API contracts
- Automatic request/response validation
- Custom error handling with proper HTTP status codes
- Full type hints throughout codebase

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Frontend Layer                             │
│                         (static/index.html)                              │
│                      Web UI for user interaction                         │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ HTTP/JSON
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              API Layer                                   │
│                         (FastAPI Application)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  main.py                    # App setup, exception handlers, CORS  │ │
│  │  db.py                      # SQLite layer, custom errors           │ │
│  │  schemas.py                 # Pydantic models (request/response)    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────┬─────────────────────────────────┐│
│  │  routers/notes.py                 │  routers/action_items.py        ││
│  │  - POST /notes                    │  - POST /action-items/extract    ││
│  │  - GET  /notes                    │  - POST /action-items/extract-llm││
│  │  - GET  /notes/{id}               │  - GET  /action-items           ││
│  │                                    │  - POST /action-items/{id}/done ││
│  └───────────────────────────────────┴─────────────────────────────────┘│
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  services/extract.py                                               │ │
│  │  - extract_action_items()       # Rules-based extraction            │ │
│  │  - extract_action_items_llm()   # LLM-powered extraction            │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │                    │
                                     ▼                    ▼
┌─────────────────────────────────┐  ┌─────────────────────────────────┐
│      SQLite Database             │  │         Ollama LLM              │
│      (data/app.db)               │  │    (localhost:11434)            │
│  - notes table                   │  │  - llama3.1:8b model            │
│  - action_items table            │  │  - JSON mode output             │
└─────────────────────────────────┘  └─────────────────────────────────┘
```

---

## Project Structure

```
week2/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app with exception handlers
│   ├── db.py                   # Database layer with custom exceptions
│   ├── schemas.py              # Pydantic models for validation
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── notes.py            # Notes CRUD endpoints
│   │   └── action_items.py     # Action items endpoints
│   └── services/
│       ├── __init__.py
│       └── extract.py          # Extraction logic (rules + LLM)
│
├── frontend/
│   └── index.html              # Web UI
│
├── tests/
│   ├── __init__.py
│   ├── test_extract.py         # Extraction tests (9 tests)
│   ├── test_refactoring.py     # Refactoring validation tests (17 tests)
│   └── manual/                 # Manual testing scripts
│       ├── manual_filter.py
│       └── manual_llm.py
│
├── data/
│   └── app.db                  # SQLite database (auto-created)
│
├── assignment.md               # Assignment requirements
├── writeup.md                  # Assignment write-up
└── README.md                   # This file
```

---

## Detailed Setup

### Prerequisites Checklist

- [ ] Python 3.12 or higher installed
- [ ] pip or poetry for package management
- [ ] Ollama installed
- [ ] At least 2GB RAM available for LLM

### Step 1: Install Ollama

<details>
<summary><b>macOS</b> (click to expand)</summary>

```bash
brew install ollama
```

</details>

<details>
<summary><b>Linux</b> (click to expand)</summary>

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

</details>

<details>
<summary><b>Windows</b> (click to expand)</summary>

Download from [ollama.com](https://ollama.com) and run the installer.

</details>

### Step 2: Start Ollama and Pull Model

```bash
# Terminal 1: Start Ollama server
ollama serve

# Terminal 2: Pull the model (one-time setup)
ollama pull llama3.1:8b

# Verify installation
ollama list
# Should show: llama3.1:8b
```

### Step 3: Install Python Dependencies

```bash
# From project root
cd /path/to/modern-software-dev-assignments

# Install in editable mode
pip install -e .

# Or using poetry
poetry install
```

**Dependencies installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `ollama` - LLM client
- `pytest` - Testing framework

### Step 4: Initialize Database

```bash
python -c "from week2.app import db; db.init_db()"
```

This creates `week2/data/app.db` with two tables:
- `notes` - Stores original meeting notes
- `action_items` - Stores extracted action items

---

## Usage

### Starting the Server

```bash
# Development mode with auto-reload
python -m uvicorn week2.app.main:app --reload --port 8000

# Production mode
python -m uvicorn week2.app.main:app --port 8000 --workers 4
```

**Server endpoints:**
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs` (interactive Swagger UI)
- Frontend: `http://localhost:8000/`

### Using the Web UI

1. **Open** `http://localhost:8000/` in your browser
2. **Paste** meeting notes into the text area
3. **Choose** extraction method:
   - "Extract (Rules)" - Fast, pattern-based
   - "Extract (LLM)" - Smarter, semantic understanding
4. **Optional:** Check "Save note" to store original text
5. **Click** the extract button
6. **Manage:** Click checkboxes to mark items as done
7. **List:** Use "List Notes" to view all saved notes

### Example Meeting Notes

Try these examples to test the app:

**Structured Notes (Rules-based):**
```
Project Sync Meeting - Dec 23

- Prepare Q1 presentation slides
- [ ] Review pull request #123
- [ ] Update API documentation
- Schedule follow-up with design team

action: Fix the login bug
todo: Deploy to staging environment
```

**Unstructured Notes (LLM):**
```
Hey team, thanks for joining today. We discussed the roadmap and
decided to move forward with the new feature. John will handle the
backend implementation while Sarah works on the UI components.
Don't forget to update the test cases before Friday. Also, someone
needs to schedule the demo with stakeholders.
```

---

## API Documentation

### Action Items Endpoints

#### 1. Extract (Rules-based)

```http
POST /action-items/extract
Content-Type: application/json

{
  "text": "- Prepare slides\n- Review code",
  "save_note": true
}
```

**Response:**
```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Prepare slides",
      "note_id": 1,
      "done": false,
      "created_at": "2025-12-23T10:00:00"
    },
    {
      "id": 2,
      "text": "Review code",
      "note_id": 1,
      "done": false,
      "created_at": "2025-12-23T10:00:00"
    }
  ]
}
```

#### 2. Extract (LLM-powered)

```http
POST /action-items/extract-llm
Content-Type: application/json

{
  "text": "Meeting notes here...",
  "save_note": false,
  "model": "llama3.1:8b"
}
```

**Response:** Same as rules-based

#### 3. List All Action Items

```http
GET /action-items
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "text": "Prepare slides",
      "note_id": 1,
      "done": false,
      "created_at": "2025-12-23T10:00:00"
    }
  ]
}
```

#### 4. Toggle Done Status

```http
POST /action-items/{id}/done
Content-Type: application/json

{
  "done": true
}
```

**Response:**
```json
{
  "id": 1,
  "text": "Prepare slides",
  "note_id": 1,
  "done": true,
  "created_at": "2025-12-23T10:00:00"
}
```

### Notes Endpoints

#### 1. Create Note

```http
POST /notes
Content-Type: application/json

{
  "content": "Meeting notes content here"
}
```

#### 2. List All Notes

```http
GET /notes
```

#### 3. Get Single Note

```http
GET /notes/{id}
```

---

## Testing

### Test Architecture

```
Unit Tests (70%)        ← Fast, mocked, frequent
├── Mock success case
├── Post-processing logic
├── Error handling
├── Invalid JSON handling
└── Custom model support

Integration Tests (20%) ← Slow, real LLM, occasional
├── Real LLM basic extraction
└── Semantic understanding

Refactoring Tests (10%) ← Validates improvements
├── Custom error handling
├── Response format
└── Database operations
```

### Running Tests

```bash
# Run all tests (excludes slow LLM tests by default)
pytest week2/tests/

# Run fast tests only (recommended for development)
pytest week2/tests/ -m "not slow"

# Run LLM integration tests (requires Ollama running)
pytest week2/tests/ -m "slow"

# Run with coverage
pytest week2/tests/ --cov=week2/app --cov-report=html

# Run specific test file
pytest week2/tests/test_extract.py -v
```

### Manual Testing

```bash
# Manual rules-based test
python week2/tests/manual/manual_filter.py

# Manual LLM test (requires Ollama)
python week2/tests/manual/manual_llm.py
```

### Test Results

```
tests/test_extract.py ....................                               [50%]
tests/test_refactoring.py .................................             [100%]

========================= 53 passed in 1.23s =========================
```

---

## Troubleshooting

### Common Issues

<details>
<summary><b>Issue: "ModuleNotFoundError: No module named 'week2'"</b></summary>

**Cause:** Running Python files directly instead of using pytest or module syntax.

**Solutions:**
```bash
# ✅ Use pytest for tests
pytest week2/tests/

# ✅ Use module syntax for running apps
python -m week2.app.main

# ❌ Don't do this
python week2/tests/test_extract.py
```

</details>

<details>
<summary><b>Issue: "Connection refused" when calling LLM</b></summary>

**Cause:** Ollama server is not running.

**Solutions:**
```bash
# Start Ollama in a separate terminal
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags

# Check if model is pulled
ollama list
```

</details>

<details>
<summary><b>Issue: "Database is locked"</b></summary>

**Cause:** Multiple processes trying to write to SQLite simultaneously.

**Solutions:**
```bash
# Stop all running servers
# Delete the database file
rm week2/data/app.db

# Reinitialize
python -c "from week2.app import db; db.init_db()"
```

</details>

<details>
<summary><b>Issue: LLM returns "no action items found" for valid text</b></summary>

**Cause:** Model temperature too high or system prompt unclear.

**Solutions:**
```python
# In extract.py, try lowering temperature
options={'temperature': 0.1}  # More deterministic

# Or try a different model
extract_action_items_llm(text, model="llama3.2:3b")
```

</details>

<details>
<summary><b>Issue: Tests timeout when running LLM tests</b></summary>

**Cause:** LLM inference is slow (2-3 seconds per call).

**Solutions:**
```bash
# Skip slow tests during development
pytest week2/tests/ -m "not slow"

# Run LLM tests separately when needed
pytest week2/tests/ -m "slow"
```

</details>

### Debug Mode

Enable verbose logging:

```bash
# Run with debug output
python -m uvicorn week2.app.main:app --reload --log-level debug

# Run pytest with verbose output
pytest week2/tests/ -vv -s
```

---

## Development

### Adding New Features

1. **Create a new branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes and test**
   ```bash
   pytest week2/tests/ -m "not slow"
   ```

3. **Run LLM tests before committing**
   ```bash
   pytest week2/tests/ -m "slow"
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   git push origin feature/your-feature-name
   ```

### Code Style

- **Type hints:** Required for all functions
- **Docstrings:** Google style for public functions
- **Imports:** Grouped (stdlib, third-party, local)
- **Line length:** Max 100 characters

### Project-Specific Patterns

<details>
<summary><b>Error Handling Pattern</b></summary>

```python
from week2.app.db import DatabaseError, NotFoundError

@app.post("/action-items/extract")
async def extract_items(request: ExtractRequest):
    try:
        items = extract_action_items(request.text)
        return {"items": items}
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

</details>

<details>
<summary><b>Pydantic Validation Pattern</b></summary>

```python
from pydantic import BaseModel, Field

class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to extract from")
    save_note: bool = Field(default=False, description="Whether to save note")
    model: str = Field(default="llama3.1:8b", description="LLM model to use")
```

</details>

---

## Configuration

### Ollama Settings

Edit in `app/services/extract.py`:

```python
DEFAULT_OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "llama3.1:8b",
    "temperature": 0.3,  # Lower = more deterministic
    "timeout": 30,       # Seconds
}
```

### Database Settings

Edit in `app/db.py`:

```python
DATABASE_PATH = "week2/data/app.db"
```

---

## Tech Stack Details

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12+ | Runtime |
| FastAPI | 0.115+ | Web framework |
| Pydantic | 2.x | Data validation |
| Uvicorn | Latest | ASGI server |
| Ollama | Latest | LLM runtime |
| SQLite | Built-in | Database |
| pytest | Latest | Testing |

---

## License

MIT License - feel free to use this project for learning and development.

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Ollama Documentation](https://ollama.com)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [Learning Notes](../learning_notes/week2/)
