# Week2 Codebase Learning Path for AI Engineers

This is a beginner-friendly FastAPI action item extractor app that bridges traditional software engineering with modern AI. You'll learn backend APIs, databases, LLM integration, and testing through 5 incremental exercises.

## Understanding the Current Codebase

**Architecture Flow:**
```
Frontend (HTML/JS) → FastAPI Routers → Services (Business Logic) → Database (SQLite)
```

**Key Components:**
1. [`week2/app/main.py`] - FastAPI app entry point, registers routers
2. [`week2/app/db.py`] - Database operations (notes & action_items tables)
3. [`week2/app/routers/notes.py`] - CRUD endpoints for notes
4. [`week2/app/routers/action_items.py`] - Extraction & action item management
5. [`week2/app/services/extract.py`] - `extract_action_items()` uses regex/heuristics to find action items
6. [`week2/frontend/index.html`] - Simple UI with textarea, extract button, checkboxes

**Current Extraction Logic:**
- Rule-based: detects bullets (`-`, `*`), keywords (`TODO:`, `action:`), checkboxes (`[ ]`)
- Fallback: finds imperative sentences (starts with "add", "fix", "create", etc.)
- **Your Goal:** Build LLM version using Ollama for smarter extraction

## Recommended Learning Path

**Step 1: Trace a Request End-to-End** (30 min)
- Run the app: `poetry run uvicorn week2.app.main:app --reload`
- Open browser DevTools, submit a note with "- Buy groceries"
- Follow the flow: Frontend `fetch()` → `POST /action-items/extract` → `extract_action_items()` → SQLite insert
- Visit `http://127.0.0.1:8000/docs` to see auto-generated API documentation

**Step 2: Experiment with Existing Code** (45 min)
- Modify [`extract.py`]: add new keyword like "urgent:" to `is_action_item()`
- Add `print()` statements to trace execution
- Run tests: `poetry run pytest week2/tests/` to see how testing works
- Break something intentionally (remove a bullet pattern), see how output changes

**Step 3: Study the 5 TODOs in Order** (Read assignment.md)
- **TODO 1:** Implement `extract_action_items_llm()` using Ollama - *Core AI engineering skill*
- **TODO 2:** Write unit tests for LLM function - *Learn testing non-deterministic systems*
- **TODO 3:** Refactor with Pydantic models - *Learn API best practices*
- **TODO 4:** Add new endpoints + frontend buttons - *Full-stack integration*
- **TODO 5:** Generate README with AI - *Meta-learning about AI capabilities*

**Step 4: Implement TODO 1 (LLM Integration)** (2-3 hours)
- Read [Ollama structured outputs docs](https://ollama.com/blog/structured-outputs)
- Start with small model: `ollama run llama3.2:1b`
- Create `extract_action_items_llm(text: str) -> list[str]` in [`extract.py`]
- Use Ollama's JSON schema to return `{ "action_items": ["item1", "item2"] }`
- Test manually with different note formats

**Step 5: Build Incrementally on TODOs 2-5** (4-6 hours)
- Add tests before features (TDD approach)
- Refactor one router at a time (start with `notes.py`)
- Use Cursor's agent mode for TODO 4 (learn delegation)
- Document as you go in `writeup.md`

## Further Considerations

**Learning Resources:**
- FastAPI tutorial: https://fastapi.tiangolo.com/tutorial/
- Ollama Python library docs: https://github.com/ollama/ollama-python
- Pydantic models: https://docs.pydantic.dev/latest/

**Common Beginner Pitfalls:**
- Not activating conda environment before running commands
- Forgetting to restart server after changing non-watched files
- Trying to implement all TODOs at once (work incrementally!)
- Not reading error messages in browser DevTools/terminal

**Skills You'll Develop:**
- 🐍 Python type hints, async/await patterns
- 🚀 REST API design with FastAPI
- 🤖 LLM integration with structured outputs
- 🗄️ SQLite database operations
- ✅ Unit testing strategies
- 🎨 Basic frontend-backend communication

**Time Estimate:** 8-12 hours total (2-3 hours per TODO)
