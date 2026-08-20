"""Rolling transfer news marquee shown at the top of the dashboard."""

import html

import streamlit as st

import config
from data_processor import fetch_transfers
from utils.date import get_current_gameweek, get_gameweek_first_kickoff
from utils.news_flavor import build_dynamic_feed
from utils.transfer_timetable import get_current_transfer_slot


def render_current_transfer_indicator() -> None:
    """Render a banner showing whose transfer pick slot is currently active."""
    try:
        current_gameweek = get_current_gameweek()
        gameweek_id = current_gameweek.get("id")
        if not gameweek_id:
            return

        first_kickoff = get_gameweek_first_kickoff(gameweek_id)
        slot = get_current_transfer_slot(gameweek_id, first_kickoff)
    except Exception as e:
        print(f"Failed to compute current transfer slot: {e}")
        return

    if not slot:
        return

    time_range = f"{slot['start'].strftime('%H:%M')}-{slot['end'].strftime('%H:%M')}"
    if slot["manager"]:
        label = f"{html.escape(slot['label'].upper())} \u2014 {html.escape(slot['manager'].upper())}"
    else:
        label = html.escape(slot["label"].upper())

    st.markdown(
        f"""<div style='background-color:#FFFF00; color:#000000; padding:6px 10px;
        font-weight:bold; text-align:center; text-transform:uppercase; margin-bottom:4px;'>
        \u23f0 CURRENT TRANSFER SLOT: {label} ({time_range})
        </div>""",
        unsafe_allow_html=True,
    )


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

    transfer_text = "".join(
        f'<span class="transfer-item">{html.escape(transfer)}</span>'
        for transfer in transfers
    )

    # CSS for marquee scrolling effect (must not be indented, or Markdown renders it as a code block)
    marquee_html = f"""<style>
@keyframes scroll {{
    0% {{ transform: translateX(100%); }}
    100% {{ transform: translateX(-100%); }}
}}
.transfer-marquee {{
    background-color: #000000;
    color: #FFFFFF;
    padding: 12px 10px;
    font-size: 20px;
    font-weight: bold;
    text-transform: uppercase;
    overflow: hidden;
    white-space: nowrap;
    margin-top: 0;
    margin-bottom: 8px;
}}
.transfer-item {{
    display: inline-block;
    padding: 0 28px;
    border-right: 2px solid #FF00FF;
}}
.transfer-scroll {{
    display: inline-block;
    animation: scroll 120s linear infinite;
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
