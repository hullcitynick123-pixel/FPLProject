"""Top-level page navigation and dispatch for the dashboard."""

import streamlit as st

from views.fantasy_league import render_fantasy_league_table
from views.fixtures import render_fixtures_page
from views.league import render_league_table
from views.squads import render_fantasy_squad_page


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

        if btn_col1.button("303 FANTASY SQUADS", use_container_width=True, key="squads_tab"):
            st.session_state.active_page = "squads"
        if btn_col2.button("304 FANTASY LEAGUE TABLE", use_container_width=True, key="fantasy_league_tab"):
            st.session_state.active_page = "fantasy_league"
        if btn_col3.button("305 LIVE PREMIER LEAGUE TABLE", use_container_width=True, key="league_tab"):
            st.session_state.active_page = "league"
        if btn_col4.button("306 FIXTURES & RESULTS", use_container_width=True, key="fixtures_tab"):
            st.session_state.active_page = "fixtures"

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
