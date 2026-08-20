"""Fantasy league scorecard page."""

import pandas as pd
import streamlit as st

import config
from ceefax_theme.ceefax_table import render_ceefax_table
from data_processor import get_fantasy_league_table


def _format_cell(val: object) -> str:
    """Format a table cell, dropping trailing .0 from whole-number floats."""
    if pd.isna(val):
        return ""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)


def _gw_score_color(val: object) -> str | None:
    """Return the background color for a gameweek score cell based on its value."""
    if pd.isna(val):
        return None
    try:
        score = float(val)
    except (TypeError, ValueError):
        return None

    if score >= 70:
        return "#00CC00"
    if score >= 56:
        return "#2E7420"
    if score >= 44:
        return "#FFFF00"
    if score >= 30:
        return "#FF8C00"
    return "#FF0000"


def render_fantasy_league_table() -> None:
    """Render the fantasy league scorecard in the same teletext style as the league table."""
    table = get_fantasy_league_table(sheet_id=config.SHEET_ID, tab_name=config.SCORECARD_SHEET_NAME)

    st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>LIVE FANTASY LEAGUE TABLE</h2>", unsafe_allow_html=True)

    if table.empty:
        st.warning("Fantasy league table is unavailable right now.")
        return

    table = table.iloc[:-1, :-2]

    headers = ["" if str(col).startswith("Unnamed:") else str(col).upper() for col in table.columns]
    gw_columns = [str(col).startswith("GW") for col in table.columns]
    rows_html = []
    for _, row in table.iterrows():
        cells = []
        for is_gw, val in zip(gw_columns, row):
            color = _gw_score_color(val) if is_gw else None
            style = f" style='background-color: {color}; color: #000000;'" if color else ""
            cells.append(f"<td{style}>{_format_cell(val)}</td>")
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    render_ceefax_table(
        headers,
        rows_html,
        extra_css="""
        .ceefax-table-shell {
            width: min(80%, 1400px);
            margin-left: 0;
            margin-right: 0;
        }
        .ceefax-table {
            table-layout: auto;
            font-size: 23px;
        }
        .ceefax-table th, .ceefax-table td {
            padding: 6px 10px;
            white-space: nowrap;
        }
        @media (max-width: 768px) {
            .fantasy-league-table {
                font-size: 16px;
                min-width: 760px;
            }
            .fantasy-league-table th, .fantasy-league-table td {
                white-space: normal;
                overflow-wrap: anywhere;
            }
        }
        """,
        table_class="fantasy-league-table",
    )
