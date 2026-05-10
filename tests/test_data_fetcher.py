import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_nifty_pe_data
import pandas as pd

def test_fetch_nifty_data():
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'close' in df.columns

def test_fetch_macro_data():
    df = fetch_macro_data("CL=F", "2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)

def test_fetch_nifty_pe_data():
    df = fetch_nifty_pe_data("2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)

def test_fetch_nifty_data_format():
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    if not df.empty:
        assert 'time' in df.columns
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns

def test_fetch_nifty_data_weekly():
    from data_fetcher import fetch_nifty_data
    df = fetch_nifty_data("2023-01-01", "2023-12-31", interval="1wk")
    # Verify we get significantly fewer rows than daily (~52)
    assert len(df) < 100
