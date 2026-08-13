"""Ceefax header utility for the FPL dashboard."""

import datetime

import streamlit.components.v1 as components

from ceefax_theme.ceefax_clock import get_clock_script
from get_fpl_data import get_time_until_next_gameweek


def render_ceefax_header(page_num: int = 302, title: str = "FOOTBALL") -> None:
    """Render the classic top header line seen on BBC Ceefax."""
    components.html(
        f"""
        <html>
        <head>
            <style>
            @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #000000;
                    color: #FFFFFF;
                    font-family: 'VT323', monospace;
                }}
                .ceefax-header {{
                    background-color: #000000;
                    color: #00FFFF;
                    font-size: 28px;
                    font-family: 'VT323', monospace;
                    border-bottom: 4px solid #0000FF;
                    padding: 4px 0px;
                    margin: 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                .ceefax-page-num {{ color: #FFFF00; font-weight: bold; }}
                .ceefax-title {{ color: #FFFFFF; background-color: #0000FF; padding: 0 8px; }}
                .ceefax-meta {{
                    display: flex;
                    flex-direction: column;
                    align-items: flex-end;
                    justify-content: center;
                    line-height: 1.1;
                }}
                .ceefax-countdown {{
                    color: #FF00FF;
                    font-size: 18px;
                    letter-spacing: 0.5px;
                }}
                .ceefax-time {{ color: #00FF00; font-size: 26px; }}
            </style>
        </head>
        <body>
            <div class="ceefax-header">
                <span>CEEFAX 1 <span class="ceefax-page-num">{page_num}</span></span>
                <span class="ceefax-title">{title}</span>
                <div class="ceefax-meta">
                    <div class="ceefax-countdown">{get_time_until_next_gameweek()}</div>
                    <div class="ceefax-time" id="ceefax-time">{datetime.datetime.now().strftime("%a %d %b %H:%M:%S")}</div>
                </div>
            </div>
            {get_clock_script()}
        </body>
        </html>
        """,
        height=110,
        scrolling=False,
    )
