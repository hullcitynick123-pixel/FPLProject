"""Page 308 - Ceefax Player Search & Profile Generator."""

import streamlit as st
import pandas as pd


def render_player_search_page(df: pd.DataFrame) -> None:
    """Render the Ceefax Player Lookup and Stat Profile view."""
    
    st.markdown(
        "<h1 style='color:#FFFF00; text-align:center;'>P308 PLAYER INDEX</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='color:#00FFFF; text-align:center;'>SELECT TEAM OR SEARCH PLAYER NAME</p>", 
        unsafe_allow_html=True
    )

    if df.empty:
        st.error("⚠️ NO PLAYER DATA AVAILABLE TO SEARCH.")
        return

    # --- Search & Filter Controls ---
    col_search, col_team = st.columns([2, 1])

    with col_team:
        teams = ["ALL TEAMS"] + sorted(df["Team"].dropna().unique().tolist())
        selected_team = st.selectbox("FILTER BY TEAM:", teams)

    # Filter dataframe by team first
    filtered_df = df.copy()
    if selected_team != "ALL TEAMS":
        filtered_df = filtered_df[filtered_df["Team"] == selected_team]

    with col_search:
        search_query = st.text_input("SEARCH PLAYER NAME:", "").strip().lower()

    if search_query:
        filtered_df = filtered_df[
            filtered_df["Player"].str.lower().str.contains(search_query)
        ]

    st.markdown("---")

    # --- Player Selector ---
    if filtered_df.empty:
        st.warning("⚠️ NO MATCHING PLAYERS FOUND ON PAGE 308.")
        return

    player_names = filtered_df["Player"].tolist()
    selected_player_name = st.selectbox("SELECT PLAYER TO INSPECT:", player_names)

    # Extract selected player record
    player_data = filtered_df[filtered_df["Player"] == selected_player_name].iloc[0]

    # --- Teletext Profile Display ---
    render_ceefax_player_card(player_data)


def render_ceefax_player_card(player: pd.Series) -> None:
    """Render a pixel-perfect Teletext stat profile for an individual player."""
    
    name = str(player.get("Player", "UNKNOWN")).upper()
    team = str(player.get("Team", "N/A")).upper()
    pos = str(player.get("Position", "N/A")).upper()
    minutes = player.get("Minutes", 0)
    goals = player.get("Goals", 0)
    xg_90 = player.get("xG_Per_90", 0.0)
    goals_90 = player.get("Goals_Per_90", 0.0)
    tackles_90 = player.get("Tackles_Per_90", 0.0)

    # Retro Teletext Player Header
    st.markdown(
        f"""
        <div style="background-color: #0000FF; padding: 10px; border: 2px solid #FFFF00; margin-bottom: 20px;">
            <h2 style="color: #FFFF00; margin: 0; font-size: 32px;">DOSSIER: {name}</h2>
            <p style="color: #FFFFFF; margin: 0; font-size: 22px;">
                TEAM: <span style="color:#00FF00;">{team}</span> | 
                POS: <span style="color:#00FFFF;">{pos}</span> | 
                MINS PLAYED: <span style="color:#FFFF00;">{minutes}</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Stat Grid
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("TOTAL GOALS", f"{goals}")
    m2.metric("GOALS / 90", f"{goals_90}")
    m3.metric("xG / 90 MINS", f"{xg_90}")
    m4.metric("TACKLES / 90", f"{tackles_90}")

    # Teletext Assessment Box
    st.markdown("<h3 style='color:#FF00FF; margin-top:25px;'>CEEFAX ANALYTICS VERDICT</h3>", unsafe_allow_html=True)
    
    # Simple rule-based verdict logic
    if xg_90 >= 0.5:
        verdict_color = "#00FF00"
        verdict = "HIGH GOAL THREAT - ELITE FPL OPTION"
    elif xg_90 >= 0.25:
        verdict_color = "#FFFF00"
        verdict = "MODERATE THREAT - SOLID SQUAD ROTATION"
    else:
        verdict_color = "#FF0000"
        verdict = "LOW ATTACKING OUTPUT - MONITOR FIXTURES"

    st.markdown(
        f"""
        <div style="border: 2px dashed {verdict_color}; padding: 12px; background-color: #000000;">
            <span style="color: {verdict_color}; font-size: 24px; font-weight: bold;">
                >>> {verdict}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )