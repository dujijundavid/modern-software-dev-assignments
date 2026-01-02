# Quick Reference: Command & Pattern Cheat Sheet

> **Navigation**: [CS146S Docs](INDEX.md) > [Quick Reference](./)
>
> **Last Updated**: 2026-01-02
>
> **Coverage**: Weeks 1-4 (Prompting, LLM Integration, MCP, SubAgents)

---

## Prompting (Week 1)

### K-Shot Pattern

```python
# N examples + test case
prompt = f"""
Example 1: {ex1} → {out1}
Example 2: {ex2} → {out2}
Example 3: {ex3} → {out3}
Test: {test_input} →
"""
```

**Usage**: 3-5 examples, ordered simple → complex

### Chain-of-Thought

```python
prompt = "Let's think step by step: {question}"

# Or explicit steps
prompt = """
Step 1: [analyze]
Step 2: [reason]
Step 3: [conclude]
"""
```

**Usage**: Complex reasoning, multi-step problems

### Tool Calling

```python
response = model.generate(
    prompt="What is HTTP 404?",
    tools=[tool_schema]  # Model can request tools
)
# Returns: {tool_use: {name: "tool", parameters: {...}}}
```

### 5W1H Framework

| Component | Question | Example |
|-----------|----------|---------|
| Who | Role? | "You are a HTTP expert" |
| What | Task? | "Extract action items" |
| When | Context? | "When processing meetings" |
| Where | Domain? | "Project management" |
| Why | Goal? | "Ensure actionability" |
| How | Format? | "Return JSON with task, owner, deadline" |

### Key Principles

- **Recency Bias**: Critical examples last
- **Semantic Isolation**: Separate distinct concepts
- **Explicit Structure**: Use delimiters (###, ---)
- **Progressive Complexity**: Simple → complex

---

## LLM Integration (Week 2)

### Architecture

```
┌─────────────────┐
│  Presentation   │  FastAPI routers
├─────────────────┤
│  Business Logic │  Services, validation
├─────────────────┤
│  Data           │  Database, LLM, APIs
└─────────────────┘
```

### Pydantic Schema

```python
from pydantic import BaseModel

class ActionItem(BaseModel):
    task: str
    priority: int  # 1-5
    owner: str | None
    due_date: str | None

# Generate schema
json_schema = ActionItem.model_json_schema()

# Use with LLM
response = await ollama.generate(
    model="llama3.1:8b",
    prompt=f"Extract: {text}",
    format="json",
    schema=json_schema
)

# Validate
item = ActionItem.model_validate_json(response)
```

### Service Layer Pattern

```python
# Presentation (router)
@router.post("/extract")
async def extract_action_items(text: str):
    items = await action_items_service.extract(text)
    return {"ok": True, "data": items}

# Business Logic (service)
async def extract(text: str) -> List[ActionItem]:
    if not text or len(text.strip()) < 10:
        raise ValidationError("Text too short")

    response = await llm_client.extract_items(text)
    return validate_and_process(response)

# Data (LLM client)
async def extract_items(text: str) -> dict:
    response = await ollama.generate(
        model="llama3.1:8b",
        prompt=text,
        format="json"
    )
    return json.loads(response)
```

### Error Handling

```python
try:
    result = process(input)
except ValidationError as e:
    return {
        "ok": False,
        "error": {"code": "VALIDATION_ERROR", "message": str(e)}
    }
except DatabaseError as e:
    return {
        "ok": False,
        "error": {"code": "DATABASE_ERROR", "message": "Failed to save"}
    }
```

### Testing

```python
# Unit test
def test_validate_action_item():
    item = ActionItem(task="Do something", priority=3)
    assert 1 <= item.priority <= 5

# Integration test
@pytest.mark.asyncio
async def test_extract_integration():
    items = await action_items_service.extract(text)
    assert items[0].task == "finish report"

# E2E test
@pytest.mark.asyncio
async def test_extract_e2e():
    async with TestClient(app) as client:
        response = await client.post("/api/action-items/extract", json={"text": "..."})
        assert response.status_code == 200
```

### Temperature Settings

| Temperature | Use Case | Range |
|-------------|----------|-------|
| 0.1-0.3 | Extraction, parsing | Consistent |
| 0.4-0.6 | General tasks | Balanced |
| 0.7-1.0 | Creative tasks | Diverse |

---

## MCP Development (Week 3)

### Architecture

```
┌──────────┐
│ Claude   │
└────┬─────┘
     │ MCP Client
┌────▼─────┐
│ MCP Srv  │
└────┬─────┘
  ┌──┴───┐
  │      │
Tools Resources
```

### FastMCP

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather"""
    return f"Weather in {city}: 72°F"

@mcp.resource("weather://forecasts/{city}")
async def get_forecast(city: str) -> str:
    """Get forecast"""
    return f"5-day forecast for {city}"

@mcp.prompt()
def weather_prompt(city: str) -> str:
    """Generate analysis prompt"""
    return f"Analyze weather for {city}"
```

### Async Patterns

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def process_multiple(items: list) -> list:
    tasks = [fetch_data(item.url) for item in items]
    results = await asyncio.gather(*tasks)
    return results

# With timeout
try:
    result = await asyncio.wait_for(fetch_data(url), timeout=5.0)
except asyncio.TimeoutError:
    logger.error(f"Timeout: {url}")
```

### MCP Config

`~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {"API_KEY": "your-key"}
    }
  }
}
```

### Testing MCP

```python
async def test_mcp_tool():
    async with mcp.ClientSession() as session:
        await session.initialize()

        result = await session.call_tool(
            "get_weather",
            arguments={"city": "San Francisco"}
        )

        assert result["success"] is True
        assert "San Francisco" in result["data"]
```

---

## SubAgents (Week 4)

### 4-Layer Prompt Model

```yaml
---
# Layer 1: YAML (metadata)
name: architect-hub
description: "Module refactoring tool"
---

# Layer 2: Persona (role)
You are a software architect specializing in refactoring.
Focus: clean code, SOLID principles, maintainability.

# Layer 3: Process (workflow)
When asked to refactor:
1. Analyze structure
2. Identify code smells
3. Design improvements
4. Propose steps
5. Validate

# Layer 4: Output (format)
## Analysis
[current state]

## Issues
[problems]

## Proposed Structure
[new design]

## Steps
[refactoring plan]
```

### Agent Roles

- **TestAgent**: Writes failing tests
- **CodeAgent**: Implements to pass
- **ReviewAgent**: Reviews quality
- **Orchestrator**: Coordinates workflow

### Handoff Protocol

```python
def handoff(to_agent: str, context: dict) -> dict:
    return {
        "agent": to_agent,
        "context": context,
        "next_step": "Continue from here",
        "checkpoint": save_checkpoint()
    }
```

### TDD Coordination

```python
async def tdd_cycle(task: str):
    # TestAgent writes tests
    tests = await test_agent.write_tests(task)

    # CodeAgent implements
    code = await code_agent.implement(task, tests)

    # Run tests
    results = await run_tests(code, tests)

    if not all_passed(results):
        # Handoff back to CodeAgent
        await handoff("CodeAgent", {
            "task": task,
            "tests": tests,
            "failed": results.failed
        })
    else:
        # ReviewAgent checks
        review = await review_agent.review(code)
```

### Safe Agent Call

```python
async def safe_agent_call(agent, task, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await agent.execute(task)
        except AgentError as e:
            if attempt == max_retries - 1:
                return {"ok": False, "error": "Failed after retries"}
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Agent Testing

```python
async def test_agent_coordination():
    agent_a = TestAgent()
    agent_b = CodeAgent()

    result_a = await agent_a.execute(task)
    handoff_msg = handoff("CodeAgent", result_a)
    result_b = await agent_b.execute(
        handoff_msg["next_step"],
        context=handoff_msg["context"]
    )

    assert result_b["ok"] is True
```

---

## Common Commands

### pytest

```bash
pytest                          # all tests
pytest -k "test_name"           # specific test
pytest -v                       # verbose
pytest -m "not slow"            # exclude markers
pytest --cov=app                # with coverage
```

### Git

```bash
git checkout -b feature-branch
git add .
git commit -m "message"
git push origin feature-branch
```

### Python

```bash
python -m pytest
python -m pip install package
uv venv && source .venv/bin/activate
```

### Async/Await

```python
# Define
async def fetch_data(): ...

# Call
result = await fetch_data()

# Concurrent
tasks = [fetch_data() for _ in range(10)]
results = await asyncio.gather(*tasks)
```

### Mock Pattern

```python
from unittest.mock import Mock, patch

# Simple mock
mock = Mock(return_value=expected)

# Patch
with patch('llm_client.generate', return_value=mock_response):
    result = await service.extract(text)
```

---

## Debugging Tips

| Symptom | Cause | Fix |
|----------|-------|-----|
| JSON parse error | Invalid format | Use Pydantic validation |
| LLM hallucination | Ambiguous prompt | Add examples |
| Test timeout | Slow operation | Use mocks |
| MCP not found | Wrong path | Check Claude config |
| Agents looping | No iteration limit | Add max_iterations |
| Low quality output | Poor prompt | Use K-shot + CoT |

### Prompt Fixes

```python
# Before (ambiguous)
prompt = "Extract action items"

# After (specific)
prompt = """
Extract action items from meeting notes.
Each must have: task, owner, deadline
Return as JSON array.
"""
```

### LLM Fixes

```python
# Before (no validation)
response = await llm.generate(prompt)
data = json.loads(response)

# After (with validation)
try:
    response = await llm.generate(prompt, format="json")
    data = ActionItem.model_validate_json(response)
except ValidationError as e:
    logger.error(f"Invalid: {e}")
```

### Agent Fixes

```python
# Before (infinite loop)
while not done:
    result = await agent.execute(task)

# After (with limit)
for i in range(max_iterations):
    result = await agent.execute(task)
    if result["ok"]:
        break
else:
    raise AgentError("Failed after max attempts")
```

---

## Automation Levels

- **Level 1**: One-off script
- **Level 2**: Reusable function
- **Level 3**: Composable system
- **Level 4**: Self-improving

### Design Checklist

- [ ] What's the bottleneck?
- [ ] What's the leverage point?
- [ ] How to compound value?

---

## Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| `VALIDATION_ERROR` | Invalid input | Check schema |
| `DATABASE_ERROR` | DB failed | Retry with backoff |
| `LLM_ERROR` | LLM failed | Check API key, reduce rate |
| `TIMEOUT_ERROR` | Timeout | Increase timeout, optimize |
| `AGENT_ERROR` | Agent failed | Check prompt, add retry |

---

## Quick Lookups

### Common Patterns

| Task | Pattern |
|------|---------|
| Structured output | `format="json"` + Pydantic |
| MCP tool | `@mcp.tool()` decorator |
| Test | `def test_` + `assert` |
| Async call | `async def` + `await` |
| Agent handoff | `handoff(agent, context)` |
| K-shot prompt | N examples + test case |

### Temperature Guide

- **0.1-0.3**: Extraction (consistent)
- **0.4-0.6**: General (balanced)
- **0.7-1.0**: Creative (diverse)

---

## Further Reading

- [Theme docs](INDEX.md) for detailed explanations
- [Week 1](weeks/week01/) - Prompting techniques
- [Week 2](weeks/week02/) - LLM integration
- [Week 3](weeks/week03/) - MCP servers
- [Week 4](weeks/week04/) - SubAgents & automation
