# LLM Integration Practice

> **Goal**: Implement intelligent action item extraction using LLM with structured output

## Core Concepts

### 1. Structured Output

Why use JSON Schema with LLMs?

```python
# Without structured output - unpredictable
prompt = "Extract action items, return as JSON"
response = llm(prompt)  
# May return: "Here are the items:\n- item1\n- item2"
# Complex parsing needed

# With structured output - reliable
json_schema = {
    'type': 'object',
    'properties': {
        'action_items': {
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'List of actionable items'
        }
    },
    'required': ['action_items']
}
response = chat(..., format='json')
# Guaranteed: {"action_items": ["item1", "item2"]}
```

### 2. Temperature Tuning

| Temperature | Behavior | Use Case |
|-------------|----------|----------|
| 0.0-0.3 | Highly deterministic | Extraction, parsing |
| 0.5-0.7 | Balanced | Dialogue, general tasks |
| 0.7-1.0 | Creative | Content generation |

For extraction tasks: use `temperature=0.1` for consistency.

### 3. System Prompt Engineering

```python
SYSTEM_PROMPT = """
You are an action item extraction assistant.

RULES:
1. Only extract clear, specific actions that someone should do
2. Ignore greetings, pleasantries, and context
3. Ignore descriptive statements that aren't actions
4. Remove formatting markers like "-", "•", "[ ]"
5. Keep each item concise but complete

EXAMPLES:
Input: "Let's schedule a follow-up meeting."
Output: ["Schedule a follow-up meeting"]

Input: "Hi everyone, thanks for coming."
Output: []
"""
```

### 4. Post-Processing

```python
def post_process_items(items: list[str]) -> list[str]:
    # Clean whitespace
    items = [item.strip() for item in items]
    
    # Filter empty strings
    items = [item for item in items if item]
    
    # Deduplicate (preserve order)
    seen = set()
    unique_items = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            unique_items.append(item)
    
    # Validate length
    return [item for item in unique_items if len(item) > 3]
```

### 5. Error Handling - Graceful Degradation

```python
try:
    response = chat(...)
    items = parse_response(response)
except httpx.ConnectError:
    logger.warning("Ollama not available, returning empty list")
    return []
except json.JSONDecodeError:
    logger.warning(f"Invalid JSON from LLM: {response}")
    return []
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return []
```

**Design principle**: Never let LLM errors crash your application.

## Implementation Example

```python
from ollama import chat
import json
import logging

logger = logging.getLogger(__name__)

def extract_action_items_llm(text: str, model: str = "llama3.1:8b") -> list[str]:
    """Extract action items from text using LLM."""
    
    system_prompt = """You are an action item extraction assistant..."""
    
    json_schema = {
        'type': 'object',
        'properties': {
            'action_items': {
                'type': 'array',
                'items': {'type': 'string'}
            }
        },
        'required': ['action_items']
    }
    
    try:
        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            format='json',
            options={'temperature': 0.1}
        )
        
        content = response['message']['content']
        data = json.loads(content)
        items = data.get('action_items', [])
        
        return post_process_items(items)
        
    except Exception as e:
        logger.error(f"LLM extraction failed: {e}")
        return []
```

## Key Takeaways

1. **Structured output = reliability** - JSON Schema ensures parseable output
2. **System prompt = accuracy** - Tell LLM what is/isn't an action item
3. **Post-processing = robustness** - Clean, deduplicate, validate
4. **Error handling = graceful degradation** - Return [] instead of crashing
5. **Temperature tuning** - Lower (0.1-0.3) for extraction, higher for creativity

## Common Issues

| Issue | Solution |
|-------|----------|
| LLM extracts vague items like "help" | Add post-processing filter for short words |
| Inconsistent output | Lower temperature to 0.1 |
| Invalid JSON | Use `format='json'` parameter in Ollama |
| API timeouts | Add try-except with timeout handling |
| Duplicate items | Deduplicate in post-processing |

## Related Files

- Implementation: `week2/app/services/extract.py`
- Tests: `week2/tests/test_extract.py`
- Testing guide: `practice/testing_patterns.md`
