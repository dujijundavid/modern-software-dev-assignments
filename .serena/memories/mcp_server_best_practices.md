# MCP Server Best Practices

Best practices and patterns for building robust Model Context Protocol (MCP) servers.

---

## Metadata

| 字段 | 值 |
|------|-----|
| **创建时间** | 2025-01-19 |
| **最后更新** | 2025-01-19 |
| **维护者** | AI Team |
| **状态** | Active |
| **相关记忆** | [LLM Integration Patterns](llm_integration_patterns.md), [Code Patterns](code_patterns.md) |

---

## Core Principles

### 1. Tool Design Philosophy

**DO ✅**:
- Each tool should do ONE thing well
- Use clear, descriptive names (e.g., `get_weather` not `data`)
- Provide detailed docstrings for AI understanding
- Return structured data (JSON, not unstructured text)

**DON'T ❌**:
- Don't create "Swiss Army Knife" tools
- Don't use abbreviations in tool names
- Don't return error messages as exceptions (use error responses)

### 2. Error Handling Strategy

```python
# Pattern: Consistent Error Response Structure

@mcp.tool()
async def get_user(user_id: str) -> dict:
    """
    Get user by ID with proper error handling.
    
    Returns:
        dict with structure: {"ok": bool, "data": any, "error": str}
    """
    try:
        user = await db.get_user(user_id)
        if not user:
            return {"ok": False, "error": "User not found", "data": None}
        return {"ok": True, "data": user, "error": None}
    except Exception as e:
        return {"ok": False, "error": str(e), "data": None}
```

**Key Insight**: Always return a response, never raise exceptions to the LLM.

### 3. Rate Limiting Pattern

```python
# From week3/weather_server implementation

class RateLimiter:
    """Token bucket rate limiter for MCP tools"""
    
    def __init__(self, rate: float, burst: int = 5):
        self.rate = rate  # Tokens per second
        self.burst = burst
        self.tokens = burst
        self.last_update = time.time()
    
    async def acquire(self):
        """Wait for token availability"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_update = now
        
        if self.tokens < 1:
            wait_time = (1 - self.tokens) / self.rate
            await asyncio.sleep(wait_time)
            self.tokens = 0
        else:
            self.tokens -= 1

# Usage in tool
@mcp.tool()
async def fetch_data(url: str) -> dict:
    await rate_limiter.acquire()
    # ... perform fetch ...
```

### 4. Resource vs Tool Decision

**Use Resources when**:
- Data is read-only (e.g., config files, schemas)
- Data changes infrequently
- Multiple tools need access to same data
- You want caching

**Use Tools when**:
- Operation performs actions (write, update, delete)
- Data changes frequently
- Operation has side effects
- Need real-time computation

---

## MCP Server Architecture Patterns

### Pattern 1: FastMCP (Recommended for Python)

```python
# Simple, declarative MCP server

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-server")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get current weather for a city"""
    return await weather_api.fetch(city)

@mcp.resource("weather://forecast")
async def get_forecast() -> str:
    """7-day weather forecast"""
    return await weather_api.get_forecast()
```

**Advantages**:
- Minimal boilerplate
- Auto-generated documentation
- Built-in error handling
- Easy testing

### Pattern 2: Layered Service Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Tool Layer                        │
│  (Exposes functionality to LLM)                          │
│  - @mcp.tool() decorators                                │
│  - Input validation                                     │
│  - Response formatting                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  Service Layer                           │
│  (Business logic, no MCP concerns)                      │
│  - WeatherService.fetch()                               │
│  - Cache management                                     │
│  - Rate limiting                                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  Data Layer                             │
│  (External integrations)                                │
│  - HTTP clients (httpx)                                 │
│  - Database connections                                 │
│  - File system access                                   │
└─────────────────────────────────────────────────────────┘
```

**Example**:
```python
# Service layer (MCP-agnostic)
class WeatherService:
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient()
        self.cache = {}
    
    async def fetch(self, city: str) -> dict:
        # Business logic here
        pass

# MCP layer
service = WeatherService(api_key=os.getenv("API_KEY"))

@mcp.tool()
async def get_weather(city: str) -> str:
    """MCP tool wraps service"""
    return await service.fetch(city)
```

---

## Testing MCP Servers

### Unit Testing (Mock External Dependencies)

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_get_weather_success():
    # Arrange
    mock_client = AsyncMock()
    mock_client.get.return_value = {"temp": 20, "city": "Tokyo"}
    
    # Act
    result = await get_weather("Tokyo", client=mock_client)
    
    # Assert
    assert result["temp"] == 20
    assert result["city"] == "Tokyo"
```

### Integration Testing (Real MCP Client)

```python
import pytest
from mcp import ClientSession

@pytest.mark.asyncio
async def test_mcp_tool_call():
    # Start MCP server
    server = WeatherServer()
    session = ClientSession(server)
    
    # Call tool through MCP protocol
    result = await session.call_tool("get_weather", {"city": "Tokyo"})
    
    # Verify structure
    assert result["ok"] == True
    assert "data" in result
```

### Rate Limiting Tests

```python
@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(rate=10)  # 10 requests/sec
    
    start = time.time()
    
    # Should process 10 requests quickly
    for _ in range(10):
        await limiter.acquire()
    
    duration = time.time() - start
    assert duration < 0.1  # Should be fast
    
    # 11th request should wait
    start = time.time()
    await limiter.acquire()
    duration = time.time() - start
    assert duration >= 0.1  # Should have waited
```

---

## Common Pitfalls

### ❌ Pitfall 1: Blocking Operations in Tools

```python
# BAD: Blocks the MCP server event loop
@mcp.tool()
def fetch_sync(url: str):
    return requests.get(url).json()  # Synchronous!
```

```python
# GOOD: Non-blocking async
@mcp.tool()
async def fetch_async(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### ❌ Pitfall 2: Not Validating Inputs

```python
# BAD: Trusts input blindly
@mcp.tool()
async def delete_user(user_id: str):
    await db.delete(user_id)  # What if user_id is malicious?
```

```python
# GOOD: Validates and sanitizes
@mcp.tool()
async def delete_user(user_id: str):
    if not user_id.isalnum():
        return {"ok": False, "error": "Invalid user_id format"}
    
    user = await db.get_user(user_id)
    if not user:
        return {"ok": False, "error": "User not found"}
    
    await db.delete(user_id)
    return {"ok": True, "data": None}
```

### ❌ Pitfall 3: Ignoring Rate Limits

```python
# BAD: No rate limiting
@mcp.tool()
async def fetch_external_api():
    return await httpx.get("https://api.example.com/data")
    # Will get 429 Too Many Requests!
```

```python
# GOOD: Rate limited
limiter = RateLimiter(rate=5)  # 5 requests/sec

@mcp.tool()
async def fetch_external_api():
    await limiter.acquire()
    return await httpx.get("https://api.example.com/data")
```

---

## Performance Optimization

### 1. Response Caching

```python
from functools import lru_cache
from typing import Optional

@mcp.tool()
@lru_cache(maxsize=100)
def get_config(key: str) -> Optional[str]:
    """Cached configuration lookup"""
    return config.get(key)
```

### 2. Batch Operations

```python
@mcp.tool()
async def get_weather_batch(cities: list[str]) -> dict:
    """Fetch weather for multiple cities efficiently"""
    tasks = [fetch_weather(city) for city in cities]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return {
        city: result if not isinstance(result, Exception) else {"error": str(result)}
        for city, result in zip(cities, results)
    }
```

### 3. Connection Pooling

```python
# Reuse HTTP client across tool calls
class WeatherService:
    def __init__(self):
        # Connection pool for reuse
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(max_connections=100),
            timeout=httpx.Timeout(10.0)
        )
    
    async def close(self):
        await self.client.aclose()
```

---

## Security Considerations

### 1. API Key Management

```python
import os
from dotenv import load_dotenv

load_dotenv()

@api_key_validation
@mcp.tool()
async def call_external_api():
    api_key = os.getenv("API_KEY")
    if not api_key:
        return {"ok": False, "error": "API key not configured"}
    
    # Use api_key securely
    headers = {"Authorization": f"Bearer {api_key}"}
    # ...
```

### 2. Input Sanitization

```python
import re

def sanitize_sql_identifier(identifier: str) -> str:
    """Remove dangerous characters from SQL identifiers"""
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier):
        raise ValueError(f"Invalid identifier: {identifier}")
    return identifier
```

### 3. Rate Limiting per Client

```python
from collections import defaultdict

class PerClientRateLimiter:
    def __init__(self, rate: float):
        self.rate = rate
        self.limiters = defaultdict(RateLimiter)
    
    async def acquire(self, client_id: str):
        limiter = self.limiters[client_id]
        await limiter.acquire()
```

---

## Examples from This Project

### Week 3: Weather Server

**Location**: `week3/weather_server/`

**Key Patterns**:
- ✅ FastMCP for server setup
- ✅ Async HTTP client (httpx)
- ✅ Rate limiting (5 requests/sec)
- ✅ Error handling with consistent responses
- ✅ Resource for forecast data
- ✅ Tool for current weather

**Learn from**:
- [weather_server/main.py](../../week3/weather_server/main.py) - Tool definition
- [weather_server/weather_service.py](../../week3/weather_server/weather_service.py) - Service layer

---

## Related Resources

- [MCP Specification](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [LLM Integration Patterns](llm_integration_patterns.md)
- [Code Patterns](code_patterns.md)

---

## Changelog

| 日期 | 变更 | 作者 |
|------|------|------|
| 2025-01-19 | 初始版本，记录 MCP 服务器开发最佳实践 | AI Team |
