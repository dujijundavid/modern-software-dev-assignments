#!/usr/bin/env python3
"""
Notion MCP Server - A Model Context Protocol server that wraps the Notion API.

Provides tools to interact with Notion databases, pages, and blocks through
a standardized MCP interface.
"""

import os
import json
import logging
import asyncio
from typing import Any, Optional
from datetime import datetime, timedelta

from dotenv import load_dotenv
import httpx
from mcp.server import Server, Request
from mcp.types import Tool, TextContent, ToolResponse
import mcp.types as types

# Load environment variables
load_dotenv()

# Configure logging (use stderr for STDIO mode)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Notion API Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_API_VERSION = "2024-05-15"
NOTION_BASE_URL = "https://api.notion.com/v1"

# Rate limiting
LAST_REQUEST_TIME = datetime.now()
MIN_REQUEST_INTERVAL = timedelta(seconds=0.34)  # ~3 req/sec limit


class NotionAPIClient:
    """Client for interacting with the Notion API."""

    def __init__(self, token: str):
        """Initialize the Notion API client.
        
        Args:
            token: Notion API integration token
        """
        if not token:
            raise ValueError("NOTION_TOKEN environment variable is required")
        
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        }
        self.client = httpx.Client(timeout=30.0)
        self.last_request_time = datetime.now()

    async def _rate_limit(self) -> None:
        """Enforce rate limiting (3 req/sec)."""
        now = datetime.now()
        time_since_last = now - self.last_request_time
        if time_since_last < MIN_REQUEST_INTERVAL:
            await asyncio.sleep(
                (MIN_REQUEST_INTERVAL - time_since_last).total_seconds()
            )
        self.last_request_time = datetime.now()

    async def _request(
        self, method: str, endpoint: str, data: Optional[dict] = None
    ) -> dict:
        """Make a request to the Notion API with rate limiting.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path
            data: Request body for POST/PATCH
            
        Returns:
            Parsed JSON response
            
        Raises:
            ValueError: For API errors
        """
        await self._rate_limit()
        
        url = f"{NOTION_BASE_URL}{endpoint}"
        
        try:
            if method == "GET":
                response = self.client.get(url, headers=self.headers)
            elif method == "POST":
                response = self.client.post(url, headers=self.headers, json=data)
            elif method == "PATCH":
                response = self.client.patch(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = self.client.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPStatusError as e:
            error_msg = f"Notion API Error ({e.response.status_code}): {e.response.text}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        except httpx.TimeoutException:
            raise ValueError("Notion API request timed out (30s)")
        except Exception as e:
            raise ValueError(f"Request failed: {str(e)}")

    async def query_database(
        self, database_id: str, filter_dict: Optional[dict] = None,
        sorts: Optional[list] = None, page_size: int = 10
    ) -> dict:
        """Query a Notion database.
        
        Args:
            database_id: ID of the database to query
            filter_dict: Filter criteria (Notion filter format)
            sorts: Sort order
            page_size: Number of results (1-100)
            
        Returns:
            Dictionary with results and metadata
        """
        page_size = min(max(page_size, 1), 100)
        payload = {"page_size": page_size}
        
        if filter_dict:
            payload["filter"] = filter_dict
        if sorts:
            payload["sorts"] = sorts
        
        result = await self._request("POST", f"/databases/{database_id}/query", payload)
        
        # Extract useful information from results
        pages = []
        for item in result.get("results", []):
            pages.append({
                "id": item["id"],
                "title": self._extract_title(item),
                "url": item.get("url"),
                "created_time": item.get("created_time"),
                "last_edited_time": item.get("last_edited_time"),
                "properties": item.get("properties", {}),
            })
        
        return {
            "database_id": database_id,
            "page_count": len(pages),
            "total_results": result.get("total_results", len(pages)),
            "has_more": result.get("has_more", False),
            "pages": pages,
        }

    async def get_page(self, page_id: str) -> dict:
        """Retrieve a Notion page's details.
        
        Args:
            page_id: ID of the page
            
        Returns:
            Page details including properties and content
        """
        page = await self._request("GET", f"/pages/{page_id}")
        
        # Retrieve blocks (page content)
        blocks = await self._request("GET", f"/blocks/{page_id}/children")
        
        return {
            "id": page["id"],
            "title": self._extract_title(page),
            "url": page.get("url"),
            "created_time": page.get("created_time"),
            "last_edited_time": page.get("last_edited_time"),
            "properties": page.get("properties", {}),
            "blocks_count": len(blocks.get("results", [])),
            "blocks": [self._extract_block_content(b) for b in blocks.get("results", [])],
        }

    async def create_page(
        self, parent_id: str, title: str, properties: Optional[dict] = None,
        content: Optional[list] = None
    ) -> dict:
        """Create a new Notion page in a database.
        
        Args:
            parent_id: ID of the parent database
            title: Page title
            properties: Additional page properties (Notion format)
            content: List of blocks to add to the page
            
        Returns:
            Created page details
        """
        payload = {
            "parent": {"database_id": parent_id},
            "properties": {
                "title": {
                    "title": [{"text": {"content": title}}]
                }
            }
        }
        
        # Add custom properties if provided
        if properties:
            payload["properties"].update(properties)
        
        page = await self._request("POST", "/pages", payload)
        
        # Add content blocks if provided
        if content:
            blocks_payload = {"children": content}
            await self._request("PATCH", f"/blocks/{page['id']}/children", blocks_payload)
        
        return {
            "id": page["id"],
            "title": title,
            "url": page.get("url"),
            "created": True,
        }

    async def update_page(self, page_id: str, properties: dict) -> dict:
        """Update a Notion page's properties.
        
        Args:
            page_id: ID of the page
            properties: Properties to update (Notion format)
            
        Returns:
            Updated page details
        """
        payload = {"properties": properties}
        page = await self._request("PATCH", f"/pages/{page_id}", payload)
        
        return {
            "id": page["id"],
            "title": self._extract_title(page),
            "url": page.get("url"),
            "updated": True,
            "last_edited_time": page.get("last_edited_time"),
        }

    @staticmethod
    def _extract_title(page: dict) -> str:
        """Extract title from Notion page properties."""
        props = page.get("properties", {})
        for prop in props.values():
            if prop.get("type") == "title":
                title_arr = prop.get("title", [])
                if title_arr:
                    return "".join([t.get("text", {}).get("content", "") for t in title_arr])
        return "Untitled"

    @staticmethod
    def _extract_block_content(block: dict) -> dict:
        """Extract content from a Notion block."""
        block_type = block.get("type")
        block_content = block.get(block_type, {})
        
        content = block_content.get("rich_text", [])
        text = "".join([t.get("text", {}).get("content", "") for t in content])
        
        return {
            "id": block["id"],
            "type": block_type,
            "content": text or f"[{block_type.upper()}]",
        }


# Initialize MCP Server
server = Server("notion-mcp-server")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="query_database",
            description="Query a Notion database for pages matching optional filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {
                        "type": "string",
                        "description": "ID of the Notion database to query"
                    },
                    "filter": {
                        "type": "string",
                        "description": "Optional filter in natural language (e.g., 'status is Done')"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results (1-100, default: 10)",
                        "default": 10
                    }
                },
                "required": ["database_id"]
            }
        ),
        Tool(
            name="get_page",
            description="Retrieve full details of a Notion page including its content",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "ID of the Notion page"
                    }
                },
                "required": ["page_id"]
            }
        ),
        Tool(
            name="create_page",
            description="Create a new page in a Notion database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_id": {
                        "type": "string",
                        "description": "ID of the parent database"
                    },
                    "title": {
                        "type": "string",
                        "description": "Title of the new page"
                    },
                    "properties": {
                        "type": "string",
                        "description": "JSON string with additional properties (optional)"
                    }
                },
                "required": ["database_id", "title"]
            }
        ),
        Tool(
            name="update_page",
            description="Update properties of an existing Notion page",
            inputSchema={
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "ID of the page to update"
                    },
                    "properties": {
                        "type": "string",
                        "description": "JSON string with properties to update"
                    }
                },
                "required": ["page_id", "properties"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool call."""
    
    if not NOTION_TOKEN:
        return [TextContent(type="text", text="Error: NOTION_TOKEN not configured")]
    
    try:
        client = NotionAPIClient(NOTION_TOKEN)
        
        if name == "query_database":
            database_id = arguments.get("database_id")
            if not database_id:
                return [TextContent(type="text", text="Error: database_id is required")]
            
            result = await client.query_database(
                database_id,
                page_size=arguments.get("page_size", 10)
            )
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "get_page":
            page_id = arguments.get("page_id")
            if not page_id:
                return [TextContent(type="text", text="Error: page_id is required")]
            
            result = await client.get_page(page_id)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "create_page":
            database_id = arguments.get("database_id")
            title = arguments.get("title")
            if not database_id or not title:
                return [TextContent(type="text", text="Error: database_id and title are required")]
            
            props = None
            if "properties" in arguments:
                try:
                    props = json.loads(arguments["properties"])
                except json.JSONDecodeError:
                    pass
            
            result = await client.create_page(database_id, title, props)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        elif name == "update_page":
            page_id = arguments.get("page_id")
            properties_str = arguments.get("properties")
            if not page_id or not properties_str:
                return [TextContent(type="text", text="Error: page_id and properties are required")]
            
            try:
                props = json.loads(properties_str)
            except json.JSONDecodeError:
                return [TextContent(type="text", text="Error: properties must be valid JSON")]
            
            result = await client.update_page(page_id, props)
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        logger.exception("Tool execution error")
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def main():
    """Start the MCP server."""
    logger.info("Starting Notion MCP Server...")
    
    # Verify Notion token is available
    if not NOTION_TOKEN:
        logger.error("NOTION_TOKEN environment variable not set")
        raise RuntimeError("NOTION_TOKEN is required")
    
    # Use stdio for local development
    logger.info("Running in STDIO mode")
    async with httpx.AsyncClient() as async_client:
        await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())
