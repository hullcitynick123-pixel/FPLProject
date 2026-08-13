from typing import Any, Dict, Optional
import requests
import config

class APIFootballClient:
    """Client for managing API-Football authentication and network requests."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or config.API_KEY
        if not self.api_key:
            raise ValueError("API_FOOTBALL_KEY is missing or invalid in your .env file.")
            
        self.headers: Dict[str, str] = {
            "x-apisports-key": self.api_key
        }

    def fetch_standings(
        self,
        league_id: int = config.DEFAULT_LEAGUE_ID,
        season: int = config.DEFAULT_SEASON
    ) -> Dict[str, Any]:
        """Fetch the current league standings from API-Football."""
        url = f"{config.BASE_URL}/standings"
        params = {"league": league_id, "season": season}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data: Dict[str, Any] = response.json()

            errors = data.get("errors")
            if errors and len(errors) > 0:
                print(f"⚠️ API Notice: {errors}")

            return data
        except requests.exceptions.RequestException as exc:
            print(f"❌ Network Request Failed: {exc}")
            raise