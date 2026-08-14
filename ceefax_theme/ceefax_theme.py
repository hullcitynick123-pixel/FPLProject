"""Ceefax / Teletext 1980s Retro Theme for Streamlit."""

import streamlit as st
import streamlit.components.v1 as components
import datetime


def inject_ceefax_styles() -> None:
    """Inject custom CSS to turn Streamlit into a 1990s BBC Ceefax terminal."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

        /* 1. FORCE ABSOLUTE BLACK BACKGROUND EVERYWHERE (KILL WHITE BLEED) */
        html, body, #root, .stApp, 
        [data-testid="stAppViewContainer"], 
        [data-testid="stHeader"], header {
            background-color: #000000 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* 2. COMPLETELY REMOVE STREAMLIT TOP HEADER & DECORATION BARS */
        header, 
        [data-testid="stHeader"], 
        [data-testid="stDecoration"], 
        [data-testid="stToolbar"], 
        .stAppHeader {
            display: none !important;
            height: 0px !important;
            min-height: 0px !important;
            visibility: hidden !important;
        }

        /* 3. PULL MAIN CONTAINER FLUSH TO TOP EDGE */
        .main, 
        .main .block-container, 
        [data-testid="stAppViewBlockContainer"],
        section.main {
            padding-top: 0px !important;
            margin-top: 0px !important;
            top: 0px !important;
        }
        
        /* 3b. REMOVE PADDING FROM MAIN BLOCK CONTAINER */
        .stMainBlockContainer {
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            margin-top: 0px !important;
        }
        
        /* 3c. REMOVE ALL TOP PADDING FROM NESTED BLOCKS */
        [data-testid="stVerticalBlock"] > * > [data-testid="stVerticalBlock"]:first-child {
            margin-top: 0px !important;
            padding-top: 0px !important;
        }
        
        .stMarkdown:first-of-type,
        .stMarkdown:first-of-type > div,
        [data-testid="stVerticalBlock"]:first-child {
            margin-top: 0px !important;
            padding-top: 0px !important;
        }

        /* 4. OVERRIDE TYPOGRAPHY */
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
        div[data-baseweb="input"] > div, 
        div[data-baseweb="select"] > div {
            background-color: #000000 !important;
            border: 2px solid #00FF00 !important;
            color: #00FF00 !important;
            border-radius: 0px !important;
        }

        input {
            color: #FFFF00 !important;
            background-color: #000000 !important;
        }

        div[data-baseweb="popover"] {
            background-color: #000000 !important;
            border: 2px solid #00FFFF !important;
        }

        li[role="option"] {
            background-color: #000000 !important;
            color: #FFFF00 !important;
            font-family: 'VT323', monospace !important;
        }

        /* Make wide tables (league/fantasy tables) horizontally scrollable instead of squashed */
        .teletext-table-wrapper {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            width: 100%;
        }

        /* Let button rows wrap onto multiple lines on narrow screens */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 10px !important;
        }

        /* Nav buttons: verified via live DOM inspection that st.columns() renders
           as stHorizontalBlock > stColumn, and that the st-key-* class lands
           directly on the container's stVerticalBlock. A fixed-column grid on
           the horizontal block (not flex) guarantees every column/button is
           exactly the same width regardless of label length. */
        .st-key-navbuttons div[data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(5, 1fr) !important;
            gap: 12px !important;
        }
        .st-key-navbuttons div[data-testid="stColumn"] {
            width: 100% !important;
            min-width: 0 !important;
            flex: none !important;
        }
        /* Streamlit sets an inline pixel width on .stButton based on measured
           content; force every wrapper between the column and the button to
           100% so that inline style loses to this !important chain. */
        .st-key-navbuttons div[data-testid="stVerticalBlockBorderWrapper"],
        .st-key-navbuttons div[data-testid="stVerticalBlock"],
        .st-key-navbuttons div[data-testid="stElementContainer"],
        .st-key-navbuttons .stButton,
        .st-key-navbuttons .stButton > button {
            width: 100% !important;
            box-sizing: border-box !important;
            margin: 0 !important;
            white-space: normal !important;
        }

        /* --- Mobile breakpoint --- */
        @media (max-width: 768px) {
            h1 { font-size: 26px !important; }
            h2 { font-size: 22px !important; }
            h3 { font-size: 18px !important; }

            .ceefax-header { font-size: 18px !important; }

            .stButton > button {
                font-size: 16px !important;
                width: 100% !important;
                min-width: 0 !important;
            }

            div[data-testid="stHorizontalBlock"] {
                gap: 8px !important;
                flex-direction: column !important;
            }

            div[data-testid="stHorizontalBlock"] > div {
                box-sizing: border-box !important;
                flex: 1 1 calc(50% - 8px) !important;
                min-width: calc(50% - 8px) !important;
                margin-bottom: 8px !important;
            }

            /* Nav buttons: stack them in a single column with visible spacing */
            .st-key-navbuttons div[data-testid="stHorizontalBlock"] {
                grid-template-columns: 1fr !important;
                gap: 12px !important;
            }

            .teletext-table {
                font-size: 13px !important;
            }

            .teletext-table th, .teletext-table td {
                padding: 4px 5px !important;
            }

            .transfer-marquee {
                font-size: 11px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
                }}
                .ceefax-page-num {{ color: #FFFF00; font-weight: bold; }}
                .ceefax-title {{ color: #FFFFFF; background-color: #0000FF; padding: 0 8px; }}
                .ceefax-time {{ color: #00FF00; }}
            </style>
        </head>
        <body>
            <div class="ceefax-header">
                <span>CEEFAX 1 <span class="ceefax-page-num">{page_num}</span></span>
                <span class="ceefax-title">{title}</span>
                <span class="ceefax-time" id="ceefax-time">{datetime.datetime.now().strftime("%a %d %b %H:%M:%S")}</span>
            </div>
            <script>
            (function() {{
                const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                const clock = document.getElementById('ceefax-time');
                if (!clock) return;
                function updateTime() {{
                    const now = new Date();
                    const formatted = `${{days[now.getDay()]}} ${{String(now.getDate()).padStart(2, '0')}} ${{months[now.getMonth()]}} ${{String(now.getHours()).padStart(2, '0')}}:${{String(now.getMinutes()).padStart(2, '0')}}:${{String(now.getSeconds()).padStart(2, '0')}}`;
                    clock.textContent = formatted;
                }}
                updateTime();
                setInterval(updateTime, 1000);
            }})();
            </script>
        </body>
        </html>
        """,
        height=100,
        scrolling=False,
    )