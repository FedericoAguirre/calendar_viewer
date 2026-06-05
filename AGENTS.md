# AGENTS.md — Calendar Viewer

## Project structure

```
src/main.py          — CLI: exports this week's events to CSV
src/mcp_server.py    — MCP server (FastMCP, stdio transport)
src/calendar_api.py  — shared Google Calendar auth + fetch logic
```

## Commands

| What | Command |
|---|---|
| Install deps | `uv sync` |
| Run CSV export | `uv run python src/main.py` |
| Start MCP server | `uv run python src/mcp_server.py` |

Always use `uv run python ...` — the project requires `uv` and Python >=3.14 (see `.python-version`).

## MCP server details

- Built with `mcp>=1.0.0` (FastMCP), exposes one tool: `get_availability`
- Runs on **stdio** transport — must be launched by an MCP client (opencode, etc.)
- opencode config for `~/.config/opencode/mcp.json`:

```json
{
  "mcpServers": {
    "calendar-availability": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/calendar_viewer", "python", "src/mcp_server.py"]
    }
  }
}
```

## Auth (both entrypoints)

- Requires `credentials.json` (Google OAuth) in project root — **not checked in** (`.gitignore`)
- First run opens a browser for consent, then saves `token.json` locally (also gitignored)
- Google Advanced Protection blocks unverified OAuth apps — use a standard account

## Tooling

- **No** linter, formatter, type checker, or test framework configured in `pyproject.toml`
- No test files exist

## Key gotchas

- `credentials.json` and `token.json` are gitignored; an agent must remind the user to place `credentials.json` before attempting to run
- The duplicate `calendar_api.py` at root and `src/calendar_api.py` must be kept in sync — both are identical
