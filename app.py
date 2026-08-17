"""Streamlit Dashboard for Premier League & FPL Analytics."""

import streamlit as st

import config
from ceefax_theme.ceefax_header import render_ceefax_header
from ceefax_theme.ceefax_theme import inject_ceefax_styles
from data_processor import fetch_transfers
from utils.date import get_current_gameweek
from utils.news_flavor import build_dynamic_feed
from views.fantasy_league import render_fantasy_league_table
from views.fixtures import render_fixtures_page
from views.league import render_league_table
from views.squads import render_fantasy_squad_page

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

def render_navigation() -> None:
    """Render the main page navigation buttons."""
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
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

        if btn_col1.button("303 LIVE PREMIER LEAGUE TABLE", use_container_width=True, key="league_tab"):
            st.session_state.active_page = "league"
        if btn_col2.button("304 FIXTURES & RESULTS", use_container_width=True, key="fixtures_tab"):
            st.session_state.active_page = "fixtures"
        if btn_col4.button("305 FANTASY SQUADS", use_container_width=True, key="squads_tab"):
            st.session_state.active_page = "squads"
        if btn_col3.button("306 FANTASY LEAGUE TABLE", use_container_width=True, key="fantasy_league_tab"):
            st.session_state.active_page = "fantasy_league"

def render_active_page() -> None:
    """Render the page selected in session state."""
    page_renderers = {
        "league": render_league_table,
        "squads": render_fantasy_squad_page,
        "fixtures": render_fixtures_page,
        "fantasy_league": render_fantasy_league_table,
    }
    renderer = page_renderers.get(st.session_state.active_page)
    if renderer:
        renderer()

def main() -> None:
    """Render the dashboard shell and the currently selected page."""
    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"

    render_transfer_feed()
    render_ceefax_header(page_num=302, title="FOOTBALL")
    st.markdown(
        "<p style='color:#00FFFF; text-align:center; margin:4px 0;'>"
        "FANTASY FOOTBALL STATISTICAL INDEX 2026/27</p>",
        unsafe_allow_html=True,
    )
    render_navigation()
    render_active_page()


if __name__ == "__main__":
    main()
