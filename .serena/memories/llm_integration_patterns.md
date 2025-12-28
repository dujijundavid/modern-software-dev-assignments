# LLM Integration Patterns

Best practices for integrating Large Language Models into production applications.

---

## Ollama Integration

### Basic Setup

**Configuration:**
```python
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "llama3.1:8b",
    "timeout": 30,
    "temperature": 0.1,
}
```

**Health Check:**
```python
import requests

async def check_ollama_health():
    """Verify Ollama service is running"""
    try:
        response = requests.get(f"{OLLAMA_CONFIG['base_url']}/api/tags", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
```

**Usage:**
```python
import ollama

async def call_ollama(prompt: str, system_prompt: str = None) -> str:
    """Call Ollama with error handling"""
    if not await check_ollama_health():
        raise RuntimeError("Ollama service not available")
    
    response = ollama.__call__(
        model=OLLAMA_CONFIG["model"],
        prompt=prompt,
        system=system_prompt,
        options={"temperature": OLLAMA_CONFIG["temperature"]},
    )
    return response
```

---

## Structured Output with JSON Schema

### Problem: LLMs Return Unpredictable Formats

**Without schema enforcement:**
```python
response = ollama.__call__(model="llama3.1:8b", prompt="Extract action items")
# Returns: "Here are the items: 1. Do X, 2. Do Y"  # Not JSON!
```

### Solution: Use JSON Schema Enforcement

```python
response = ollama.__call__(
    model="llama3.1:8b",
    prompt=prompt,
    format="json",  # Enforce JSON output
    schema={
        "type": "array",
        "items": {
            "type": "string",
            "description": "An action item"
        }
    }
)

# Returns: '["item 1", "item 2", "item 3"]'  # Pure JSON!
```

### Robust JSON Parsing

```python
import json
import re

def parse_llm_json(response: str) -> list:
    """Parse JSON from LLM with fallback strategies"""
    try:
        # Try direct parse first
        return json.loads(response)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        # Try to find any JSON array
        array_match = re.search(r'\[.*?\]', response, re.DOTALL)
        if array_match:
            return json.loads(array_match.group(0))
        
        raise ValueError(f"Could not parse JSON from: {response[:100]}")
```

---

## Prompt Engineering Patterns

### System Prompts

**Effective pattern for action item extraction:**
```python
SYSTEM_PROMPT = """You are an action item extraction assistant. Your task is to extract specific, actionable items from text.

Rules:
- Extract ONLY clear, specific action items
- Exclude vague items like "do work", "stuff to do", "tasks"
- Exclude single-word items shorter than 6 characters
- Preserve the original wording
- Return as a JSON array of strings

Example:
Input: "I need to finish the project report by Friday and call John about the meeting."
Output: ["finish the project report by Friday", "call John about the meeting"]
"""
```

### Few-Shot Prompting

```python
prompt = f"""Extract action items from the following text.

Example 1:
Text: "Remember to buy groceries and call mom."
Items: ["buy groceries", "call mom"]

Example 2:
Text: "Meeting tomorrow at 3pm, prepare presentation slides."
Items: ["Meeting tomorrow at 3pm", "prepare presentation slides"]

Now extract from this text:
Text: {user_text}
Items:"""

response = ollama.__call__(prompt, system=SYSTEM_PROMPT)
```

### Chain-of-Thought for Complex Tasks

```python
prompt = f"""Let's think step by step to extract action items from: {text}

Step 1: Identify all potential tasks or commitments in the text.
Step 2: Filter out vague or non-specific items.
Step 3: Convert each remaining item into a clear action statement.
Step 4: Return as JSON array.

Now execute:"""
```

---

## Temperature Tuning

### Temperature vs Use Case

| Temperature | Range | Use Case | Example |
|-------------|-------|----------|---------|
| Low | 0.0-0.2 | Structured extraction, code generation | JSON output, API responses |
| Medium | 0.3-0.7 | General purpose, balanced | Content creation, summaries |
| High | 0.8-1.0 | Creative, diverse | Brainstorming, creative writing |

**For reliable extraction:**
```python
RELIABLE_CONFIG = {
    "temperature": 0.1,  # Low for consistency
    "top_p": 0.9,        # Still allow some variation
    "repeat_penalty": 1.0,
}
```

---

## Error Handling & Graceful Degradation

### Retry with Exponential Backoff

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def call_ollama_with_retry(prompt: str) -> str:
    """Call Ollama with retry logic"""
    try:
        return ollama.__call__(model="llama3.1:8b", prompt=prompt)
    except Exception as e:
        logger.warning(f"Ollama call failed: {e}, retrying...")
        raise
```

### Fallback Strategies

```python
async def extract_with_fallback(text: str) -> list:
    """Try multiple strategies in order"""
    # Strategy 1: LLM extraction
    try:
        items = await extract_with_llm(text)
        if items:  # Got results
            return items
    except Exception as e:
        logger.error(f"LLM extraction failed: {e}")
    
    # Strategy 2: Regex-based extraction (simple)
    items = extract_with_regex(text)
    if items:
        logger.info("Fell back to regex extraction")
        return items
    
    # Strategy 3: Return empty
    logger.warning("All extraction strategies failed")
    return []
```

---

## Response Post-Processing

### Deduplication

```python
def deduplicate_items(items: list) -> list:
    """Remove duplicate action items"""
    seen = set()
    unique = []
    
    for item in items:
        normalized = item.lower().strip()
        if normalized not in seen:
            seen.add(normalized)
            unique.append(item)
    
    return unique
```

### Vague Item Filtering

```python
def is_vague_item(item: str) -> bool:
    """Check if item is too vague"""
    item = item.strip().lower()
    
    # Too short
    if len(item) < 6 and ' ' not in item:
        return True
    
    # Vague phrases
    vague_phrases = ['do work', 'stuff', 'things to do', 'tasks', 'todo']
    if any(phrase in item for phrase in vague_phrases):
        return True
    
    return False

def filter_vague_items(items: list) -> list:
    """Remove vague action items"""
    return [item for item in items if not is_vague_item(item)]
```

### Order Preservation

```python
# Ollama maintains order, but if using multiple LLM calls:
from collections import OrderedDict

def preserve_order(items: list) -> list:
    """Remove duplicates while preserving order"""
    return list(OrderedDict.fromkeys(items))
```

---

## Performance Optimization

### Caching

```python
from functools import lru_cache
import hashlib

def cache_key(prompt: str) -> str:
    """Generate cache key from prompt"""
    return hashlib.md5(prompt.encode()).hexdigest()

@lru_cache(maxsize=100)
async def cached_llm_call(prompt: str) -> str:
    """Cache LLM responses for identical prompts"""
    return ollama.__call__(model="llama3.1:8b", prompt=prompt)

# Usage
response = await cached_llm_call(user_prompt)
```

### Batch Processing

```python
async def extract_from_multiple_notes(notes: list) -> dict:
    """Extract items from multiple notes efficiently"""
    tasks = [extract_from_note(note.id) for note in notes]
    results = await asyncio.gather(*tasks)
    
    return {
        note.id: items 
        for note, items in zip(notes, results)
    }
```

---

## Rate Limiting

### For External APIs (e.g., Notion MCP)

```python
import asyncio

class RateLimiter:
    def __init__(self, rate: float):
        self.rate = rate  # Requests per second
        self.last_call = None
    
    async def acquire(self):
        """Wait before allowing next call"""
        if self.last_call:
            elapsed = time.time() - self.last_call
            wait_time = (1.0 / self.rate) - elapsed
            
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        self.last_call = time.time()

# Usage
limiter = RateLimiter(3)  # 3 requests per second

async def call_notion_api(endpoint: str):
    await limiter.acquire()
    # ... API call ...
```

---

## Testing LLM Integration

### Unit Tests (Mock LLM)

```python
@pytest.fixture
def mock_llm(monkeypatch):
    """Mock LLM for deterministic unit tests"""
    def mock_call(prompt, **kwargs):
        return '["action 1", "action 2"]'
    
    monkeypatch.setattr("ollama.__call__", mock_call)

def test_extract_with_mock(mock_llm):
    result = extract_action_items_llm("test")
    assert result == ["action 1", "action 2"]
```

### Integration Tests (Real LLM)

```python
@pytest.mark.slow
@pytest.mark.integration
async def test_extract_with_real_llm():
    """Test with actual Ollama - mark as slow"""
    result = await extract_action_items_llm("Buy milk and call John")
    
    # Verify structure, not exact content
    assert isinstance(result, list)
    assert len(result) >= 1
    assert all(isinstance(item, str) for item in result)
```

---

## Monitoring & Observability

### Logging

```python
import logging

logger = logging.getLogger(__name__)

async def call_ollama_with_logging(prompt: str):
    """Call Ollama with logging"""
    logger.info(f"Calling Ollama with prompt: {prompt[:50]}...")
    
    start = time.time()
    try:
        response = await call_ollama(prompt)
        duration = time.time() - start
        
        logger.info(f"Ollama response received in {duration:.2f}s")
        logger.debug(f"Response: {response[:100]}...")
        
        return response
    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        raise
```

### Metrics

```python
# Track success rates, latency, token usage
class LLMMetrics:
    def __init__(self):
        self.calls = 0
        self.failures = 0
        self.total_latency = 0
    
    def record_call(self, latency: float, success: bool):
        self.calls += 1
        self.total_latency += latency
        if not success:
            self.failures += 1
    
    @property
    def success_rate(self) -> float:
        if self.calls == 0:
            return 1.0
        return (self.calls - self.failures) / self.calls
```

---

## Common Pitfalls

### ❌ Don't: Use High Temperature for Extraction
```python
# Bad: Unpredictable outputs
ollama.__call__(prompt, options={"temperature": 0.8})
```

### ✅ Do: Use Low Temperature for Consistency
```python
# Good: Reliable outputs
ollama.__call__(prompt, options={"temperature": 0.1})
```

### ❌ Don't: Assume JSON is Perfect
```python
# Bad: Crashes on malformed JSON
items = json.loads(llm_response)
```

### ✅ Do: Parse with Error Handling
```python
# Good: Graceful fallback
try:
    items = json.loads(llm_response)
except json.JSONDecodeError:
    items = parse_llm_json(llm_response)  # Custom parser
```

### ❌ Don't: Call LLM Synchronously in Request Handler
```python
# Bad: Blocks the event loop
@app.post("/extract")
def extract(text: str):
    result = ollama.__call__(text)  # Sync call!
    return result
```

### ✅ Do: Use Async for LLM Calls
```python
# Good: Non-blocking
@app.post("/extract")
async def extract(text: str):
    result = await call_ollama_async(text)
    return result
```
