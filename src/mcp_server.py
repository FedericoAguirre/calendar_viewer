import logging
from datetime import datetime, timedelta
from typing import Optional
from mcp.server.fastmcp import FastMCP
from calendar_api import fetch_events
import pytz

log = logging.getLogger(__name__)

TIMEZONE = pytz.timezone("America/Mexico_City")

DEFAULT_HOURS = {
    0: (10, 17),
    1: (10, 15),
    2: (10, 17),
    3: (10, 17),
    4: (10, 15),
    5: (10, 20),
    6: (10, 20),
}

mcp = FastMCP("Calendar Availability")


def _parse_event_time(event_time_str: str) -> datetime:
    try:
        return datetime.fromisoformat(event_time_str)
    except ValueError:
        return datetime.fromisoformat(event_time_str).replace(tzinfo=TIMEZONE)


def _is_busy(slot_start: datetime, slot_end: datetime, busy_ranges: list[tuple]) -> bool:
    for busy_start, busy_end in busy_ranges:
        if slot_start < busy_end and slot_end > busy_start:
            return True
    return False


@mcp.tool()
def get_availability(
    start_date: str,
    end_date: str,
    min_hour: Optional[int] = None,
    max_hour: Optional[int] = None,
) -> str:
    """Get available 1-hour time slots within a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format (inclusive).
        end_date: End date in YYYY-MM-DD format (inclusive).
        min_hour: Minimum hour (0-23) for all days. If omitted, uses
                  day-specific defaults (Mon/Wed/Thu 10-17, Tue/Fri 10-15,
                  weekends 10-20).
        max_hour: Maximum hour (0-23) for all days. Must be provided together
                  with min_hour.
    """
    start = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=TIMEZONE)
    end = datetime.strptime(end_date, "%Y-%m-%d").replace(
        hour=23, minute=59, second=59, tzinfo=TIMEZONE
    )

    events = fetch_events(start, end)

    busy_ranges = []
    for event in events:
        start_raw = event["start"].get("dateTime") or event["start"].get("date")
        end_raw = event["end"].get("dateTime") or event["end"].get("date")
        busy_start = _parse_event_time(start_raw)
        busy_end = _parse_event_time(end_raw)
        if busy_end <= busy_start:
            busy_end = busy_start + timedelta(hours=1)
        busy_ranges.append((busy_start, busy_end))

    result_lines = []
    current = start

    while current.date() <= end.date():
        weekday = current.weekday()
        day_label = current.strftime("%A, %Y-%m-%d")

        if min_hour is not None and max_hour is not None:
            day_min, day_max = min_hour, max_hour
        else:
            day_min, day_max = DEFAULT_HOURS.get(weekday, (10, 17))

        slot_start = current.replace(hour=day_min, minute=0, second=0, microsecond=0)
        day_slots = []

        while slot_start.hour < day_max:
            slot_end = slot_start + timedelta(hours=1)

            if not _is_busy(slot_start, slot_end, busy_ranges):
                day_slots.append(
                    f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                )

            slot_start = slot_end

        if day_slots:
            result_lines.append(f"{day_label}:")
            result_lines.extend(f"  {s}" for s in day_slots)

        current += timedelta(days=1)

    if not result_lines:
        return "No available time slots found in the given date range."

    return "\n".join(result_lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mcp.run(transport="stdio")
