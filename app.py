"""Streamlit Dashboard for Premier League & FPL Analytics."""

import streamlit as st
import pandas as pd
import plotly.express as px

import config
from api_client import APIFootballClient
from data_processor import parse_player_raw_data, calculate_per_90_metrics
from ceefax_theme import inject_ceefax_styles
from ceefax_header import render_ceefax_header


# --- Page Configuration ---
st.set_page_config(
    page_title="CEEFAX P302 - FPL STATS",
    page_icon="📺",
    layout="wide"
)

# --- Inject Ceefax Styles ---
inject_ceefax_styles()

# --- Cached Data Fetching ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_player_data(season: int) -> pd.DataFrame:
    """Fetch raw API data, parse, and engineer metrics with 1-hour cache."""
    client = APIFootballClient()
    raw_response = client.fetch_top_scorers(season=season)
    raw_df = parse_player_raw_data(raw_response)
    if raw_df.empty:
        return pd.DataFrame()
    
    # Process base metrics with minimum 1 minute played
    processed_df = calculate_per_90_metrics(raw_df, min_minutes=1)
    return processed_df


@st.cache_data(ttl=3600, show_spinner=False)
def get_league_table(season: int = config.DEFAULT_SEASON) -> pd.DataFrame:
    """Fetch and flatten the current Premier League standings."""
    client = APIFootballClient()
    response = client.fetch_standings(season=season)
    standings = response.get("response", [])
    if not standings:
        return pd.DataFrame()

    rows = standings[0].get("league", {}).get("standings", [[]])[0]
    if not rows:
        return pd.DataFrame()

    table = pd.DataFrame(
        [
            {
                "Rank": row.get("rank"),
                "Team": row.get("team", {}).get("name", ""),
                "Team_Logo": row.get("team", {}).get("logo"),
                "Played": row.get("all", {}).get("played"),
                "Won": row.get("all", {}).get("win"),
                "Drawn": row.get("all", {}).get("draw"),
                "Lost": row.get("all", {}).get("lose"),
                "GF": row.get("all", {}).get("goals", {}).get("for"),
                "GA": row.get("all", {}).get("goals", {}).get("against"),
                "GD": row.get("goalsDiff"),
                "Points": row.get("points"),
                "Form": row.get("form"),
            }
            for row in rows
        ]
    )
    return table


def teletext_styler(frame: pd.DataFrame):
    """Return a retro Ceefax-style pandas Styler for data tables."""
    return (
        frame.style.set_properties(**{
            "background-color": "#000000",
            "color": "#00FF00",
            "border": "1px solid #00FF00",
            "font-family": "'VT323', monospace",
            "font-size": "18px",
            "padding": "6px 10px",
            "text-align": "center",
        })
        .set_table_styles([
            {
                "selector": "th",
                "props": [
                    ("background-color", "#0000FF"),
                    ("color", "#FFFFFF"),
                    ("border", "1px solid #00FF00"),
                    ("font-weight", "bold"),
                    ("padding", "8px 10px"),
                    ("text-transform", "uppercase"),
                ],
            },
            {
                "selector": "td",
                "props": [
                    ("border", "1px solid #00FF00"),
                    ("padding", "6px 10px"),
                ],
            },
            {
                "selector": "tbody tr:hover",
                "props": [("background-color", "#001100"), ("color", "#FFFF00")],
            },
            {
                "selector": "img",
                "props": [("width", "20px"), ("height", "20px"), ("display", "block")],
            },
        ])
        .format({"Team": lambda value: value}, escape="html")
    )


def render_home_page() -> None:
    """Render the default analytics home view."""
    client = APIFootballClient()
    raw_data = client.fetch_top_scorers(season=config.DEFAULT_SEASON)
    raw_df = parse_player_raw_data(raw_data)
    df = calculate_per_90_metrics(raw_df, min_minutes=90)

    if not df.empty:
        col1, col2, col3 = st.columns(3)
        top_scorer = df.sort_values(by="Goals", ascending=False).iloc[0]
        top_xg = df.sort_values(by="xG_Per_90", ascending=False).iloc[0]

        col1.metric("LEADING SCORER", top_scorer["Player"], f"{top_scorer['Goals']} GOALS")
        col2.metric("HIGHEST xG/90", top_xg["Player"], f"{top_xg['xG_Per_90']}")
        col3.metric("TOTAL PLAYERS", len(df))

        st.markdown("<h2 style='color:#00FF00; margin-top:20px;'>PLAYER PERFORMANCE MATRIX</h2>", unsafe_allow_html=True)
        st.dataframe(
            teletext_styler(
                df[["Player", "Team", "Position", "Minutes", "Goals", "Goals_Per_90", "xG_Per_90", "Tackles_Per_90"]]
            ),
            use_container_width=True,
            hide_index=True,
        )


def render_league_table() -> None:
    """Render the current Premier League standings table."""
    table = get_league_table(season=config.DEFAULT_SEASON)

    st.markdown("<h2 style='color:#00FF00; margin-top:20px;'>CURRENT PREMIER LEAGUE TABLE</h2>", unsafe_allow_html=True)

    if table.empty:
        st.warning("Standings are unavailable right now.")
        return

    headers = ["POS", "TEAM", "P", "W", "D", "L", "GF", "GA", "GD", "PTS", "FORM"]
    rows_html = []
    for _, row in table.iterrows():
        team_logo = row.get("Team_Logo") or ""
        team_name = row.get("Team") or ""
        team_cell = (
            f"<div class='team-cell'><img src='{team_logo}' alt='{team_name}' /><span>{team_name}</span></div>"
            if team_logo
            else f"<div class='team-cell'><span>{team_name}</span></div>"
        )
        rows_html.append(
            "<tr>"
            f"<td>{int(row['Rank'])}</td>"
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

    table_html = f"""
    <style>
        .teletext-table {{
            width: 100%;
            border-collapse: collapse;
            background: #000000;
            color: #00FF00;
            font-family: 'VT323', monospace;
            font-size: 18px;
            border: 2px solid #00FF00;
        }}
        .teletext-table th, .teletext-table td {{
            border: 1px solid #00FF00;
            padding: 8px 10px;
            text-align: center;
            vertical-align: middle;
        }}
        .teletext-table th {{
            background: #0000FF;
            color: #FFFFFF;
            text-transform: uppercase;
        }}
        .team-cell {{
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 8px;
            text-align: left;
        }}
        .team-cell img {{
            width: 20px;
            height: 20px;
            display: block;
        }}
    </style>
    <table class='teletext-table'>
        <thead>
            <tr>{''.join(f'<th>{header}</th>' for header in headers)}</tr>
        </thead>
        <tbody>
            {''.join(rows_html)}
        </tbody>
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)


def main() -> None:
    if "active_page" not in st.session_state:
        st.session_state.active_page = "home"

    render_ceefax_header(page_num=302, title="FPL ANALYTICS")

    st.markdown("<h1 style='color:#FFFF00; text-align:center;'>CEEFAX FANTASY PREMIER LEAGUE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#00FFFF; text-align:center;'>FANTASY FOOTBALL STATISTICAL INDEX 2026/27</p>", unsafe_allow_html=True)

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
            width: min(100%, 230px);
            white-space: nowrap;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

    if btn_col1.button("303 LEAGUE TABLE", use_container_width=True, key="league_tab"):
        st.session_state.active_page = "league"
    if btn_col2.button("304 FIXTURES & RESULTS", use_container_width=True, key="fixtures_tab"):
        st.session_state.active_page = "fixtures"
    if btn_col3.button("305 PLAYER METRICS", use_container_width=True, key="players_tab"):
        st.session_state.active_page = "players"
    if btn_col4.button("306 FANTASY STATS", use_container_width=True, key="stats_tab"):
        st.session_state.active_page = "stats"
    st.markdown("---")

    if st.session_state.active_page == "league":
        render_league_table()
    else:
        render_home_page()


if __name__ == "__main__":
    main()