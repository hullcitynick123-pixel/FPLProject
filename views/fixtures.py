"""Fixtures & results page with gameweek navigation."""

import pandas as pd
import streamlit as st

from data_processor import get_fixtures_for_gameweek
from utils.date import get_current_gameweek


def render_fixtures_page() -> None:
    """Render the fixtures and results page for a selectable gameweek."""
    st.markdown("<h2 style='color:#00FF00; margin-top:20px; text-align:center;'>FIXTURES & RESULTS</h2>", unsafe_allow_html=True)

    if "fixtures_gameweek" not in st.session_state:
        current_gameweek = get_current_gameweek()
        st.session_state.fixtures_gameweek = current_gameweek.get("id") or 1

    min_gw, max_gw = 1, 38
    gameweek = st.session_state.fixtures_gameweek

    st.markdown(
        """
        <style>
        @media (max-width: 768px) {
            div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
                flex-direction: row !important;
                flex-wrap: nowrap !important;
            }
            div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) div[data-testid="stColumn"] {
                width: unset !important;
                flex: 1 1 0 !important;
                min-width: 0 !important;
            }
            div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button {
                font-size: 12px !important;
                padding: 0.25rem 0.4rem !important;
                white-space: nowrap !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    nav_prev, nav_label, nav_next = st.columns([1, 2, 1])
    with nav_prev:
        if st.button("◀ PREV GW", use_container_width=True, disabled=gameweek <= min_gw, key="fixtures_prev_gw"):
            st.session_state.fixtures_gameweek = max(min_gw, gameweek - 1)
            st.rerun()
    with nav_label:
        st.markdown(
            f"<h3 style='color:#FFFF00; text-align:center; margin:0;'>GAMEWEEK {gameweek}</h3>",
            unsafe_allow_html=True,
        )
    with nav_next:
        if st.button("NEXT GW ▶", use_container_width=True, disabled=gameweek >= max_gw, key="fixtures_next_gw"):
            st.session_state.fixtures_gameweek = min(max_gw, gameweek + 1)
            st.rerun()

    try:
        fixtures = get_fixtures_for_gameweek(gameweek)
    except Exception as e:
        st.error(f"Failed to fetch fixtures: {e}")
        return

    if not fixtures:
        st.warning("No fixtures found for this gameweek.")
        return

    fixture_rows = []
    for fixture in fixtures:
        try:
            kickoff_dt = pd.to_datetime(fixture["date"]).tz_convert("Europe/London")
            kickoff = f"{kickoff_dt.strftime('%a %d %b')}<br>{kickoff_dt.strftime('%H:%M')}"
        except Exception:
            kickoff = ""

        status = fixture.get("status_short")
        if status in ("FT", "AET", "PEN"):
            score_display = f"{fixture['home_goals']} - {fixture['away_goals']}"
        elif status in ("1H", "2H", "ET", "P", "LIVE"):
            score_display = f"{fixture['home_goals']} - {fixture['away_goals']} ({fixture.get('elapsed') or ''}')"
        else:
            score_display = kickoff

        fixture_rows.append(
            "<tr>"
            f"<td class='fx-home'><span class='fx-team-name'>{fixture['home_name']}</span>"
            f"<img src='{fixture['home_logo']}' class='fx-crest' /></td>"
            f"<td class='fx-score'>{score_display}</td>"
            f"<td class='fx-away'><img src='{fixture['away_logo']}' class='fx-crest' />"
            f"<span class='fx-team-name'>{fixture['away_name']}</span></td>"
            "</tr>"
        )

    st.markdown(
        """
        <style>
        .fx-table { width:100%; table-layout:fixed; border-collapse:collapse; }
        .fx-table td { padding:10px 12px; vertical-align:middle; border-bottom:1px solid #073807; overflow:hidden; }
        .fx-home { width:40%; text-align:right; }
        .fx-away { width:40%; text-align:left; }
        .fx-score { width:20%; text-align:center; color:#00FFFF; font-weight:bold; white-space:nowrap; line-height:1.3; }
        .fx-team-name {
            display:inline-block; vertical-align:middle; color:#FFFFFF;
            white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:80%;
        }
        .fx-crest { width:28px; height:28px; vertical-align:middle; margin:0 8px; }
        @media (max-width: 768px) {
            .fx-table td { padding:8px 4px; font-size:12px; }
            .fx-home { width:38%; }
            .fx-away { width:38%; }
            .fx-score { width:24%; font-size:11px; }
            .fx-crest { width:18px; height:18px; margin:0 3px; }
            .fx-team-name { max-width:70%; }
        }
        </style>
        """
        ,
        unsafe_allow_html=True,
    )

    for fixture, fixture_row in zip(fixtures, fixture_rows):
        st.markdown(
            f"<table class='fx-table'><tbody>{fixture_row}</tbody></table>",
            unsafe_allow_html=True,
        )
        fixture_key = fixture.get("fixture_id") or f"{fixture['home_name']}_{fixture['away_name']}"
        scorer_state_key = f"show_scorers_{fixture_key}"
        is_visible = st.session_state.get(scorer_state_key, False)
        button_label = "HIDE SCORERS" if is_visible else "SHOW SCORERS"
        if st.button(button_label, key=f"scorers_button_{fixture_key}", use_container_width=True):
            st.session_state[scorer_state_key] = not is_visible
            st.rerun()

        if is_visible:
            scorers = fixture.get("scorers", [])
            if scorers:
                scorer_lines = []
                for scorer in scorers:
                    minute = scorer.get("elapsed")
                    extra = scorer.get("extra")
                    minute_text = ""
                    if minute is not None:
                        minute_text = f" ({minute}+{extra}' if extra else f' ({minute}')"
                    scorer_lines.append(
                        f"<div class='fx-scorer'>{scorer['name']}{minute_text}"
                        f" <span class='fx-scorer-team'>{scorer['team']}</span></div>"
                    )
                    print(scorer_lines)
                st.markdown("<div class='fx-scorers'>" + "".join(scorer_lines) + "</div>", unsafe_allow_html=True)
            else:
                st.caption("No scorers recorded.")
