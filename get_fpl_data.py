import datetime as dt

import requests

FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


def parse_utc_datetime(value: str) -> dt.datetime:
    """Parse an ISO datetime string and always return a timezone-aware UTC datetime."""
    if not value:
        raise ValueError("Missing datetime value")

    if value.endswith("Z"):
        return dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)

    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def get_time_until_next_gameweek() -> str:
    """Return a formatted countdown to the next Premier League gameweek deadline."""
    try:
        response = requests.get(FPL_BOOTSTRAP_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return "NEXT GW: N/A"

    events = data.get("events", [])
    if not events:
        return "NEXT GW: N/A"

    now = dt.datetime.now(tz=dt.timezone.utc)
    next_event = None

    for event in sorted(events, key=lambda item: item.get("deadline_time", "")):
        deadline = event.get("deadline_time")
        if not deadline:
            continue
        deadline_dt = parse_utc_datetime(deadline)
        if deadline_dt >= now:
            next_event = event
            break

    if next_event is None:
        return "NEXT GW: SEASON DONE"

    deadline_dt = parse_utc_datetime(next_event["deadline_time"])
    total_seconds = max(0, int((deadline_dt - now).total_seconds()))
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    gameweek_id = next_event.get("id", "")
    return f"NEXT GW{gameweek_id}: {days}d {hours}h {minutes}m"


if __name__ == "__main__":
    print(get_time_until_next_gameweek())