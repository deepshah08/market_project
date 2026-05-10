import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import get_app_title

def test_app_title():
    assert get_app_title() == "NSE Market Assistant"

def test_app_tabs():
    # We won't test Streamlit rendering deeply, but we can verify our new helper functions exist
    from app import render_macro_tab, render_news_tab
    assert callable(render_macro_tab)
    assert callable(render_news_tab)

def test_screener_tab_exists():
    from app import render_screener_tab
    assert callable(render_screener_tab)
