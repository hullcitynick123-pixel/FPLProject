"""Fantasy Squads page."""

import streamlit as st

import config
from data.data_processor import fetch_draft_squads, get_manager_squad_by_position
from fpl_constants import MANAGER_TEAMS
from views.player_modal import render_player_modal


def render_fantasy_squad_page() -> None:
    """Render the Fantasy Squads page with manager selections."""
    st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>FANTASY SQUADS</h2>", unsafe_allow_html=True)

    try:
        squads_df = fetch_draft_squads(sheet_id=config.SHEET_ID, tab_name=config.SQUAD_SHEET_NAME)
    except Exception as e:
        st.error(f"Failed to fetch fantasy squads: {e}")
        return

    if squads_df.empty:
        st.warning("No squad data available.")
        return

    managers = list(squads_df.columns)
    columns = st.columns(min(5, max(1, len(managers))))

    for index, manager_name in enumerate(managers):
        team_name = MANAGER_TEAMS.get(manager_name, manager_name)
        squad_dict = get_manager_squad_by_position(squads_df, manager_name)

        with columns[index % len(columns)]:
            st.markdown(f"<h3 style='color:#FFFF00; text-align:center; margin-bottom:4px;'>{team_name}</h3>", unsafe_allow_html=True)
            st.caption(f"Manager: {manager_name}")

            if not squad_dict:
                st.write("No squad data.")
                continue

            for position, players in squad_dict.items():
                st.markdown(f"<p style='color:#00FFFF; margin:8px 0 4px 0;'>{position}</p>", unsafe_allow_html=True)
                for player in players:
                    if st.button(player, key=f"player_{manager_name}_{player}", use_container_width=True):
                        st.session_state.selected_player = player
                        render_player_modal(player)
