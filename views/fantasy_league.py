"""Fantasy league scorecard page."""

import pandas as pd
import streamlit as st

import config
from ceefax_theme.ceefax_table import render_ceefax_table
from data_processor import get_fantasy_league_table


def render_fantasy_league_table() -> None:
    """Render the fantasy league scorecard in the same teletext style as the league table."""
    table = get_fantasy_league_table(sheet_id=config.SHEET_ID, tab_name=config.SCORECARD_SHEET_NAME)

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
