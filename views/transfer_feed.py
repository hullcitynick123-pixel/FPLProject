"""Rolling transfer news marquee shown at the top of the dashboard."""

import streamlit as st

import config
from data_processor import fetch_transfers
from utils.date import get_current_gameweek
from utils.news_flavor import build_dynamic_feed


def render_transfer_feed() -> None:
    """Render a rolling transfer news feed at the top of the page."""
    try:
        current_gameweek = get_current_gameweek()
        transfers = fetch_transfers(sheet_id=config.SHEET_ID, tab_name=config.TRANSFERS_SHEET_NAME, gameweek=current_gameweek["id"])
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
