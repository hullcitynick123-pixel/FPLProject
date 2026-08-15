"""Streamlit Dashboard for Premier League & FPL Analytics."""

import pandas as pd
import streamlit as st

import config
from ceefax_theme.ceefax_header import render_ceefax_header
from ceefax_theme.ceefax_theme import inject_ceefax_styles
from data_processor import (
    fetch_draft_squads,
    fetch_transfers,
    get_fantasy_league_table,
    get_league_table,
    get_manager_squad_by_position,
)
from fpl_constants import MANAGER_TEAMS
from utils.date import get_current_gameweek
from utils.news_flavor import build_dynamic_feed

# --- Page Configuration ---
st.set_page_config(
    page_title="CEEFAX P302 - FPL STATS",
    page_icon="📺",
    layout="wide"
)

sheet_id = config.SHEET_ID
tab_name = config.SQUAD_SHEET_NAME

# --- Inject Ceefax Styles ---
inject_ceefax_styles()

def render_transfer_feed() -> None:
    """Render a rolling transfer news feed at the top of the page."""
    try:
        current_gameweek = get_current_gameweek()
        transfers = fetch_transfers(sheet_id=sheet_id, tab_name=config.TRANSFERS_SHEET_NAME, gameweek=current_gameweek["id"])
        transfers = build_dynamic_feed(transfers, gameweek_id=current_gameweek.get("id", 0))
    except Exception as e:
        print(f"Failed to fetch transfers: {e}")
        transfers = []
    
    if not transfers:
        return
    
    # Create transfer text without duplication
    transfer_text = " • ".join(transfers)
    
    # CSS for marquee scrolling effect
    marquee_html = f"""
    <style>
        @keyframes scroll {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-100%); }}
        }}
        .transfer-marquee {{
            background-color: #000000;
            color: #FF00FF;
            border: 2px solid #FF00FF;
            padding: 12px 10px;
            font-family: 'VT323', monospace;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
            overflow: hidden;
            white-space: nowrap;
            margin-top: 0;
            margin-bottom: 8px;
        }}
        .transfer-scroll {{
            display: inline-block;
            animation: scroll 45s linear infinite;
            padding-right: 50px;
        }}
        .transfer-scroll:hover {{
            animation-play-state: paused;
        }}
    </style>
    <div class="transfer-marquee">
        <span class="transfer-scroll">{transfer_text}</span>
    </div>
    """
    
    st.markdown(marquee_html, unsafe_allow_html=True)

def render_fantasy_squad_page() -> None:
    """Render the Fantasy Squads page with manager selections."""
    st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>FANTASY SQUADS</h2>", unsafe_allow_html=True)

    try:
        squads_df = fetch_draft_squads(sheet_id=sheet_id, tab_name=tab_name)
    except Exception as e:
        st.error(f"Failed to fetch fantasy squads: {e}")
        return

    if squads_df.empty:
        st.warning("No squad data available.")
        return

    # Build each squad card as raw HTML in a CSS grid so column count is fully
    # controlled by CSS (not Streamlit's own inline column widths), which lets
    # the mobile media query reliably collapse it to one card per row.
    managers = list(squads_df.columns)
    cards_html = []
    for manager_name in managers:
        team_name = MANAGER_TEAMS.get(manager_name, manager_name)

        squad_dict = get_manager_squad_by_position(squads_df, manager_name)
        if not squad_dict:
            cards_html.append(
                f"<div class='squad-card'><p style='color:#00FFFF;'>No squad data for {manager_name}.</p></div>"
            )
            continue

        squad_data = []
        for position, players in squad_dict.items():
            for player in players:
                squad_data.append({"Position": position, "Player": player})

        rows_html = "".join(
            f"<tr><td>{item['Position']}</td><td>{item['Player']}</td></tr>" for item in squad_data
        )
        table_html = build_ceefax_table_html(
            ["POSITION", "PLAYER"],
            [rows_html],
            extra_css="""
            .ceefax-table-shell {
                width: 100%;
                margin: 0;
                padding: 0;
            }
            .ceefax-table {
                table-layout: auto;
                font-size: 16px;
                min-width: 180px;
            }
            .ceefax-table th, .ceefax-table td {
                padding: 3px 5px;
                white-space: nowrap;
            }
            """,
        )

        header_html = (
            f"<div style='text-align:center; width:100%;'>"
            f"<h3 style='color:#FFFF00; margin:0 0 4px 0; padding:0;'>{team_name}</h3>"
            f"<p style='color:#00FFFF; margin:0 0 8px 0; padding:0; font-size:11px;'>(Manager: {manager_name})</p>"
            f"</div>"
        )

        cards_html.append(f"<div class='squad-card'>{header_html}{table_html}</div>")

    grid_html = f"""
    <style>
        .squad-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
        }}
        .squad-card {{
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 0;
            overflow-x: auto;
        }}
        @media (max-width: 768px) {{
            .squad-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    <div class="squad-grid">{''.join(cards_html)}</div>
    """
    st.markdown(grid_html, unsafe_allow_html=True)

def build_ceefax_table_html(headers: list[str], rows_html: list[str], extra_css: str = "") -> str:
    """Build a compact Ceefax-style table with optional table-specific CSS."""
    table_html = f"""
    <style>
        .ceefax-table-shell {{
            width: min(100%, 820px);
            margin: 18px auto 40px;
            padding: 10px 12px 12px;
            background: #000000;
        }}
        .ceefax-table {{
            width: 100%;
            border-collapse: collapse;
            background: #000000;
            color: #FFFFFF;
            font-family: 'VT323', monospace;
            font-size: 19px;
            table-layout: fixed;
        }}
        .ceefax-table th, .ceefax-table td {{
            border: 0;
            border-bottom: 1px solid #073807;
            padding: 3px 5px;
            text-align: center;
            vertical-align: middle;
            line-height: 1.05;
        }}
        .ceefax-table th {{
            background: #0000FF;
            color: #FFFFFF;
            text-transform: uppercase;
            font-size: 17px;
            padding: 4px 5px;
        }}
        .ceefax-table tr:hover td {{
            background: #001c00;
            color: #FFFFFF !important;
        }}
        {extra_css}
        @media (max-width: 768px) {{
            .ceefax-table-shell {{ padding: 7px; }}
            .ceefax-table {{ font-size: 14px; }}
            .ceefax-table th {{ font-size: 13px; }}
            .ceefax-table th, .ceefax-table td {{ padding: 3px 2px; }}
        }}
    </style>
    <div class="teletext-table-wrapper">
    <div class="ceefax-table-shell">
    <table class='ceefax-table'>
        <thead>
            <tr>{''.join(f'<th>{header}</th>' for header in headers)}</tr>
        </thead>
        <tbody>
            {''.join(rows_html)}
        </tbody>
    </table>
    </div>
    </div>
    """
    return table_html

def render_ceefax_table(headers: list[str], rows_html: list[str], extra_css: str = "") -> None:
    """Render a compact Ceefax-style table with optional table-specific CSS."""
    st.markdown(build_ceefax_table_html(headers, rows_html, extra_css), unsafe_allow_html=True)

def render_league_table() -> None:
    """Render the current Premier League standings table with zone borders."""
    table = get_league_table(season=config.DEFAULT_SEASON)

    if table.empty:
        st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>CURRENT PREMIER LEAGUE TABLE</h2>", unsafe_allow_html=True)
        st.warning("Standings are unavailable right now.")
        return

    headers = ["POS", "TEAM", "P", "W", "D", "L", "GF", "GA", "GD", "PTS", "FORM"]
    rows_html = []

    for _, row in table.iterrows():
        rank = int(row['Rank'])

        # Teletext zone colors & section bottom dividers
        zone_color = "#00FF00"  # Default Teletext Green
        divider_css = ""

        if rank <= 4:
            zone_color = "#00FFFF"  # Champions League (Teletext Cyan)
            if rank == 4:
                divider_css = "border-bottom: 2px solid #00FFFF !important;"
        elif rank == 5:
            zone_color = "#FFFF00"  # Europa League (Teletext Yellow)
            divider_css = "border-bottom: 2px solid #FFFF00 !important;"
        elif rank == 6:
            zone_color = "#00FFFF"  # Conference League (Teletext Cyan)
            divider_css = "border-bottom: 2px solid #00FFFF !important;"
        elif rank >= 18:
            zone_color = "#FF0000"  # Relegation (Teletext Red)
        elif rank == 17:
            divider_css = "border-bottom: 2px solid #FF0000 !important;"

        # Row border style
        row_style = f"style='--zone-color: {zone_color}; {divider_css}'"

        team_logo = row.get("Team_Logo") or ""
        team_name = row.get("Team") or ""
        team_cell = (
            f"<div class='team-cell'><img src='{team_logo}' alt='{team_name}' /><span>{team_name}</span></div>"
            if team_logo
            else f"<div class='team-cell'><span>{team_name}</span></div>"
        )

        rows_html.append(
            f"<tr {row_style}>"
            f"<td class='position' style='color: {zone_color};'>{rank}</td>"
            f"<td>{team_cell}</td>"
            f"<td>{int(row['Played'])}</td>"
            f"<td>{int(row['Won'])}</td>"
            f"<td>{int(row['Drawn'])}</td>"
            f"<td>{int(row['Lost'])}</td>"
            f"<td>{int(row['GF'])}</td>"
            f"<td>{int(row['GA'])}</td>"
            f"<td>{int(row['GD'])}</td>"
            f"<td>{int(row['Points'])}</td>"
            f"<td>{row['Form']}</td>"
            "</tr>"
        )
    st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>LIVE PREMIER LEAGUE TABLE</h2>", unsafe_allow_html=True)
    render_ceefax_table(
        headers,
        rows_html,
        extra_css="""
        .ceefax-table-shell {
            width: min(100%, 1400px);
        }
        .ceefax-table {
            font-size: 23px;
        }
        .ceefax-table th, .ceefax-table td {
            padding: 6px 10px;
        }
        .ceefax-table th:nth-child(2), .ceefax-table td:nth-child(2) {
            width: 36%;
            text-align: left;
        }
        .ceefax-table tr {
            border-left: 5px solid var(--zone-color);
        }
        .ceefax-table .position {
            font-weight: bold;
            width: 7%;
        }
        .team-cell {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 6px;
            text-align: left;
            color: #FFFFFF;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .team-cell img {
            width: 18px;
            height: 18px;
            display: block;
        }
        @media (max-width: 768px) {
            .ceefax-table th:nth-child(2), .ceefax-table td:nth-child(2) { width: 31%; }
            .team-cell img { width: 14px; height: 14px; }
        }
        """,
    )

def render_fantasy_league_table() -> None:
    """Render the fantasy league scorecard in the same teletext style as the league table."""
    table = get_fantasy_league_table(sheet_id=sheet_id, tab_name=config.SCORECARD_SHEET_NAME)

    st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>LIVE FANTASY LEAGUE TABLE</h2>", unsafe_allow_html=True)

    if table.empty:
        st.warning("Fantasy league table is unavailable right now.")
        return

    table = table.iloc[:-1, :-2]

    headers = [str(col).upper() for col in table.columns]
    rows_html = []
    for _, row in table.iterrows():
        cells = "".join(f"<td>{'' if pd.isna(val) else val}</td>" for val in row)
        rows_html.append(f"<tr>{cells}</tr>")

    render_ceefax_table(
        headers,
        rows_html,
        extra_css="""
        .ceefax-table-shell {
            width: min(100%, 1400px);
            margin-left: 0;
            margin-right: 0;
        }
        .ceefax-table {
            table-layout: auto;
            font-size: 23px;
            min-width: 760px;
        }
        .ceefax-table th, .ceefax-table td {
            padding: 6px 10px;
            white-space: nowrap;
        }
        @media (max-width: 768px) {
            .ceefax-table {
                font-size: 16px;
            }
        }
        """,
    )

def main() -> None:
    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"

    # Render transfer feed
    render_transfer_feed()

    render_ceefax_header(page_num=302, title="FOOTBALL")

    st.markdown("<p style='color:#00FFFF; text-align:center; margin:4px 0;'>FANTASY FOOTBALL STATISTICAL INDEX 2026/27</p>", unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        div[data-testid="stHorizontalBlock"] {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        div[data-testid="stHorizontalBlock"] > div {
            display: flex;
            justify-content: center;
        }
        div.stButton {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        div.stButton > button {
            width: 100%;
            white-space: nowrap;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="navbuttons"):
        btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns(5)

        if btn_col1.button("303 LIVE PREMIER LEAGUE TABLE", use_container_width=True, key="league_tab"):
            st.session_state.active_page = "league"
        if btn_col2.button("304 FIXTURES & RESULTS", use_container_width=True, key="fixtures_tab"):
            st.session_state.active_page = "fixtures"
        if btn_col3.button("305 PLAYER SEARCH", use_container_width=True, key="players_tab"):
            st.session_state.active_page = "players"
        if btn_col4.button("306 FANTASY SQUADS", use_container_width=True, key="squads_tab"):
            st.session_state.active_page = "squads"
        if btn_col5.button("307 FANTASY LEAGUE TABLE", use_container_width=True, key="fantasy_league_tab"):
            st.session_state.active_page = "fantasy_league"

    if st.session_state.active_page == "league":
        render_league_table()
    elif st.session_state.active_page == "squads":
        render_fantasy_squad_page()
    elif st.session_state.active_page == "players":
        return;
    elif st.session_state.active_page == "fantasy_league":
        render_fantasy_league_table()
if __name__ == "__main__":
    main()