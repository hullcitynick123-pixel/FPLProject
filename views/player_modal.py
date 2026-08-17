"""Player profile modal used by squad/player views."""

import pandas as pd
import streamlit as st

import config
from api_client import APIFootballClient
from data.data_processor import build_player_stats_rows


def render_player_modal(player_name: str) -> None:
    """Display a modal with player stats and a season selector."""
    seasons = [2022, 2023, 2024, 2025]
    if "player_modal_year" not in st.session_state:
        st.session_state.player_modal_year = config.DEFAULT_SEASON

    @st.dialog(f"Player profile: {player_name}")
    def modal_content() -> None:
        selected_year = st.selectbox(
            "Season",
            seasons,
            index=seasons.index(st.session_state.player_modal_year) if st.session_state.player_modal_year in seasons else len(seasons) - 1,
            key="player_modal_year_select",
        )
        st.session_state.player_modal_year = selected_year

        client = APIFootballClient()
        try:
            response = client.fetch_player(player_name, league=config.DEFAULT_LEAGUE_ID, season=selected_year)
            results = response.get("response", [])
            if not results:
                st.warning(f"No data found for {player_name} in {selected_year}.")
                return

            player = results[0].get("player", {})
            statistics = results[0].get("statistics", [{}])[0]

            col_photo, col_meta = st.columns([1, 3])
            with col_photo:
                if player.get("photo"):
                    st.image(player["photo"], width=120)
            with col_meta:
                st.markdown(f"### {player.get('name', player_name)}")
                items = [
                    player.get("nationality"),
                    player.get("position"),
                    player.get("age"),
                    player.get("height"),
                    player.get("weight"),
                ]
                st.caption(" • ".join(str(item) for item in items if item))

            stat_rows = build_player_stats_rows(statistics)
            if stat_rows:
                stat_df = pd.DataFrame(stat_rows, columns=["Metric", "Value"])
                st.dataframe(stat_df, hide_index=True, use_container_width=True)
            else:
                st.info("Statistics are currently unavailable for this player.")
        except Exception as exc:
            st.error(f"Unable to load player stats: {exc}")

    modal_content()
