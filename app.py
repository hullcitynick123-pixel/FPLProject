"""Streamlit Dashboard for Premier League & FPL Analytics."""

import streamlit as st

from ceefax_theme.ceefax_header import render_ceefax_header
from ceefax_theme.ceefax_theme import inject_ceefax_styles
from views.navigation import render_active_page, render_navigation
from views.transfer_feed import render_current_transfer_indicator, render_transfer_feed

# --- Page Configuration ---
st.set_page_config(
    page_title="CEEFAX P302 - FPL STATS",
    page_icon="📺",
    layout="wide"
)

# --- Inject Ceefax Styles ---
inject_ceefax_styles()


def main() -> None:
    """Render the dashboard shell and the currently selected page."""
    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"

    render_current_transfer_indicator()
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
