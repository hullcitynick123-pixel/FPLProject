"""Data processing and feature engineering module for FPL analytics."""

import urllib.parse
import pandas as pd
import streamlit as st
from api_client import APIFootballClient
import config

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

@st.cache_data(ttl=3600, show_spinner=False)
def get_league_table(season: int = config.DEFAULT_SEASON) -> pd.DataFrame:
    """Fetch and flatten the current Premier League standings."""
    client = APIFootballClient()
    response = client.fetch_standings(season=season)
    standings = response.get("response", [])
    if not standings:
        return pd.DataFrame()

    rows = standings[0].get("league", {}).get("standings", [[]])[0]
    if not rows:
        return pd.DataFrame()

    table = pd.DataFrame(
        [
            {
                "Rank": row.get("rank"),
                "Team": row.get("team", {}).get("name", ""),
                "Team_Logo": row.get("team", {}).get("logo"),
                "Played": row.get("all", {}).get("played"),
                "Won": row.get("all", {}).get("win"),
                "Drawn": row.get("all", {}).get("draw"),
                "Lost": row.get("all", {}).get("lose"),
                "GF": row.get("all", {}).get("goals", {}).get("for"),
                "GA": row.get("all", {}).get("goals", {}).get("against"),
                "GD": row.get("goalsDiff"),
                "Points": row.get("points"),
                "Form": row.get("form"),
            }
            for row in rows
        ]
    )
    return table