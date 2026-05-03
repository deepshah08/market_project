import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_fetcher import fetch_nifty_data
import pandas as pd

def test_fetch_nifty_data():
    # We will mock the yfinance call or just verify the return type
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'Close' in df.columns
