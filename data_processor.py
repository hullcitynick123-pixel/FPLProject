"""Data processing and feature engineering module for FPL analytics."""

from typing import Any, Dict, List
import pandas as pd


def parse_player_raw_data(api_response: Dict[str, Any]) -> pd.DataFrame:
    """Convert raw API-Football JSON response into a clean Pandas DataFrame."""
    records: List[Dict[str, Any]] = api_response.get("response", [])
    if not records:
        return pd.DataFrame()

    parsed_players: List[Dict[str, Any]] = []

    for item in records:
        player = item.get("player", {})
        stats = item.get("statistics", [{}])[0]

        minutes = stats.get("games", {}).get("minutes") or 0
        goals = stats.get("goals", {}).get("total") or 0
        assists = stats.get("goals", {}).get("assists") or 0
        tackles = stats.get("tackles", {}).get("total") or 0

        # Parse xG safely
        raw_xg = stats.get("goals", {}).get("expected")
        xg = float(raw_xg) if raw_xg is not None else 0.0

        parsed_players.append({
            "Player": player.get("name", "Unknown"),
            "Team": stats.get("team", {}).get("name", "Unknown"),
            "Position": stats.get("games", {}).get("position", "N/A"),
            "Minutes": minutes,
            "Goals": goals,
            "Assists": assists,
            "xG": round(xg, 2),
            "Tackles": tackles,
            "Rating": float(stats.get("games", {}).get("rating") or 0.0),
        })

    return pd.DataFrame(parsed_players)


def calculate_per_90_metrics(df: pd.DataFrame, min_minutes: int = 90) -> pd.DataFrame:
    """Normalize statistics per 90 minutes played for fair comparisons."""
    if df.empty or "Minutes" not in df.columns:
        return df

    # Filter out players below minimum minutes threshold
    filtered_df = df[df["Minutes"] >= min_minutes].copy()

    filtered_df["90s_Played"] = (filtered_df["Minutes"] / 90.0).round(2)

    # Per 90 metrics
    filtered_df["Goals_Per_90"] = (filtered_df["Goals"] / filtered_df["90s_Played"]).round(2)
    filtered_df["xG_Per_90"] = (filtered_df["xG"] / filtered_df["90s_Played"]).round(2)
    filtered_df["Tackles_Per_90"] = (filtered_df["Tackles"] / filtered_df["90s_Played"]).round(2)

    # Over/Under performance against Expected Goals
    filtered_df["xG_Delta"] = (filtered_df["Goals"] - filtered_df["xG"]).round(2)

    return filtered_df