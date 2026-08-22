from typing import Any

import requests
import re

import config


class APIFootballClient:
    """Client for managing API-Football authentication and network requests."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or config.API_KEY
        if not self.api_key:
            raise ValueError("API_FOOTBALL_KEY is missing or invalid in your .env file.")

        self.headers: dict[str, str] = {
            "x-apisports-key": self.api_key
        }

    def _request(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        """Shared request wrapper for API-Football endpoints."""
        url = f"{config.BASE_URL}/{endpoint}"

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data: dict[str, Any] = response.json()

            errors = data.get("errors")
            if errors and len(errors) > 0:
                print(f"⚠️ API Notice: {errors}")

            return data
        except requests.exceptions.RequestException as exc:
            print(f"❌ Network Request Failed: {exc}")
            raise

    def fetch_standings(
        self,
        league_id: int = config.DEFAULT_LEAGUE_ID,
        season: int = config.DEFAULT_SEASON
    ) -> dict[str, Any]:
        """Fetch the current league standings from API-Football."""
        params = {"league": league_id, "season": season}
        return self._request("standings", params)

    def fetch_fixtures_by_round(
        self,
        round_number: int,
        league_id: int = config.DEFAULT_LEAGUE_ID,
        season: int = config.DEFAULT_SEASON,
    ) -> dict[str, Any]:
        """Fetch fixtures for a specific matchweek/round from API-Football."""
        params = {
            "league": league_id,
            "season": season,
            "round": f"Regular Season - {round_number}",
        }
        return self._request("fixtures", params)

    def fetch_fixture_events(self, fixture_id: int) -> dict[str, Any]:
        """Fetch match events, including goals and scorers, for a fixture."""
        return self._request("fixtures/events", {"fixture": fixture_id})
    
    def fetch_player(self, player_name: str, league: int = config.DEFAULT_LEAGUE_ID, season: int = config.DEFAULT_SEASON) -> dict[str, Any]:
        """Fetch player details from API-Football."""
        params = {"search": self.clean_player_search_name(player_name), "league": league, "season": season}
        print(f"Fetching player data for '{player_name}' with params: {params}")
        return self._request("players", params)

    def clean_player_search_name(self, name: str) -> str:
        """Clean player search name."""
        cleaned = re.sub(r"[^A-Za-z0-9 ]+", " ", name)
        return " ".join(cleaned.split())

