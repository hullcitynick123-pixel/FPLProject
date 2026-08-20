from datetime import datetime, timezone

import requests
import streamlit as st


def get_current_date() -> str:
    """Return the current date in 'Day DD Mon HH:MM:SS' format."""
    return datetime.now().strftime("%a %d %b %H:%M:%S")


@st.cache_data(ttl=300)  # Caches result for 5 minutes
def get_current_gameweek() -> dict:
    """Fetch the current (or next upcoming) Gameweek info from FPL API."""
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        events = data.get("events", [])

        # Find current active Gameweek, fallback to next upcoming GW (pre-season/post-deadline)
        gw_data = next((e for e in events if e.get("is_current")), None)
        if not gw_data:
            gw_data = next((e for e in events if e.get("is_next")), None)

        if gw_data:
            return {
                "id": gw_data.get("id"),
                "name": gw_data.get("name"),
                "deadline_time": gw_data.get("deadline_time"),
                "is_current": gw_data.get("is_current", False),
                "is_next": gw_data.get("is_next", False),
                "finished": gw_data.get("finished", False),
            }

        return {}

    except requests.exceptions.RequestException as exc:
        print(f"❌ Failed to fetch current Gameweek: {exc}")
        return {}


@st.cache_data(ttl=3600)
def get_gameweek_first_kickoff(gameweek_id: int) -> datetime | None:
    """Return the UTC kickoff time of the earliest fixture in a gameweek, or None."""
    url = "https://fantasy.premierleague.com/api/fixtures/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(url, params={"event": gameweek_id}, headers=headers, timeout=10)
        response.raise_for_status()
        fixtures = response.json()

        kickoff_times = [f["kickoff_time"] for f in fixtures if f.get("kickoff_time")]
        if not kickoff_times:
            return None

        earliest = min(kickoff_times)
        return datetime.strptime(earliest, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    except requests.exceptions.RequestException as exc:
        print(f"❌ Failed to fetch gameweek fixtures: {exc}")
        return None