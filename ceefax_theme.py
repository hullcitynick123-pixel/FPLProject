"""Ceefax / Teletext 1980s Retro Theme for Streamlit."""

import streamlit as st


def inject_ceefax_styles() -> None:
    """Inject custom CSS to turn Streamlit into a 1990s BBC Ceefax terminal."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        /* Global Teletext Canvas */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stApp, .main, .block-container {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            font-family: 'VT323', monospace !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* Remove the white margin gap at the very top of the page */
        .stApp {
            background: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        [data-testid="stHeader"] {
            background: #000000 !important;
            display: none !important;
        }

        [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stVerticalBlock"] {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }

        /* Override Streamlit Typography Everywhere */
        h1, h2, h3, h4, h5, h6, p, span, div, label, button, input {
            font-family: 'VT323', monospace !important;
            letter-spacing: 1.5px !important;
        }

        h1 { font-size: 38px !important; color: #FFFF00 !important; }
        h2 { font-size: 30px !important; color: #00FFFF !important; }
        h3 { font-size: 24px !important; color: #00FF00 !important; }

        /* Ceefax Header Banner */
        .ceefax-header {
            background-color: #000000;
            color: #00FFFF;
            font-size: 28px;
            font-family: 'VT323', monospace;
            border-bottom: 4px solid #0000FF;
            padding: 4px 0px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
        }

        .ceefax-page-num { color: #FFFF00; font-weight: bold; }
        .ceefax-title    { color: #FFFFFF; background-color: #0000FF; padding: 0 8px; }
        .ceefax-time     { color: #00FF00; }

        /* Custom Teletext Data Cards */
        div[data-testid="stMetric"] {
            background-color: #000000 !important;
            border: 2px solid #00FFFF !important;
            padding: 10px !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #FFFF00 !important;
            font-size: 20px !important;
        }

        div[data-testid="stMetricValue"] {
            color: #00FF00 !important;
            font-size: 32px !important;
        }

        /* Fastext Color Buttons (Red, Green, Yellow, Blue) */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
            background-color: #CC0000 !important; color: #FFFFFF !important; border: none !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
            background-color: #008800 !important; color: #FFFFFF !important; border: none !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {
            background-color: #CCCC00 !important; color: #000000 !important; border: none !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(4) button {
            background-color: #0000CC !important; color: #FFFFFF !important; border: none !important;
        }

        .stButton > button {
            width: 100%;
            font-size: 22px !important;
            border-radius: 0px !important;
            text-transform: uppercase;
        }

        /* Streamlit Tables Teletext Look */
        [data-testid="stDataFrame"] {
            border: 2px solid #FFFF00 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_ceefax_header(page_num: int = 302, title: str = "FOOTBALL") -> None:
    """Render the classic top header line seen on BBC Ceefax."""
    st.markdown(
        f"""
        <div class="ceefax-header">
            <span>CEEFAX 1 <span class="ceefax-page-num">{page_num}</span></span>
            <span class="ceefax-title">{title}</span>
            <span class="ceefax-time">Tue 11 Aug 11:58:00</span>
        </div>
        """,
        unsafe_allow_html=True,
    )