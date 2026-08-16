from typing import Any

import requests

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

    def fetch_player(self, player_name: str, league: int = config.DEFAULT_LEAGUE_ID, season: int = config.DEFAULT_SEASON) -> dict[str, Any]:
        """Fetch player details from API-Football."""
        params = {"search": player_name, "league": league, "season": season}
        return self._request("players", params)

    def fetch_player_stats(
        self,
        player_id: int,
        league: int = config.DEFAULT_LEAGUE_ID,
        season: int = config.DEFAULT_SEASON,
    ) -> dict[str, Any]:
        """Fetch a single player's detailed stats for a season."""
        params = {"id": player_id, "league": league, "season": season}
        return self._request("players", params)