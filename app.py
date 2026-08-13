"""Streamlit Dashboard for Premier League & FPL Analytics."""

import streamlit as st
import pandas as pd
import config
from fpl_constants import MANAGER_TEAMS
from data_processor import fetch_draft_squads, get_manager_squad_by_position, fetch_transfers, get_league_table
from ceefax_theme.ceefax_theme import inject_ceefax_styles
from ceefax_theme.ceefax_header import render_ceefax_header


# --- Page Configuration ---
st.set_page_config(
    page_title="CEEFAX P302 - FPL STATS",
    page_icon="📺",
    layout="wide"
)

sheet_id = config.SHEET_ID
tab_name = config.SHEET_NAME

# --- Inject Ceefax Styles ---
inject_ceefax_styles()

def render_transfer_feed() -> None:
    """Render a rolling transfer news feed at the top of the page."""
    try:
        # Determine current gameweek based on season start date
        from datetime import datetime, timedelta
        try:
            season_start = datetime.strptime(config.SEASON_START_DATE, "%Y-%m-%d")
        except:
            season_start = datetime(2026, 8, 21)  # Default fallback
        
        current_date = datetime.now()
        days_since_start = (current_date - season_start).days
        current_gameweek = max(1, (days_since_start // 7) + 1)  # Gameweek changes weekly
        
        transfers = fetch_transfers(sheet_id=sheet_id, tab_name="Transfers", gameweek=current_gameweek)
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

    # Display squads in 5-column layout (2 rows of 5)
    managers = list(squads_df.columns)
    for i in range(0, len(managers), 5):
        cols = st.columns(5)
        
        for col_idx, manager_name in enumerate(managers[i:i+5]):
            with cols[col_idx]:
                # Get team name for this manager
                team_name = MANAGER_TEAMS.get(manager_name, manager_name)

                # Get the manager's squad by position
                squad_dict = get_manager_squad_by_position(squads_df, manager_name)
                if not squad_dict:
                    st.info(f"No squad data for {manager_name}.")
                    continue

                # Convert dict to DataFrame for styling
                squad_data = []
                for position, players in squad_dict.items():
                    for player in players:
                        squad_data.append({"Position": position, "Player": player})
                squad_df = pd.DataFrame(squad_data)

                # Display the squad in a styled table with compact sizing
                styled_table = (
                    squad_df.style.set_properties(**{
                        "background-color": "#000000",
                        "color": "#00FF00",
                        "border": "1px solid #00FF00",
                        "font-family": "'VT323', monospace",
                        "font-size": "20px",
                        "padding": "3px 4px",
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
                                ("padding", "3px 4px"),
                                ("font-size", "15px"),
                            ],
                        },
                        {
                            "selector": "td",
                            "props": [
                                ("border", "1px solid #00FF00"),
                                ("padding", "3px 3px"),
                                ("font-size", "20px"),  
                            ],
                        },
                    ])
                )
                
                # Combine header and table in a single container
                header_html = (
                    f"<div style='text-align:center; width:100%;'>"
                    f"<h3 style='color:#FFFF00; margin:0 0 4px 0; padding:0;'>{team_name}</h3>"
                    f"<p style='color:#00FFFF; margin:0 0 8px 0; padding:0; font-size:11px;'>(Manager: {manager_name})</p>"
                    f"</div>"
                )
                table_html = styled_table.to_html()
                
                combined_html = f"<div style='display:flex; flex-direction:column; align-items:center;'>{header_html}{table_html}</div>"
                st.markdown(combined_html, unsafe_allow_html=True)

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

    # Render transfer feed
    render_transfer_feed()

    render_ceefax_header(page_num=302, title="FOOTBALL")

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

    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)

    if btn_col1.button("303 LEAGUE TABLE", use_container_width=True, key="league_tab"):
        st.session_state.active_page = "league"
    if btn_col2.button("304 FIXTURES & RESULTS", use_container_width=True, key="fixtures_tab"):
        st.session_state.active_page = "fixtures"
    if btn_col3.button("305 PLAYER INDEX", use_container_width=True, key="players_tab"):
        st.session_state.active_page = "players"
    if btn_col4.button("306 FANTASY SQUADS", use_container_width=True, key="squads_tab"):
        st.session_state.active_page = "squads"

    if st.session_state.active_page == "league":
        render_league_table()
    elif st.session_state.active_page == "squads":
        render_fantasy_squad_page()

if __name__ == "__main__":
    main()