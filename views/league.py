"""Live Premier League standings page."""

import streamlit as st

import config
from ceefax_theme.ceefax_table import render_ceefax_table
from data.data_processor import get_league_table


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
