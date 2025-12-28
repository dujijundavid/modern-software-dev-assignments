# Week2 Tests

This folder contains automated tests for the Week2 action item extractor.

## Test categories
- Unit (fast): schema validation, rule-based extraction, and mocked LLM parsing.
- Integration (slow): real Ollama calls for LLM extraction.
- Manual scripts: interactive sanity checks under `tests/manual/` (not collected by pytest).

## How to run
```bash
pytest week2/tests
pytest week2/tests -m "not slow"
pytest week2/tests -m slow
```

## Slow tests (LLM)
Slow tests require:
- Ollama running locally
- The model pulled (default: `llama3.1:8b`)

## Manual scripts
```bash
poetry run python week2/tests/manual/manual_filter.py
poetry run python week2/tests/manual/manual_llm.py
```

## Notes on database state
Tests currently use the on-disk SQLite file at `week2/data/app.db`.
If you need isolation, consider patching `DB_PATH` to a temp location or adding a fixture to reset state.
