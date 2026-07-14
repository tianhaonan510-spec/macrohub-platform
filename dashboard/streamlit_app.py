# -*- coding: utf-8 -*-
"""Streamlit Cloud entrypoint for EconAtlas.

Default view: showcase landing page.
Platform view: append ?page=platform to enter the big-screen dashboard.
"""

from __future__ import annotations

import base64
import mimetypes
import re
import runpy
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


BASE_DIR = Path(__file__).resolve().parents[1]
SHOWCASE_DIR = BASE_DIR / "showcase"
BIGSCREEN_PATH = BASE_DIR / "dashboard" / "bigscreen_app.py"


def query_value(name: str, default: str = "") -> str:
    try:
        value = st.query_params.get(name, default)
    except Exception:
        try:
            value = st.experimental_get_query_params().get(name, [default])[0]
        except Exception:
            value = default
    if isinstance(value, list):
        return value[0] if value else default
    return str(value or default)


if query_value("page") == "platform":
    runpy.run_path(str(BIGSCREEN_PATH), run_name="__main__")
    st.stop()


st.set_page_config(
    page_title="EconAtlas 全球宏观经济数据要素服务平台",
    page_icon="EA",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def asset_data_uri(match: re.Match) -> str:
    relative = match.group(0)
    path = SHOWCASE_DIR / relative
    if not path.exists():
        return relative
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def load_showcase_html() -> str:
    html = (SHOWCASE_DIR / "index.html").read_text(encoding="utf-8")
    html = re.sub(r"assets/[A-Za-z0-9_.-]+", asset_data_uri, html)
    html = html.replace('href="http://localhost:8508/" target="_blank"', 'href="?page=platform" target="_parent"')
    html = html.replace('href="http://localhost:8508/"', 'href="?page=platform" target="_parent"')
    resize_script = """
    <script>
      (() => {
        const updateFrameHeight = () => {
          const height = Math.ceil(document.documentElement.scrollHeight);
          window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:setFrameHeight",
            height,
          }, "*");
        };

        window.addEventListener("load", updateFrameHeight);
        window.addEventListener("resize", updateFrameHeight);
        new ResizeObserver(updateFrameHeight).observe(document.body);
        requestAnimationFrame(updateFrameHeight);
      })();
    </script>
    """
    return html.replace("</body>", f"{resize_script}</body>")


st.markdown(
    """
    <style>
    .stApp { background: #fff; }
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }
    #MainMenu, header, footer, [data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }
    iframe {
        display: block;
        border: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(load_showcase_html(), height=5600, scrolling=True)
