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
        assert 'close' in df.columns

from data_fetcher import fetch_macro_data, fetch_polymarket_events

def test_fetch_macro_data():
    df = fetch_macro_data("CL=F", "2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)

def test_fetch_polymarket_events():
    events = fetch_polymarket_events()
    assert isinstance(events, list)

def test_fetch_nifty_data_format():
    # lightweight-charts requires specific lowercase column names
    from data_fetcher import fetch_nifty_data
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    if not df.empty:
        assert 'time' in df.columns
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns
