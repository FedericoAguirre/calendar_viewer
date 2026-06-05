# Calendar viewer

## Description

**Calendar viewer** is a  *MCP Server implementation* to read a personal Google Calendar and get the events within a date range.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) - To manage this Python project.
- [credentials.json](https://developers.google.com/workspace/guides/create-credentials) file - To authenticate to Google using email and password.

## Startup project

1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd calendar_viewer
   ```

2. Sync the project dependencies:
   ```sh
   uv sync
   ```

3. Place your `credentials.json` file in the project root.

4. Run the project (entry point: `src/main.py`):
   ```sh
   uv run python src/main.py
   ```

5. Start the MCP Server (entry point: `src/mcp_server.py`):
   ```sh
   uv run python src/mcp_server.py
   ```

## MCP Server implementation

The project exposes calendar availability via the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) using the [FastMCP](https://github.com/modelcontextprotocol/python-sdk) Python SDK. The server provides a single tool:

- **`get_availability(start_date, end_date, [min_hour], [max_hour])`** — Returns free 1-hour time slots within a date range, respecting day-specific working hours:
  - Monday, Wednesday, Thursday: **10:00 – 17:00**
  - Tuesday, Friday: **10:00 – 15:00**
  - Weekends: **10:00 – 20:00**

See [`src/mcp_server.py`](src/mcp_server.py) for the implementation.

## MCP Server configuration

To use the calendar MCP server with the **opencode** agent, add the following to your `.opencode.json` in the project root:

```json
{
  "mcpServers": {
    "calendar-availability": {
      "command": "uv",
      "args": ["run", "python", "src/mcp_server.py"]
    }
  }
}
```

After configuring, restart opencode. The `get_availability` tool will be available for the agent to check your calendar availability.

## Troubleshooting

### Google Authentication

**`Error 400: invalid_scope`**
The OAuth scope URL is incorrect. Ensure `SCOPES` in `main.py` uses a valid Google scope, e.g.:
```python
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
```

**`Error 400: policy_enforced` — "not approved by Advanced Protection"**
Your Google account has Advanced Protection enabled, which blocks unverified OAuth apps. Either:
- Use a Google account without Advanced Protection, or
- Disable Advanced Protection at https://myaccount.google.com
