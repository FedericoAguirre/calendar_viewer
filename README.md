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
