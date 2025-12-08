# Notion MCP Server

A Model Context Protocol (MCP) server that provides tools to interact with Notion databases, pages, and content.

## Features

- **Query Databases**: Search and filter pages in Notion databases
- **Get Page Details**: Retrieve full page content with blocks
- **Create Pages**: Create new pages in databases with custom properties
- **Update Pages**: Modify page properties
- **Rate Limiting**: Built-in respect for Notion API rate limits (3 req/sec)
- **Error Handling**: Graceful handling of timeouts, API errors, and empty results
- **Logging**: Comprehensive logging for debugging and monitoring

## Prerequisites

- Python 3.8+
- Notion API token (Integration)
- Access to a Notion database

## Setup

### 1. Create a Notion Integration

1. Go to [notion.com/my-integrations](https://notion.com/my-integrations)
2. Click "Create new integration"
3. Name it "Notion MCP Server"
4. Copy the "Internal Integration Token"
5. Share your Notion databases with this integration

### 2. Install Dependencies

```bash
cd week3/server
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file in the `server/` directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your Notion token:

```env
NOTION_TOKEN=ntn_xxx...
MCP_MODE=stdio
LOG_LEVEL=INFO
```

### 4. Get Your Database ID

In Notion, open any database and copy the ID from the URL:
```
notion.com/workspace/DATABASE_ID?v=view_id
                     ^^^^^^^^^^
                     This is the database ID
```

## Running Locally (STDIO Mode)

### Option 1: Direct Python

```bash
cd week3/server
python main.py
```

### Option 2: Claude Desktop Integration

1. Install Claude Desktop if not already installed
2. Edit Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "notion": {
      "command": "python",
      "args": ["/path/to/week3/server/main.py"],
      "env": {
        "NOTION_TOKEN": ""
      }
    }
  }
}
```

3. Restart Claude Desktop
4. You should see the Notion tools available in Claude's tool menu

### Option 3: Cursor IDE

Similar setup to Claude Desktop - configure in your Cursor settings to use the MCP server.

## Tool Reference

### 1. `query_database`

Query a Notion database for pages matching optional filters.

**Parameters:**
- `database_id` (string, required): ID of the Notion database
- `filter` (string, optional): Natural language filter description
- `page_size` (integer, optional): Number of results (1-100, default: 10)

**Example Usage:**
```
Tool: query_database
Parameters:
  database_id: "abc123def456"
  page_size: 20
```

**Sample Output:**
```json
{
  "database_id": "abc123def456",
  "page_count": 3,
  "total_results": 10,
  "has_more": true,
  "pages": [
    {
      "id": "page_id_1",
      "title": "Project Alpha",
      "url": "https://notion.so/...",
      "created_time": "2024-01-15T10:30:00.000Z",
      "last_edited_time": "2024-12-08T15:45:00.000Z",
      "properties": {...}
    }
  ]
}
```

### 2. `get_page`

Retrieve full details of a Notion page including its content blocks.

**Parameters:**
- `page_id` (string, required): ID of the Notion page

**Example Usage:**
```
Tool: get_page
Parameters:
  page_id: "page_id_1"
```

**Sample Output:**
```json
{
  "id": "page_id_1",
  "title": "Project Alpha",
  "url": "https://notion.so/...",
  "created_time": "2024-01-15T10:30:00.000Z",
  "last_edited_time": "2024-12-08T15:45:00.000Z",
  "blocks_count": 5,
  "blocks": [
    {
      "id": "block_1",
      "type": "heading_1",
      "content": "Main Title"
    },
    {
      "id": "block_2",
      "type": "paragraph",
      "content": "This is the page content"
    }
  ],
  "properties": {...}
}
```

### 3. `create_page`

Create a new page in a Notion database.

**Parameters:**
- `database_id` (string, required): ID of the parent database
- `title` (string, required): Title of the new page
- `properties` (string, optional): JSON string with additional properties

**Example Usage:**
```
Tool: create_page
Parameters:
  database_id: "abc123def456"
  title: "New Project Ideas"
  properties: "{\"status\": {\"select\": {\"name\": \"Planning\"}}}"
```

**Sample Output:**
```json
{
  "id": "new_page_id",
  "title": "New Project Ideas",
  "url": "https://notion.so/...",
  "created": true
}
```

### 4. `update_page`

Update properties of an existing Notion page.

**Parameters:**
- `page_id` (string, required): ID of the page to update
- `properties` (string, required): JSON string with properties to update

**Example Usage:**
```
Tool: update_page
Parameters:
  page_id: "page_id_1"
  properties: "{\"status\": {\"select\": {\"name\": \"Done\"}}}"
```

**Sample Output:**
```json
{
  "id": "page_id_1",
  "title": "Project Alpha",
  "url": "https://notion.so/...",
  "updated": true,
  "last_edited_time": "2024-12-08T16:00:00.000Z"
}
```

## Example Invocation Flow

### Scenario: Tracking Projects in Claude

1. **List all projects** (STDIO via Claude Desktop):
   ```
   User: "Show me all projects in my Notion database"
   
   Claude uses: query_database with your database_id
   
   Output: [List of projects with titles, URLs, status, etc.]
   ```

2. **Create a new project**:
   ```
   User: "Create a new project called 'Website Redesign' with status 'Planning'"
   
   Claude uses: create_page with the database_id and title
   
   Output: Confirmation with the new page URL
   ```

3. **Check project details**:
   ```
   User: "Show me the full details of 'Website Redesign'"
   
   Claude uses: get_page with the page_id
   
   Output: Full page content including blocks and properties
   ```

4. **Update project status**:
   ```
   User: "Mark the Website Redesign project as In Progress"
   
   Claude uses: update_page with new status property
   
   Output: Confirmation of update with new edit time
   ```

## Error Handling

The server handles the following gracefully:

- **Missing NOTION_TOKEN**: Returns an error message
- **Invalid database/page IDs**: Returns API error from Notion
- **Timeout (30s)**: Returns timeout error message
- **Rate limit (3 req/sec)**: Automatically backs off
- **Empty results**: Returns empty pages array
- **Invalid JSON in properties**: Returns JSON decode error
- **Network errors**: Returns detailed error message

## Logging

Logs are written to stderr (for STDIO mode compatibility) with format:
```
2024-12-08 16:00:00,123 - __main__ - INFO - Starting Notion MCP Server...
```

Check logs for:
- Rate limit enforcement
- API request/response details
- Tool execution flow
- Error stack traces

## Resilience Features

1. **Rate Limiting**: Enforces 3 req/sec Notion API limit with automatic delays
2. **Timeout Protection**: All requests have 30-second timeout
3. **Input Validation**: Required parameters are checked before API calls
4. **Error Messages**: Clear, actionable error messages for debugging
5. **Graceful Degradation**: Partial failures don't crash the server

## Development Notes

- Uses `httpx` for async HTTP requests
- Uses `mcp` library for Model Context Protocol implementation
- Uses `python-dotenv` for environment configuration
- All async/await for non-blocking operations
- Type hints throughout for code clarity

## Future Enhancements

- [ ] HTTP transport mode with authentication
- [ ] Support for Notion Users API
- [ ] Batch operations
- [ ] Full-text search across databases
- [ ] Webhook support for real-time updates
- [ ] Caching layer for frequently accessed pages
- [ ] OAuth2 authentication flow

## Security Notes

- **NEVER commit `.env` file to git** - use `.env.example` instead
- Store API tokens securely (environment variables, secure vaults)
- Tokens should have minimal required permissions
- For HTTP deployment, implement proper authentication

## Troubleshooting

### MCP Server not appearing in Claude Desktop

1. Check JSON syntax in `claude_desktop_config.json`
2. Verify the Python path is correct
3. Check that `.env` file has valid NOTION_TOKEN
4. Restart Claude Desktop completely
5. Check Claude Desktop logs for errors

### API returns "Invalid Grant"

- Notion token may be expired or invalid
- Regenerate token from notion.com/my-integrations
- Ensure integration has access to the database (share with integration)

### Timeout errors

- Notion API might be slow or experiencing issues
- Check your network connection
- Try again after a few seconds

### Rate limit warnings

- The server automatically backs off - this is normal
- If you hit limits frequently, reduce page_size or requests

## References

- [MCP Documentation](https://modelcontextprotocol.io)
- [Notion API Documentation](https://developers.notion.com)
- [Notion API Rate Limits](https://developers.notion.com/reference/request-limits)
