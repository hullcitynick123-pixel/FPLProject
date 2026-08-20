"""Shared Ceefax-style HTML table builder used across dashboard pages."""

import streamlit as st


def build_ceefax_table_html(
    headers: list[str],
    rows_html: list[str],
    extra_css: str = "",
    table_class: str = "",
) -> str:
    """Build a compact Ceefax-style table with optional table-specific CSS."""
    table_html = f"""
    <style>
        .ceefax-table-shell {{
            width: min(100%, 820px);
            margin: 0 auto 0;
            padding: 12px 12px 10px;
            background: #000000;
        }}
        .ceefax-table {{
            width: 100%;
            border-collapse: collapse;
            background: #000000;
            color: #FFFFFF;
            font-size: 19px;
            table-layout: fixed;
        }}
        .ceefax-table th, .ceefax-table td {{
            border: 0;
            border-bottom: 1px solid #073807;
            padding: 3px 5px;
            text-align: center;
            vertical-align: middle;
            line-height: 1.05;
        }}
        .ceefax-table th {{
            background: #0000FF;
            color: #FFFFFF;
            text-transform: uppercase;
            font-size: 17px;
            padding: 4px 5px;
        }}
        .ceefax-table tr:hover td {{
            background: #001c00;
        }}
        {extra_css}
        @media (max-width: 768px) {{
            .ceefax-table-shell {{ padding: 7px; }}
            .ceefax-table {{ font-size: 14px; }}
            .ceefax-table th {{ font-size: 13px; }}
            .ceefax-table th, .ceefax-table td {{ padding: 3px 2px; }}
        }}
    </style>
    <div class="teletext-table-wrapper">
    <div class="ceefax-table-shell">
    <table class='ceefax-table {table_class}'>
        <thead>
            <tr>{''.join(f'<th>{header}</th>' for header in headers)}</tr>
        </thead>
        <tbody>
            {''.join(rows_html)}
        </tbody>
    </table>
    </div>
    </div>
    """
    return table_html


def render_ceefax_table(
    headers: list[str],
    rows_html: list[str],
    extra_css: str = "",
    table_class: str = "",
) -> None:
    """Render a compact Ceefax-style table with optional table-specific CSS."""
    st.markdown(
        build_ceefax_table_html(headers, rows_html, extra_css, table_class),
        unsafe_allow_html=True,
    )
