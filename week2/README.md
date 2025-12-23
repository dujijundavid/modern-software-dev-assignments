# Action Item Extractor

A FastAPI application that extracts actionable items from meeting notes using both rule-based pattern matching and LLM-powered semantic understanding.

## Features

- **Dual Extraction Methods**
  - **Rules-based**: Fast extraction using regex patterns for bullets, checkboxes, and keywords
  - **LLM-powered**: Intelligent extraction using Ollama's llama3.1:8b model with semantic understanding

- **Notes Management**
  - Save and retrieve notes
  - Automatic linking of action items to their source notes
  - List all saved notes with timestamps

- **Action Item Tracking**
  - Mark items as done/undone
  - Persistent storage with SQLite
  - Real-time status updates via frontend UI

- **Type Safety & Validation**
  - Pydantic schemas for all API contracts
  - Automatic request/response validation
  - Custom error handling with proper HTTP status codes

## Tech Stack

- **Backend**: FastAPI 0.115+ with Python 3.12+
- **Database**: SQLite with custom error handling
- **LLM**: Ollama with llama3.1:8b model
- **Validation**: Pydantic v2
- **Testing**: pytest with mock and integration tests

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI app with exception handlers
│   ├── db.py                # Database layer with custom exceptions
│   ├── schemas.py           # Pydantic models for validation
│   ├── routers/
│   │   ├── notes.py         # Notes endpoints
│   │   └── action_items.py  # Action items endpoints
│   └── services/
│       └── extract.py       # Extraction logic (rules + LLM)
├── frontend/
│   └── index.html           # Web UI
├── tests/
│   ├── test_extract.py      # Extraction tests
│   └── test_refactoring.py  # Refactoring validation tests
├── data/
│   └── app.db               # SQLite database (auto-created)
├── assignment.md            # Assignment requirements
├── writeup.md               # Assignment write-up
└── README.md                # This file
```

## Setup

### Prerequisites

- Python 3.12 or higher
- Ollama installed and running
- llama3.1:8b model pulled

### Installation

1. **Install Ollama** (if not already installed)
   ```bash
   # macOS
   brew install ollama

   # Linux
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Start Ollama and pull the model**
   ```bash
   ollama serve  # In one terminal
   ollama pull llama3.1:8b  # In another terminal
   ```

3. **Install Python dependencies**
   ```bash
   cd /path/to/modern-software-dev-assignments
   pip install -e .
   ```

4. **Initialize the database**
   ```bash
   python -c "from week2.app import db; db.init_db()"
   ```

## Usage

### Starting the Server

```bash
# From the project root
python -m uvicorn week2.app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend UI

Open `http://localhost:8000/` in your browser to access the web interface.

**Features:**
- Paste meeting notes into the text area
- Choose extraction method: "Extract (Rules)" or "Extract (LLM)"
- Optionally save the original text as a note
- Click checkboxes to mark items as done
- Use "List Notes" to view all saved notes

### API Endpoints

#### Action Items

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/action-items/extract` | Extract using rules-based patterns |
| POST | `/action-items/extract-llm` | Extract using LLM intelligence |
| GET | `/action-items` | List all action items |
| POST | `/action-items/{id}/done` | Mark item as done/undone |

**Extract Request Body:**
```json
{
  "text": "- Prepare slides\n- [ ] Review code",
  "save_note": true
}
```

**Extract Response:**
```json
{
  "note_id": 1,
  "items": [
    {
      "id": 1,
      "text": "Prepare slides",
      "note_id": 1,
      "done": false,
      "created_at": "2025-12-23 10:00:00"
    }
  ]
}
```

#### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/notes` | Create a new note |
| GET | `/notes` | List all notes |
| GET | `/notes/{id}` | Get a single note |

**Create Note Request:**
```json
{
  "content": "Meeting notes content here"
}
```

## Running Tests

### Run All Tests
```bash
pytest week2/tests/
```

### Run Fast Tests Only (Skip LLM Integration)
```bash
pytest week2/tests/ -m "not slow"
```

### Run Only LLM Integration Tests
```bash
pytest week2/tests/ -m "slow"
```

### Test Coverage
- `test_extract.py`: 9 tests covering LLM extraction functionality
- `test_refactoring.py`: 17 tests covering refactoring improvements

## Configuration

### Ollama Settings

The application uses Ollama with the following default configuration:

- **Model**: `llama3.1:8b`
- **Endpoint**: `http://localhost:11434/api/chat`
- **Temperature**: `0.3` (for deterministic outputs)

To customize the model, pass `model="model-name"` when calling `extract_action_items_llm()`.

### Database

- **Location**: `week2/data/app.db`
- **Auto-created** on first run
- **Schema**: See `db.py:init_db()` for table definitions

## Extraction Patterns

### Rules-Based Extraction

The rules-based extractor recognizes:
- Bullet points: `- Task`, `* Task`
- Checkboxes: `- [ ] Task`, `- [x] Task`
- Keywords: `todo: Task`, `action: Task`, `Task (action item)`

### LLM Extraction

The LLM extractor:
- Understands semantic meaning of action items
- Filters out greetings, context, and descriptive statements
- Removes formatting markers automatically
- Deduplicates similar items
- Handles unstructured text intelligently

## Error Handling

The application uses custom exceptions:

- `DatabaseError`: Wrapped sqlite3 errors (HTTP 500)
- `NotFoundError`: Resource not found (HTTP 404)

All errors return JSON responses with descriptive messages.
