import yfinance as yf
import pandas as pd

def fetch_nifty_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches Nifty 50 daily historical data."""
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(start=start_date, end=end_date)
        return df
    except Exception:
        return pd.DataFrame()
import requests

def fetch_macro_data(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches historical data for a given macro indicator (e.g., CL=F for Crude, ^TNX for 10Y Bond)."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date)
        return df
    except Exception:
        return pd.DataFrame()

def fetch_polymarket_events() -> list:
    """Fetches active events from Polymarket Gamma API."""
    url = "https://gamma-api.polymarket.com/events?active=true&closed=false&limit=5"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []
