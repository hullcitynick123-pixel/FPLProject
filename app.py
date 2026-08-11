"""Streamlit Dashboard for Premier League & FPL Analytics."""

import streamlit as st
import pandas as pd
import plotly.express as px

import config
from api_client import APIFootballClient
from data_processor import parse_player_raw_data, calculate_per_90_metrics
from ceefax_theme import inject_ceefax_styles, render_ceefax_header


# --- Page Configuration ---
st.set_page_config(
    page_title="CEEFAX P302 - FPL STATS",
    page_icon="📺",
    layout="wide"
)

# --- Injecting Ceefax Styles ---
inject_ceefax_styles()

# --- Cached Data Fetching ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_player_data(season: int) -> pd.DataFrame:
    """Fetch raw API data, parse, and engineer metrics with 1-hour cache."""
    client = APIFootballClient()
    raw_response = client.fetch_top_scorers(season=season)
    raw_df = parse_player_raw_data(raw_response)
    if raw_df.empty:
        return pd.DataFrame()
    
    # Process base metrics with minimum 1 minute played
    processed_df = calculate_per_90_metrics(raw_df, min_minutes=1)
    return processed_df


def main() -> None:
    # Render authentic Ceefax Top Bar
    render_ceefax_header(page_num=302, title="FPL ANALYTICS")

    st.markdown("<h1 style='color:#FFFF00; text-align:center;'>P302 BBC CEEFAX PREMIER LEAGUE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00FFFF; text-align:center;'>FANTASY FOOTBALL STATISTICAL INDEX 2025/26</p>", unsafe_allow_html=True)

    # --- Fastext Navigation Bar (Red, Green, Yellow, Blue Buttons) ---
    st.markdown("---")
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    btn_col1.button("303 TOP SCORERS")
    btn_col2.button("304 xG THREAT")
    btn_col3.button("305 TACKLES")
    btn_col4.button("306 FULL TABLE")
    st.markdown("---")

    # Load player data using existing pipeline
    client = APIFootballClient()
    raw_data = client.fetch_top_scorers(season=config.DEFAULT_SEASON)
    raw_df = parse_player_raw_data(raw_data)
    df = calculate_per_90_metrics(raw_df, min_minutes=90)

    if not df.empty:
        # Key Teletext Data Cards
        col1, col2, col3 = st.columns(3)
        top_scorer = df.sort_values(by="Goals", ascending=False).iloc[0]
        top_xg = df.sort_values(by="xG_Per_90", ascending=False).iloc[0]

        col1.metric("LEADING SCORER", top_scorer["Player"], f"{top_scorer['Goals']} GOALS")
        col2.metric("HIGHEST xG/90", top_xg["Player"], f"{top_xg['xG_Per_90']}")
        col3.metric("TOTAL PLAYERS", len(df))

        st.markdown("<h2 style='color:#00FF00; margin-top:20px;'>PLAYER PERFORMANCE MATRIX</h2>", unsafe_allow_html=True)
        
        # Display table with black/green teletext feel
        st.dataframe(
            df[["Player", "Team", "Position", "Minutes", "Goals", "Goals_Per_90", "xG_Per_90", "Tackles_Per_90"]],
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()