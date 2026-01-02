# CS146S Quick Reference Guide

This guide provides quick access to key concepts, patterns, and learnings across all weeks. Use this as a fast lookup for common tasks, debugging issues, and understanding best practices.

> **Navigation**: [CS146S Docs](INDEX.md) > [Quick Reference](./)
>
> **Last Updated**: 2026-01-02
>
> **Coverage**: Weeks 1-4 (Prompting, LLM Integration, MCP, SubAgents)

---

## Table of Contents

- [Prompting Techniques (Week 1)](#prompting-techniques-week-1)
- [LLM Integration (Week 2)](#llm-integration-week-2)
- [MCP Server Development (Week 3)](#mcp-server-development-week-3)
- [SubAgents & Automation (Week 4)](#subagents--automation-week-4)
- [Common Patterns](#common-patterns)
- [Testing Strategies](#testing-strategies)
- [Debugging Tips](#debugging-tips)

---

## Prompting Techniques (Week 1)

### Core Techniques

#### K-shot Prompting
Provide N examples before asking for output to improve model performance.

```python
# 0-shot (no examples)
prompt = "What is the HTTP status code for 'Not Found'?"

# 1-shot (one example)
prompt = """
Question: What is the HTTP status code for 'OK'?
Answer: 200

Question: What is the HTTP status code for 'Not Found'?
Answer: """

# 3-shot (three examples)
prompt = """
Question: What is the HTTP status code for 'OK'?
Answer: 200

Question: What is the HTTP status code for 'Created'?
Answer: 201

Question: What is the HTTP status code for 'Bad Request'?
Answer: 400

Question: What is the HTTP status code for 'Not Found'?
Answer: """
```

**When to use**:
- Tasks requiring pattern recognition
- When model needs examples of desired format
- For complex reasoning tasks

**Best practices**:
- Use 3-5 examples for best results
- Ensure examples are consistent in format
- Order examples from simple to complex

#### Chain-of-Thought (CoT)
Ask model to think step-by-step to improve reasoning.

```python
prompt = """
Let's think step by step.

Question: What HTTP status code should I use for a resource that no longer exists?

Step 1: The resource existed before but is gone
Step 2: The client should not request it again
Step 3: This indicates a permanent state change
Step 4: 404 Not Found is for missing resources
Step 5: 410 Gone is for resources that are permanently gone

Answer: 410 Gone
"""
```

**When to use**:
- Complex reasoning tasks
- Multi-step problems
- When model makes logic errors

**Best practices**:
- Use explicit step numbering
- Show intermediate reasoning
- Verify each step before proceeding

#### Tool Calling
Model can call external tools/APIs to get information.

```python
# Define tool schema
tool_schema = {
    'name': 'http_status_lookup',
    'description': 'Look up HTTP status codes',
    'parameters': {
        'code': {
            'type': 'integer',
            'description': 'HTTP status code'
        }
    }
}

# Model can request tool use
response = model.generate(
    prompt="What is the meaning of HTTP 404?",
    tools=[tool_schema]
)

# Model outputs:
# {
#   'tool_use': {
#     'name': 'http_status_lookup',
#     'parameters': {'code': 404}
#   }
# }
```

**When to use**:
- When model needs current information
- For calculations or data processing
- When accessing external APIs

**Best practices**:
- Provide clear tool descriptions
- Validate tool parameters
- Handle tool errors gracefully

#### Reflexion
Model reflects on its own output to improve it.

```python
prompt = """
Task: Extract action items from meeting notes

Initial Output:
- "Discuss project timeline"
- "Review budget"

Reflection:
- These are not specific action items
- They lack ownership and deadlines
- Need to convert to actionable format

Improved Output:
- "John to create project timeline by Friday"
- "Sarah to review budget and send summary by Monday"
"""
```

**When to use**:
- When initial output is low quality
- For iterative improvement
- To catch common mistakes

**Best practices**:
- Provide reflection criteria
- Show examples of good vs bad output
- Allow multiple refinement iterations

### 5W1H Framework

Use this framework to design systematic prompts:

| Component | Question | Example |
|-----------|----------|---------|
| **Who** | Who is the model? | "You are a HTTP protocol expert" |
| **What** | What should it do? | "Extract action items from meeting notes" |
| **When** | When is this used? | "When processing weekly meeting transcripts" |
| **Where** | Where does it apply? | "In project management context" |
| **Why** | Why is this important? | "To ensure actionability and accountability" |
| **How** | How should it output? | "Return JSON with task, owner, deadline" |

### Key Principles

1. **Recency Bias**: Most recent examples dominate. Place critical examples last.

2. **Semantic Isolation**: Separate distinct concepts to avoid interference.

3. **Explicit Structure**: Use clear delimiters (###, ---, etc.) to structure prompts.

4. **Progressive Complexity**: Start with simple examples, add complexity gradually.

---

## LLM Integration (Week 2)

### Architecture Patterns

#### Layered Architecture
```
┌─────────────────────────┐
│  Presentation Layer     │  FastAPI routers, endpoints
├─────────────────────────┤
│  Business Logic Layer   │  Services, validation, processing
├─────────────────────────┤
│  Data Layer             │  Database, external APIs, LLM
└─────────────────────────┘
```

**Benefits**:
- Clear separation of concerns
- Easy to test each layer independently
- Can swap implementations without affecting other layers

**Implementation**:
```python
# Presentation Layer (routers/action_items.py)
@router.post("/extract")
async def extract_action_items(text: str):
    items = await action_items_service.extract(text)
    return {"ok": True, "data": items}

# Business Logic Layer (services/action_items.py)
async def extract(text: str) -> List[ActionItem]:
    # Validate input
    if not text or len(text.strip()) < 10:
        raise ValidationError("Text too short")

    # Call LLM
    response = await llm_client.extract_items(text)

    # Validate and process
    return validate_and_process(response)

# Data Layer (llm/client.py)
async def extract_items(text: str) -> dict:
    response = await ollama.generate(
        model="llama3.1:8b",
        prompt=text,
        format="json"
    )
    return json.loads(response)
```

#### Structured Output with JSON Schema

Always use JSON schemas to guarantee parseable LLM responses.

```python
from pydantic import BaseModel

class ActionItem(BaseModel):
    task: str
    priority: int  # 1-5
    owner: Optional[str]
    due_date: Optional[str]

# Convert to JSON Schema
json_schema = ActionItem.model_json_schema()

# Use with Ollama
response = await ollama.generate(
    model="llama3.1:8b",
    prompt=f"Extract action items: {text}",
    format="json",
    schema=json_schema
)

# Validate response
item = ActionItem.model_validate_json(response)
```

**Best practices**:
- Use Pydantic for type safety
- Provide clear field descriptions
- Set appropriate temperature (0.1-0.3 for extraction)
- Validate responses before use

### Testing Pyramid

```
           /\
          /  \    E2E Tests (few, slow)
         /____\
        /      \  Integration Tests (some, medium)
       /________\
      /          \ Unit Tests (many, fast)
     /____________\
```

#### Unit Tests
Test business logic in isolation.

```python
def test_validate_action_item():
    """Test validation logic"""
    item = ActionItem(task="Do something", priority=3)
    assert item.task == "Do something"
    assert 1 <= item.priority <= 5

def test_extract_text_too_short():
    """Test error handling"""
    with pytest.raises(ValidationError):
        validate_text("hi")
```

#### Integration Tests
Test LLM integration with mocked or real LLM.

```python
@pytest.mark.asyncio
async def test_extract_action_items_integration():
    """Test with real Ollama"""
    text = "John needs to finish the report by Friday"
    items = await action_items_service.extract(text)

    assert len(items) > 0
    assert items[0].task == "finish the report"
    assert items[0].owner == "John"
```

#### E2E Tests
Test full application flow.

```python
@pytest.mark.asyncio
async def test_extract_action_items_e2e():
    """Test full endpoint"""
    async with TestClient(app) as client:
        response = await client.post(
            "/api/action-items/extract",
            json={"text": "John to finish report by Friday"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["ok"] is True
        assert len(data["data"]) > 0
```

### Best Practices

1. **Always validate structured outputs** with Pydantic
2. **Test prompts separately** from code
3. **Use test databases** for development
4. **Handle errors gracefully** at layer boundaries
5. **Set appropriate temperature** for task (0.1-0.3 for extraction, 0.7+ for creative)
6. **Provide clear instructions** in prompts
7. **Use async/await** for LLM calls to avoid blocking

---

## MCP Server Development (Week 3)

### MCP Protocol

MCP (Model Context Protocol) enables AI models to communicate with external tools, resources, and data sources.

#### Three Core Capabilities

1. **Tools**: Executable functions that LLM can call
2. **Resources**: Data sources (files, databases, APIs)
3. **Prompts**: Pre-processing templates for common tasks

#### Architecture

```
┌──────────────┐
│ AI App       │
│ (Claude)     │
└──────┬───────┘
       │
       │ MCP Client
       │
┌──────▼───────┐
│ MCP Server   │
│ (Your Code)  │
└──────┬───────┘
       │
   ┌───┴────┐
   │        │
┌──▼──┐  ┌─▼────┐
│Tools│  │Resources│
└─────┘  └────────┘
```

### FastMCP Framework

FastMCP simplifies MCP server development with decorators.

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city"""
    # Implementation
    return f"Weather in {city}: 72°F"

@mcp.resource("weather://forecasts/{city}")
async def get_forecast(city: str) -> str:
    """Get weather forecast"""
    return f"5-day forecast for {city}: ..."

@mcp.prompt()
def weather_prompt(city: str) -> str:
    """Generate weather analysis prompt"""
    return f"Analyze weather patterns for {city}"
```

### Async Programming

#### Async/Await Patterns

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Non-blocking HTTP request"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def process_multiple(items: list) -> list:
    """Process items concurrently"""
    tasks = [fetch_data(item.url) for item in items]
    results = await asyncio.gather(*tasks)
    return results
```

#### Key Points

- Use `async def` for coroutine functions
- Use `await` for coroutines
- Use `asyncio.gather()` for concurrent operations
- Handle timeouts and errors

### Testing MCP Servers

```python
import mcp

async def test_mcp_tool():
    """Test MCP tool with client session"""
    async with mcp.ClientSession() as session:
        # Initialize connection
        await session.initialize()

        # Call tool
        result = await session.call_tool(
            "get_weather",
            arguments={"city": "San Francisco"}
        )

        assert result["success"] is True
        assert "San Francisco" in result["data"]
```

### Deployment to Claude Desktop

1. **Create MCP config**: `~/.claude/mcp_config.json`
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-key"
      }
    }
  }
}
```

2. **Restart Claude Desktop**

3. **Verify in Claude**: Server appears in "MCP Servers" section

---

## SubAgents & Automation (Week 4)

### 4-Layer Prompt Model

Design slash commands with four cognitive layers:

```yaml
---
# Layer 1: YAML (Machine-readable)
name: architect-hub
description: "Module refactoring tool"
category: development
version: "1.0"
---

# Layer 2: Persona (Role definition)
You are a software architect specializing in module refactoring.
You focus on clean code, SOLID principles, and maintainability.

# Layer 3: Process (Structured workflow)
When asked to refactor:
1. Analyze current module structure
2. Identify code smells and violations
3. Design improved structure
4. Propose refactoring steps
5. Validate improvements

# Layer 4: Output (Standardized format)
Return results in this format:
## Analysis
[Current structure analysis]

## Issues
[Identified issues]

## Proposed Structure
[New structure design]

## Steps
[Step-by-step refactoring plan]
```

### SubAgent Coordination

#### Agent Roles

Define clear roles for each agent:
- **TestAgent**: Writes failing tests
- **CodeAgent**: Implements to pass tests
- **ReviewAgent**: Reviews code quality
- **Orchestrator**: Coordinates the workflow

#### Handoff Protocol

```python
def handoff(to_agent: str, context: dict) -> dict:
    """
    Hand off control to another agent

    Args:
        to_agent: Target agent name
        context: Current state and progress

    Returns:
        Handoff message with context
    """
    return {
        "agent": to_agent,
        "context": context,
        "next_step": "Continue from here",
        "handoff_from": "current_agent"
    }
```

#### Coordination Pattern

```python
async def tdd_cycle(task: str):
    """Orchestrate TDD cycle with multiple agents"""

    # Step 1: TestAgent writes tests
    tests = await test_agent.write_tests(task)
    print(f"TestAgent: Created {len(tests)} tests")

    # Step 2: CodeAgent implements
    code = await code_agent.implement(task, tests)
    print(f"CodeAgent: Implemented solution")

    # Step 3: Run tests
    results = await run_tests(code, tests)

    if not all_passed(results):
        # Handoff back to CodeAgent
        await handoff("CodeAgent", {
            "task": task,
            "tests": tests,
            "failed": results.failed
        })
    else:
        # Step 4: ReviewAgent checks quality
        review = await review_agent.review(code)
        print(f"ReviewAgent: {review.status}")
```

### TDD with SubAgents

```python
class TestAgent:
    """Agent that writes tests"""

    async def write_tests(self, task: str) -> List[str]:
        prompt = f"""
        Write failing tests for: {task}

        Requirements:
        - Use pytest framework
        - Test edge cases
        - Include error cases
        - Follow AAA pattern (Arrange, Act, Assert)
        """
        return await llm.generate(prompt)

class CodeAgent:
    """Agent that implements code"""

    async def implement(self, task: str, tests: List[str]) -> str:
        prompt = f"""
        Implement code to pass these tests: {tests}

        Task: {task}

        Requirements:
        - Make all tests pass
        - Follow best practices
        - Add error handling
        - Include type hints
        """
        return await llm.generate(prompt)
```

---

## Common Patterns

### Error Handling

#### Week 2 Pattern
```python
try:
    result = process(input)
except ValidationError as e:
    return {
        "ok": False,
        "error": {
            "code": "VALIDATION_ERROR",
            "message": str(e)
        }
    }
except DatabaseError as e:
    return {
        "ok": False,
        "error": {
            "code": "DATABASE_ERROR",
            "message": "Failed to save data"
        }
    }
```

#### Week 4 Pattern (SubAgents)
```python
async def safe_agent_call(agent, task, max_retries=3):
    """Call agent with error handling and retries"""
    for attempt in range(max_retries):
        try:
            return await agent.execute(task)
        except AgentError as e:
            if attempt == max_retries - 1:
                return {
                    "ok": False,
                    "error": f"Agent failed after {max_retries} attempts"
                }
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

### Structured Output

#### Week 2 Pattern
```python
from pydantic import BaseModel

class ActionItem(BaseModel):
    task: str
    priority: int
    due_date: Optional[str]

# Use with LLM
response = await llm.generate(
    prompt="Extract action items",
    schema=ActionItem.model_json_schema()
)

# Validate
item = ActionItem.model_validate_json(response)
```

### Agent Handoff

#### Week 4 Pattern
```python
def handoff(to_agent, context):
    """Hand off control to another agent"""
    return {
        "agent": to_agent,
        "context": context,
        "next_step": "Continue from here",
        "checkpoint": save_checkpoint()
    }
```

---

## Testing Strategies

### Week 1: Prompt Testing
```python
def test_k_shot_prompting():
    """Test K-shot prompting effectiveness"""
    prompt = create_k_shot_prompt(examples=3)
    response = llm.generate(prompt)

    assert response.accuracy > 0.8
    assert response.format_valid

def test_chain_of_thought():
    """Test CoT improves reasoning"""
    with_cot = llm.generate(prompt + "Let's think step by step")
    without_cot = llm.generate(prompt)

    assert with_cot.accuracy > without_cot.accuracy
```

### Week 2: LLM Application Testing
```python
@pytest.mark.asyncio
async def test_action_item_extraction():
    """Test extraction with mock LLM"""
    # Mock LLM response
    mock_response = {
        "action_items": [
            {"task": "Finish report", "owner": "John"}
        ]
    }

    with patch('llm_client.generate', return_value=mock_response):
        items = await action_items_service.extract(text)

    assert len(items) == 1
    assert items[0].owner == "John"
```

### Week 3: MCP Server Testing
```python
@pytest.mark.asyncio
async def test_mcp_tool():
    """Test MCP tool independently"""
    async with mcp.ClientSession() as session:
        result = await session.call_tool(
            "my_tool",
            arguments={"param": "value"}
        )

    assert result["success"] is True
    assert "expected_data" in result
```

### Week 4: SubAgent Testing
```python
@pytest.mark.asyncio
async def test_agent_coordination():
    """Test handoff protocol"""
    agent_a = TestAgent()
    agent_b = CodeAgent()

    # Agent A completes
    result_a = await agent_a.execute(task)

    # Handoff to Agent B
    handoff_msg = handoff("CodeAgent", result_a)

    # Agent B continues
    result_b = await agent_b.execute(
        handoff_msg["next_step"],
        context=handoff_msg["context"]
    )

    assert result_b["ok"] is True
```

---

## Debugging Tips

### Prompt Issues

**Symptom**: Low quality or inconsistent outputs

**Solutions**:
1. Add more examples (3-5 optimal)
2. Use chain-of-thought for reasoning tasks
3. Check for ambiguity in instructions
4. Test with simpler inputs first
5. Order examples by complexity (simple → complex)

**Example fix**:
```python
# Before (ambiguous)
prompt = "Extract action items"

# After (specific)
prompt = """
Extract action items from meeting notes.
Each action item must have:
- Task description
- Owner (person responsible)
- Deadline (specific date)

Return as JSON array.
"""
```

### LLM Integration Issues

**Symptom**: Parse errors, invalid JSON

**Solutions**:
1. Validate JSON schemas before use
2. Check API responses for errors
3. Test with known good inputs
4. Add structured logging
5. Use lower temperature (0.1-0.3)

**Example fix**:
```python
# Before (no validation)
response = await llm.generate(prompt)
data = json.loads(response)

# After (with validation)
try:
    response = await llm.generate(prompt, format="json")
    data = json.loads(response)
    item = ActionItem.model_validate(data)
except ValidationError as e:
    logger.error(f"Invalid response: {e}")
    raise
```

### MCP Server Issues

**Symptom**: Tool not found, connection errors

**Solutions**:
1. Test tool endpoints independently
2. Check async handling (await coroutines)
3. Verify resource access permissions
4. Monitor timeouts (use asyncio.wait_for)
5. Check MCP config in Claude Desktop

**Example fix**:
```python
# Before (no timeout)
result = await fetch_data(url)

# After (with timeout)
try:
    result = await asyncio.wait_for(
        fetch_data(url),
        timeout=5.0
    )
except asyncio.TimeoutError:
    logger.error(f"Timeout fetching {url}")
    raise
```

### SubAgent Issues

**Symptom**: Agents looping, unclear responsibilities

**Solutions**:
1. Test each agent independently first
2. Check handoff protocols for completeness
3. Verify role clarity in prompts
4. Add maximum iteration limits
5. Monitor agent state transitions

**Example fix**:
```python
# Before (infinite loop possible)
while not done:
    result = await agent.execute(task)

# After (with limit)
max_iterations = 5
for i in range(max_iterations):
    result = await agent.execute(task)
    if result["ok"]:
        break
else:
    raise AgentError(f"Failed after {max_iterations} attempts")
```

---

## Further Reading

- [Week 1 Documentation](weeks/week01/) - Prompting techniques and case studies
- [Week 2 Documentation](weeks/week02/) - LLM integration and testing
- [Week 3 Documentation](weeks/week03/) - MCP server development
- [Week 4 Documentation](weeks/week04/) - SubAgents and automation
- [Weekly Index](weeks/INDEX.md) - Detailed week-by-week guide
- [Migration Report](MIGRATION_VALIDATION_REPORT.md) - Documentation status

---

## Quick Lookups

### Common Commands

| Task | Command/Pattern |
|------|----------------|
| Generate structured output | `format="json"`, Pydantic validation |
| Create MCP tool | `@mcp.tool()` decorator |
| Write test with pytest | `def test_`, `assert` statements |
| Async LLM call | `async def`, `await llm.generate()` |
| Agent handoff | `handoff(agent, context)` function |
| K-shot prompt | Provide N examples before task |

### Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| `VALIDATION_ERROR` | Invalid input format | Check schema, validate input |
| `DATABASE_ERROR` | Database operation failed | Check connection, retry with backoff |
| `LLM_ERROR` | LLM call failed | Check API key, reduce rate, retry |
| `TIMEOUT_ERROR` | Operation timed out | Increase timeout, optimize query |
| `AGENT_ERROR` | Agent execution failed | Check agent prompt, add retry logic |

### Temperature Settings

| Temperature | Use Case | Range |
|-------------|----------|-------|
| Low (0.1-0.3) | Extraction, parsing | Consistent output |
| Medium (0.4-0.6) | General tasks | Balanced |
| High (0.7-1.0) | Creative tasks | Diverse output |

---

*Last updated: 2026-01-02 | Next review: When Week 5 documentation is complete*
