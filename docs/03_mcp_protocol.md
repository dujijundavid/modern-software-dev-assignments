# MCP Protocol: Model Context Integration

## Quick Reference

**MCP (Model Context Protocol)** is an open standard for connecting AI models to external tools, data sources, and prompts through a unified interface.

**When to use MCP:**
- Building AI agents that need to access external APIs or databases
- Creating reusable tools that work across Claude Desktop, Cursor IDE, and other MCP-compatible clients
- Implementing standardized interfaces for LLM-powered applications

**Core capabilities:**
1. **Tools**: Executable functions (e.g., `get_weather`, `search_database`)
2. **Resources**: Data access (files, URLs, database queries)
3. **Prompts**: Reusable prompt templates

**Transport modes:**
- **STDIO**: Local communication via standard input/output (default for Claude Desktop)
- **HTTP/SSE**: Remote communication via HTTP with Server-Sent Events

---

## Core Concepts

### What is MCP?

MCP is a standardized protocol that solves the "information silo" problem in AI systems. It provides a bridge between Large Language Models (LLMs) and external APIs, enabling AI agents to:

- Access real-time data (weather, stock prices, news)
- Interact with external services (GitHub, Notion, databases)
- Execute multi-step workflows across multiple systems

**Before MCP:**
```
LangChain tools → Only work in LangChain
OpenAI functions → Manual format conversion
Custom integrations → Fragmented ecosystem
```

**After MCP:**
```
MCP Server → Claude Desktop ✅
           → Cursor IDE ✅
           → Any MCP-compatible client ✅
```

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     AI Application                           │
│                   (Claude Desktop, Cursor)                   │
└────────────────────┬────────────────────────────────────────┘
                     │ JSON-RPC over stdio/HTTP
┌────────────────────▼────────────────────────────────────────┐
│                    MCP Client                                │
│              (Protocol Implementation)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    MCP Server                                │
│             (Your Implementation)                            │
│  ┌─────────────┬──────────────┬─────────────────┐          │
│  │   Tools     │  Resources   │    Prompts       │          │
│  └──────┬──────┴──────┬───────┴────────┬────────┘          │
│         │             │                │                    │
└─────────┼─────────────┼────────────────┼────────────────────┘
          │             │                │
┌─────────▼─────────────▼────────────────▼────────────────────┐
│              External APIs & Services                        │
│  ┌────────────┬──────────────┬─────────────────┐           │
│  │  Weather   │    GitHub    │     Notion      │           │
│  │    API     │     API      │      API        │           │
│  └────────────┴──────────────┴─────────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

**1. Tools (Executable Functions)**
- Functions that AI models can call
- Type-safe parameters with automatic JSON Schema generation
- Clear descriptions for AI understanding

**2. Resources (Data Access)**
- Read-only access to data sources
- Identified by URIs (e.g., `file:///path/to/doc`)
- Useful for exposing files, URLs, or database queries

**3. Prompts (Template Management)**
- Reusable prompt templates
- Parameterized for dynamic content
- Consistent AI interactions

**4. Transport Layer**
- **STDIO**: Local process communication (default, most secure)
- **HTTP/SSE**: Remote communication (for cloud deployment)

### FastMCP Framework

FastMCP is the official Python framework for building MCP servers. It provides:

- **Decorator-based API**: Simple `@mcp.tool()` syntax
- **Automatic schema generation**: Type hints → JSON Schema
- **Type safety**: Python 3.10+ type checking
- **Async support**: Built-in async/await patterns

**Basic structure:**

```python
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("my-server")

# Define tool
@mcp.tool()
async def my_tool(param1: str, param2: int = 10) -> str:
    """Tool description that AI will read.

    Args:
        param1: Description of parameter 1
        param2: Description of parameter 2 (optional, default: 10)

    Returns:
        Human-readable result
    """
    return f"Received {param1} and {param2}"

# Start server
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

**Supported types:**

```python
@mcp.tool()
async def example(
    text: str,           # String (required)
    count: int = 10,     # Integer with default
    price: float,        # Float (required)
    active: bool = True, # Boolean with default
    value: str | int     # Union type (Python 3.10+)
) -> str:
    """FastMCP auto-generates JSON Schema from types."""
    pass
```

---

## Real-World Example: Building a Weather Server

### Problem Statement

Build an MCP server that provides AI models with access to weather data from the National Weather Service (NWS) API. The server should:

1. Fetch active weather alerts for any US state
2. Get detailed forecasts for any location (latitude/longitude)
3. Handle API errors gracefully
4. Work with Claude Desktop via STDIO transport

### Implementation

**Project structure:**
```
weather_server/
├── .venv/              # Virtual environment (not in git)
├── .python-version     # Pin Python version (3.13)
├── pyproject.toml      # Project configuration
├── uv.lock             # Dependency lock file
├── README.md           # Documentation
├── weather.py          # Main MCP server
└── test_server.py      # Test suite
```

**pyproject.toml:**
```toml
[project]
name = "weather"
version = "0.1.0"
description = "Weather MCP Server"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "httpx>=0.27.2",
    "mcp[cli]>=1.1.2",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**weather.py (complete implementation):**

```python
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Helper function with error handling
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make HTTP request to NWS API with error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # Log error (in production, use logging to stderr)
            return None

def format_alert(feature: dict) -> str:
    """Format alert feature into readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# Tool 1: Get weather alerts
@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get active weather alerts for a US state.

    Args:
        state: Two-letter state code (e.g., CA, NY, TX)

    Returns:
        Formatted string with active weather alerts
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    # Error handling
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    # Edge case: no alerts
    if not data["features"]:
        return "No active alerts for this state."

    # Format and return
    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

# Tool 2: Get weather forecast
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a specific location.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        Formatted weather forecast
    """
    # Step 1: Get forecast URL from points endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Step 2: Get actual forecast
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Step 3: Format forecast periods
    periods = forecast_data["properties"]["periods"]
    forecasts = []

    for period in periods[:5]:  # Show first 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)

# Start server
def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
```

### Testing

**test_server.py:**

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_weather_server():
    """Test MCP server tools programmatically."""
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "weather.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Test 1: Get weather alerts
            print("\nTest 1: California weather alerts")
            result = await session.call_tool("get_alerts", arguments={"state": "CA"})
            print(f"Result: {result.content[0].text[:200]}...")

            # Test 2: Get forecast
            print("\nTest 2: San Francisco forecast")
            result = await session.call_tool(
                "get_forecast",
                arguments={"latitude": 37.7749, "longitude": -122.4194}
            )
            print(f"Result: {result.content[0].text[:200]}...")

            print("\n✅ All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_weather_server())
```

**Run tests:**
```bash
cd weather_server
uv run test_server.py
```

### Deployment to Claude Desktop

**Step 1: Locate config file**
```bash
# macOS
~/Library/Application Support/Claude/claude_desktop_config.json

# Windows
%APPDATA%\Claude\claude_desktop_config.json
```

**Step 2: Add server configuration**
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/weather_server",
        "run",
        "weather.py"
      ]
    }
  }
}
```

**Step 3: Restart Claude Desktop**

**Step 4: Test in Claude**
```
User: "What are the current weather alerts in California?"
Claude: [Calls get_alerts tool automatically] → Returns formatted alerts
```

**With API keys (if needed):**
```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/weather_server",
        "run",
        "weather.py"
      ],
      "env": {
        "WEATHER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

---

## Best Practices

### 1. Clear Tool Descriptions

**DO:**
```python
@mcp.tool()
async def search_github_issues(query: str, repo: str) -> str:
    """Search GitHub issues in a repository.

    Args:
        query: Search query (e.g., "is:open bug")
        repo: Repository in format "owner/repo"

    Returns:
        Formatted list of matching issues
    """
```

**DON'T:**
```python
@mcp.tool()
async def search(query: str, repo: str) -> str:
    """Search stuff."""
    # AI won't know when to use this
```

### 2. Comprehensive Error Handling

**DO:**
```python
async def make_api_request(url: str) -> dict | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.TimeoutException:
        logger.error(f"Timeout fetching {url}")
        return None
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

**DON'T:**
```python
async def make_api_request(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)  # No timeout!
        return response.json()  # Crashes on error!
```

### 3. Type Safety

**DO:**
```python
@mcp.tool()
async def create_user(
    username: str,
    age: int,
    active: bool = True,
    metadata: dict[str, str] | None = None
) -> str:
    """Create a new user with typed parameters."""
```

**DON'T:**
```python
@mcp.tool()
async def create_user(**kwargs) -> str:
    """Create user - no type safety!"""
```

### 4. Logging (Never Use print!)

**DO:**
```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # Critical: log to stderr, not stdout
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@mcp.tool()
async def my_tool(param: str) -> str:
    logger.info(f"Tool called with param={param}")
    result = await do_work(param)
    logger.info(f"Tool completed successfully")
    return result
```

**DON'T:**
```python
@mcp.tool()
async def my_tool(param: str) -> str:
    print(f"Processing {param}")  # Breaks JSON-RPC protocol!
    return result
```

**Why?** MCP uses stdout for JSON-RPC communication. `print()` outputs to stdout, corrupting the protocol and breaking the connection.

### 5. Input Validation

**DO:**
```python
@mcp.tool()
async def get_alerts(state: str) -> str:
    # Validate state code format
    if len(state) != 2 or not state.isalpha():
        return "Invalid state code. Use 2-letter codes like CA, NY, TX."

    # Normalize input
    state = state.upper()

    # Proceed with validated input
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    # ...
```

### 6. Graceful Degradation

**DO:**
```python
@mcp.tool()
async def get_forecast(lat: float, lon: float) -> str:
    # Try primary API
    data = await fetch_from_primary(lat, lon)

    # Fallback to cache on error
    if not data:
        logger.warning("Primary API failed, using cache")
        data = get_cached_forecast(lat, lon)

    # Final fallback
    if not data:
        return "Unable to fetch forecast. Please try again later."

    return format_forecast(data)
```

---

## Common Pitfalls

### Pitfall 1: Forgetting `await` in Async Functions

**Problem:**
```python
result = make_nws_request(url)  # Returns coroutine object!
```

**Solution:**
```python
result = await make_nws_request(url)  # Awaits the async operation
```

**How to detect:** If you get `<coroutine object ...>` instead of actual data, you're missing `await`.

### Pitfall 2: Ignoring API Rate Limits

**Problem:**
```python
for item in large_list:
    await call_external_api(item)  # May get banned!
```

**Solution:**
```python
for i, item in enumerate(large_list):
    await call_external_api(item)
    if i % 10 == 0:
        await asyncio.sleep(1)  # Rate limiting
```

### Pitfall 3: Hardcoding API Keys

**Problem:**
```python
API_KEY = "sk-1234567890abcdef"  # Security risk!
```

**Solution:**
```python
import os

API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable not set")
```

**Set environment variable:**
```bash
# Temporarily
export WEATHER_API_KEY="your_key_here"
uv run weather.py

# Or use .env file (uv auto-loads)
echo "WEATHER_API_KEY=your_key_here" > .env
uv run weather.py
```

### Pitfall 4: Not Handling Empty Results

**Problem:**
```python
alerts = [format_alert(f) for f in data["features"]]
return "\n".join(alerts)  # Crashes if features is empty!
```

**Solution:**
```python
if not data.get("features"):
    return "No active alerts for this state."

alerts = [format_alert(f) for f in data["features"]]
return "\n".join(alerts)
```

### Pitfall 5: Returning Raw HTTP Errors to AI

**Problem:**
```python
except Exception as e:
    return f"Error: HTTPError 500 - {e}"  # Not user-friendly
```

**Solution:**
```python
except Exception as e:
    logger.error(f"Request failed: {e}")
    return "Unable to fetch data. Please check your input and try again."
```

### Pitfall 6: Blocking Operations in Async Functions

**Problem:**
```python
async def process_data():
    time.sleep(5)  # Blocks entire event loop!
    return result
```

**Solution:**
```python
async def process_data():
    await asyncio.sleep(5)  # Non-blocking
    return result
```

---

## Advanced Topics

### HTTP Transport (Remote Deployment)

For cloud deployment or team sharing, use HTTP/SSE transport instead of STDIO:

```python
def main():
    mcp.run(transport='sse', port=8000, host='0.0.0.0')
```

**Deployment platforms:**
- **Vercel**: [Deploy MCP Servers to Vercel](https://vercel.com/docs/mcp/deploy-mcp-servers-to-vercel)
- **Cloudflare**: [Remote MCP Server Guide](https://developers.cloudflare.com/agents/guides/remote-mcp-server/)
- **AWS/GCP/Azure**: Deploy as containerized service

### Adding Resources

```python
@mcp.resource("weather://alerts/{state}")
async def get_alerts_resource(state: str) -> str:
    """Expose weather alerts as a resource."""
    return await get_alerts(state)

# Usage: AI can read "weather://alerts/CA"
```

### Adding Prompts

```python
@mcp.prompt("weather_forecast_prompt")
async def weather_forecast_prompt(location: str) -> str:
    """Template for weather forecast queries."""
    return f"""What is the weather forecast for {location}?
Please provide:
1. Current conditions
2. Hourly forecast
3. Weekly outlook
"""
```

---

## Further Reading

### Official Documentation
- [MCP Official Documentation](https://modelcontextprotocol.io) - Complete protocol specification
- [FastMCP GitHub Repository](https://github.com/modelcontextprotocol/mcp) - Framework reference and examples
- [MCP Authorization Spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) - Authentication patterns

### Related Guides in This Repository
- [02_llm_integration.md](02_llm_integration.md) - LLM integration patterns and Ollama usage
- [05_testing_strategies.md](05_testing_strategies.md) - Testing methodologies for AI systems

### External Resources
- [uv Documentation](https://docs.astral.sh/uv/) - Modern Python package manager
- [httpx Documentation](https://www.python-httpx.org) - Async HTTP client
- [Python AsyncIO Tutorial](https://docs.python.org/3/library/asyncio.html) - Async programming fundamentals

---

## Quick Checklist

Before deploying your MCP server:

- [ ] All tools have clear docstrings with parameter descriptions
- [ ] Error handling covers timeouts, HTTP errors, and invalid input
- [ ] Logging uses `stderr` (not `print()` to stdout)
- [ ] Type hints are complete for all parameters
- [ ] API keys are loaded from environment variables
- [ ] Tests cover success cases and error scenarios
- [ ] Empty results are handled gracefully
- [ ] Rate limiting is implemented for external APIs
- [ ] Configuration uses absolute paths for deployment

---

**Last Updated:** 2026-01-02
**Contributors:** Consolidated from Week 3 learning materials and weather_server implementation
