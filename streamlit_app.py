# -*- coding: utf-8 -*-
"""Streamlit Cloud entrypoint for EconAtlas.

This wrapper keeps the cloud default entrypoint stable while the actual
dashboard implementation lives in dashboard/bigscreen_app.py.
"""

from pathlib import Path
import runpy


APP_PATH = Path(__file__).resolve().parent / "dashboard" / "bigscreen_app.py"
runpy.run_path(str(APP_PATH), run_name="__main__")
