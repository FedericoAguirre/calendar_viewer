# Add MCP Server functionality

## Description

As an expert Python and ML Engineer, I want to add MCP Server functionality to expose calendar availability within a range of dates.

## Inputs

- Start and end dates.
- The Google calendar events (see fetch_events function in @src/calendar_api.py).
- Consider min and max hour, if not given the set from 10:00 to 17:00 for Monday, Wednesdays, and Thursdays; for Tuesdays and Fridays from 10:00 to 15:00 and from 10:00 to 20:00 in the weekends

## Outputs

- A list of empty time slots grouped by day and considering 1 full hour to reserve.

## Requirements

- Use the FastMCP Python package and add it to the project.
- Create a @src/mcp_server.py file to add the MCP server functionality.
- Add a section "MCP Server implementation" section in @READ.md with relevant links.
- Add a "MCP Server configuration" to use the server along with the **opencode** agent.
- Update @READ.md  to show up how to startup the MCP Server.

## Acceptance criteria

- The app works as a MCP server that shows calendar availability according the "Inputs" section.
- The @src/mcp_server.py file exists with required functionality.
- THe @READ.md file has the 3 updates mentioned in "Requirements" section.
