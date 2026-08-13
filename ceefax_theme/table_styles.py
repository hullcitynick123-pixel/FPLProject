import pandas as pd

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