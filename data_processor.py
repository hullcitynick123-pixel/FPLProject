"""Data processing and feature engineering module for FPL analytics."""

from typing import Any, Dict, List
import urllib.parse
import pandas as pd
import streamlit as st


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

@st.cache_data(ttl=300)
def fetch_draft_squads(sheet_id: str, tab_name: str = "current_squad") -> pd.DataFrame:
    """Fetch and slice the 10-manager squad matrix (Columns A-J, Rows 1-19)."""
    encoded_tab = urllib.parse.quote(tab_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"

    try:
        df = pd.read_csv(url)

        # 1. Slice first 10 columns (A to J: Seargent -> Browes)
        # 2. Slice first 18 data rows (Sheet rows 2 to 19)
        squads_df = df.iloc[0:18, 0:10]

        # Clean headers and remove string whitespace
        squads_df.columns = squads_df.columns.str.strip()
        squads_df = squads_df.map(
            lambda val: val.strip() if isinstance(val, str) else val
        )

        return squads_df
    except Exception as exc:
        print(f"❌ Failed to fetch draft squads: {exc}")
        return pd.DataFrame()

def get_manager_squad_by_position(squads_df: pd.DataFrame, manager_name: str) -> dict:
    """Extracts a manager's squad broken down by position."""
    if manager_name not in squads_df.columns:
        return {}

    # Extract single column and remove empty divider rows
    col = squads_df[manager_name].dropna()
    players = [p for p in col.tolist() if str(p).strip() != ""]

    if len(players) < 15:
        return {"ALL": players}

    return {
        "GOALKEEPER": players[0:2],
        "DEFENDER": players[2:7],
        "MIDFIELDER": players[7:12],
        "FORWARD": players[12:15],
    }


@st.cache_data(ttl=100)
def fetch_transfers(sheet_id: str, tab_name: str = "Transfers", gameweek: int = None) -> list:
    """Fetch transfer news from the Transfers sheet for a specific gameweek.
    
    Args:
        sheet_id: Google Sheets ID
        tab_name: Sheet tab name (default: "Transfers")
        gameweek: Gameweek number (default: uses first gameweek with data, or 1)
    
    Returns:
        List of transfer strings formatted as "Manager: Player Out → Player In"
    """
    encoded_tab = urllib.parse.quote(tab_name)
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_tab}"

    try:
        df = pd.read_csv(url)
        if df.empty:
            return []
        
        # First row should have manager names, columns have "Gameweek X" headers
        managers = df.iloc[:, 0].tolist()  # First column has manager names
        headers = df.columns.tolist()  # Column headers like "Gameweek 1", "Gameweek 2", etc.
        
        # Filter out metadata rows (anything after "Seargent" or that contains "Pick", "Time", "Slot")
        manager_rows = []
        for i, manager in enumerate(managers):
            if pd.isna(manager) or not str(manager).strip():
                continue
            manager_str = str(manager).strip()
            # Skip metadata rows
            if any(keyword in manager_str.lower() for keyword in ["pick", "time", "slot", "week complete", "1st pick ="]):
                continue
            manager_rows.append((i, manager_str))
        
        # Find gameweek column
        gameweek_col = None
        if gameweek is None:
            gameweek = 1  # Default to Gameweek 1
        
        target_gameweek = f"Gameweek {gameweek}"
        if target_gameweek in headers:
            gameweek_col = headers.index(target_gameweek)
        else:
            # Fallback to first gameweek column found
            for i, header in enumerate(headers):
                if "gameweek" in str(header).lower():
                    gameweek_col = i
                    break
        
        if gameweek_col is None:
            return []
        
        # Extract transfers for this gameweek
        transfers = []
        for row_idx, manager_name in manager_rows:
            transfer_data = df.iloc[row_idx, gameweek_col]
            if pd.notna(transfer_data) and str(transfer_data).strip():
                transfer_str = str(transfer_data).strip()
                transfers.append(f"{manager_name}: {transfer_str}")
        
        return transfers
    except Exception as exc:
        print(f"❌ Failed to fetch transfers: {exc}")
        return []