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

4. Run the project (entry point: `main.py`):
```sh
uv run python main.py
```

## MCP Server implementation

The MCP server lives in [`src/mcp_server.py`](src/mcp_server.py) and is built with the [FastMCP](https://github.com/modelcontextprotocol/python-sdk) library from the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk). It exposes a single tool:

- **`get_availability`** — Given a date range (and optional hour overrides), it fetches Google Calendar events via [`calendar_api.py`](src/calendar_api.py) and returns available 1-hour free time slots.

The server runs over **stdio transport**, making it compatible with any MCP client (including **opencode**).

## Startup MCP Server

```sh
uv run python src/mcp_server.py
```

The server will start on **stdio** and wait for MCP protocol messages from the client.

## MCP Server configuration

To use this MCP server with the **opencode** agent, add the following entry to your opencode MCP configuration file (`~/.config/opencode/mcp.json` or project-local `.opencode/mcp.json`):

```json
{
  "mcpServers": {
    "calendar-availability": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/calendar_viewer",
        "python",
        "src/mcp_server.py"
      ]
    }
  }
}
```

Replace `/path/to/calendar_viewer` with the actual absolute path to this project. Once configured, the **opencode** agent will be able to call the `get_availability` tool to check calendar availability.

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
