"""Ceefax header utility for the FPL dashboard."""

import streamlit.components.v1 as components

from ceefax_theme.ceefax_clock import get_clock_script
from get_fpl_data import get_time_until_next_gameweek
from utils.date import get_current_date


def render_ceefax_header(page_num: int = 302, title: str = "FOOTBALL") -> None:
    """Render the classic top header line seen on BBC Ceefax."""
    components.html(
        f"""
        <html>
        <head>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    background-color: #000000;
                    color: #FFFFFF;
                    user-select: none;
                }}
                
                /* Top Status Row */
                .ceefax-top-row {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-size: 26px;
                    padding: 2px 4px 6px;
                    line-height: 1;
                }}
                .ceefax-brand {{ color: #FFFFFF; }}
                .ceefax-page-num {{ color: #FFFF00; font-weight: bold; }}
                
                .ceefax-meta {{
                    display: flex;
                    align-items: center;
                    gap: 16px;
                }}
                .ceefax-countdown {{
                    color: #FF00FF;
                    font-size: 20px;
                }}
                .ceefax-time {{
                    color: #00FF00;
                    font-size: 26px;
                }}

                /* Main Teletext Title Banner */
                .ceefax-banner {{
                    display: flex;
                    align-items: stretch;
                    height: 54px;
                    width: 100%;
                }}
                
                .opx-cubes-wrapper {{
                    display: flex;
                    gap: 6px; /* Space between the 3 cubes */
                    margin-right: 12px;
                }}

                .opx-cube {{
                    background-color: #FFFFFF;
                    color: #000000;
                    font-size: 5rem;
                    font-weight: 900;
                    width: 2rem;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    
                    /* Box shadow around each cube */
                    box-shadow: 3px 3px 0px #000000; 
                    
                }}

                /* Title Section (Green Text on Blue Background) */
                .ceefax-title {{
                    background-color: #0000FF;
                    color: #00FF00;
                    flex-grow: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 48px;
                    font-weight: bold;
                    letter-spacing: 8px;
                    text-transform: uppercase;
                    margin: 0;
                    text-shadow: 0px 4px 0px #000000;
                }}

                /* Shrink everything on narrow viewports so it fits within the iframe height */
                @media (max-width: 480px) {{
                    .ceefax-top-row {{
                        font-size: 15px;
                        padding: 2px 4px 4px;
                        flex-wrap: nowrap;
                    }}
                    .ceefax-meta {{ gap: 8px; }}
                    .ceefax-countdown {{ font-size: 12px; }}
                    .ceefax-time {{ font-size: 15px; }}
                    .ceefax-banner {{ height: 38px; }}
                    .opx-cubes-wrapper {{ gap: 3px; margin-right: 6px; }}
                    .opx-cube {{ width: 1.3rem; font-size: 20px; }}
                    .ceefax-title {{ font-size: 24px; letter-spacing: 3px; }}
                }}
            </style>
        </head>
        <body>
            <div class="ceefax-header">
                <div class="ceefax-top-row">
                    <span class="ceefax-brand">CEEFAX 1 <span class="ceefax-page-num">{page_num}</span></span>
                    <div class="ceefax-meta">
                        <div class="ceefax-countdown">{get_time_until_next_gameweek()}</div>
                        <div class="ceefax-time" id="ceefax-time">{get_current_date()}</div>
                    </div>
                </div>
                <div class="ceefax-banner">
                    <div class="opx-cubes-wrapper">
                        <div class="opx-cube">O</div>
                        <div class="opx-cube">P</div>
                        <div class="opx-cube">X</div>
                    </div>
                    <div class="ceefax-title">{title}</div>
                </div>
            </div>
            {get_clock_script()}
        </body>
        </html>
        """,
        height=100,
        scrolling=False,
    )