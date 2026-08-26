import sys
import os
from unittest.mock import patch, MagicMock
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_fred_data, fetch_nifty_pe_data, standardize_data

def test_standardize_data():
    raw_df = pd.DataFrame({'Close': [100.0, 105.0]}, index=pd.to_datetime(['2023-01-01', '2023-01-02']))
    clean_df = standardize_data(raw_df)
    assert not clean_df.empty
    assert 'Close' in clean_df.columns

@patch('yfinance.Ticker')
def test_fetch_nifty_data(mock_ticker):
    mock_df = pd.DataFrame({'Close': [18000.0, 18100.0]}, index=pd.to_datetime(['2023-01-01', '2023-01-08']))
    mock_ticker.return_value.history.return_value = mock_df
    
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'Close' in df.columns

@patch('yfinance.Ticker')
def test_fetch_macro_data(mock_ticker):
    mock_df = pd.DataFrame({'Close': [75.0, 76.5]}, index=pd.to_datetime(['2023-01-01', '2023-01-08']))
    mock_ticker.return_value.history.return_value = mock_df
    
    df = fetch_macro_data("CL=F", "2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'value' in df.columns

@patch('requests.get')
def test_fetch_fred_data(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = "observation_date,DGS10\n2023-01-01,3.5\n2023-01-02,3.6\n"
    mock_get.return_value = mock_resp
    
    df = fetch_fred_data("DGS10", "2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'value' in df.columns

def test_fetch_nifty_pe_data():
    df = fetch_nifty_pe_data("2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
