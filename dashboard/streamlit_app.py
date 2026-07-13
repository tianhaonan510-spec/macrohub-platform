# -*- coding: utf-8 -*-
"""Streamlit Cloud compatible entrypoint for EconAtlas.

Streamlit Cloud was configured to run this file. Keep it lightweight and
delegate to the upgraded big-screen dashboard.

For the original full platform view, run:
    streamlit run dashboard/full_platform_app.py
"""

from pathlib import Path
import runpy


APP_PATH = Path(__file__).resolve().parent / "bigscreen_app.py"
runpy.run_path(str(APP_PATH), run_name="__main__")
