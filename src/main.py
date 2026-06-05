import logging
import csv
from datetime import datetime, timedelta
import pytz

from src.calendar_api import fetch_events

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

TIMEZONE = pytz.timezone("America/Mexico_City")

now = datetime.now(TIMEZONE)
days_until_monday = (0 - now.weekday() + 7) % 7
if days_until_monday == 0:
    days_until_monday = 7

week_start = (now + timedelta(days=days_until_monday)).replace(
    hour=0, minute=0, second=0, microsecond=0
)
week_end = (week_start + timedelta(days=5)).replace(
    hour=23, minute=59, second=59, microsecond=0
)


def convert_to_csv(events: list[dict], filename: str = "calendar_events.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Start", "End"])

        for event in events:
            title = event.get("summary", "No title")
            start_raw = event["start"].get("dateTime", event["start"].get("date"))
            end_raw = event["end"].get("dateTime", event["end"].get("date"))

            start_clean = start_raw.replace("T", " ").split(".")[0]
            end_clean = end_raw.replace("T", " ").split(".")[0]

            writer.writerow([title, start_clean, end_clean])

    log.info(f"Export successful! Data saved to '{filename}'.")


if __name__ == "__main__":
    events = fetch_events(week_start, week_end)
    if events:
        convert_to_csv(events)
