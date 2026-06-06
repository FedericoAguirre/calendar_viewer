# Calendar viewer

## Description

**Calendar viewer** is a Python package (managed with [uv](https://docs.astral.sh/uv/)) that reads a personal Google Calendar and exposes events through a CLI and an MCP server.

It provides two entry points:

- **`calendar-export`** — CLI that exports the next working week's events to CSV.
- **`calendar-mcp`** — MCP server (stdio transport) with a `get_availability` tool that returns free 1-hour time slots within a date range.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python project manager.
- `credentials.json` — Google OAuth credentials file. Follow the [Google Workspace guide](https://developers.google.com/workspace/guides/create-credentials) to create one.

## Setup

1. Clone the repository:
```sh
git clone <repo-url>
cd calendar_viewer
```

2. Sync dependencies:
```sh
uv sync
```

3. Place your `credentials.json` file in the project root.

## Usage

### Export week's events to CSV

```sh
uv run calendar-export
```

### Start the MCP server

```sh
uv run calendar-mcp
```

The server starts on **stdio** and waits for MCP protocol messages from the client.

## Package

This project is a proper `uv` package. Build it with:

```sh
uv build
```

## MCP Server configuration

To use the MCP server with **opencode**, add this to `~/.config/opencode/mcp.json` or `.opencode/mcp.json`:

```json
{
  "mcpServers": {
    "calendar-availability": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/path/to/calendar_viewer",
        "calendar-mcp"
      ]
    }
  }
}
```

Replace `/path/to/calendar_viewer` with the absolute path to the project.

## Troubleshooting

### Google Authentication

**`Error 400: invalid_scope`**
The OAuth scope URL is incorrect. Ensure `SCOPES` in `src/calendar_api.py` uses a valid Google scope, e.g.:
```python
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
```

**`Error 400: policy_enforced` — "not approved by Advanced Protection"**
Your Google account has Advanced Protection enabled, which blocks unverified OAuth apps. Either:
- Use a Google account without Advanced Protection, or
- Disable Advanced Protection at https://myaccount.google.com
