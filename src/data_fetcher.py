import yfinance as yf
import pandas as pd
import requests

def format_for_tv(df: pd.DataFrame) -> pd.DataFrame:
    """Formats yfinance dataframe for TradingView Lightweight Charts."""
    if df.empty:
        return df
    df = df.reset_index()
    # Handle timezone-aware dates by converting to string
    if 'Date' in df.columns:
        df['time'] = df['Date'].dt.strftime('%Y-%m-%d')
    elif 'Datetime' in df.columns:
        df['time'] = df['Datetime'].dt.strftime('%Y-%m-%d')
    
    df = df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    })
    return df[['time', 'open', 'high', 'low', 'close', 'volume']]

def fetch_nifty_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches Nifty 50 daily historical data."""
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(start=start_date, end=end_date)
        return format_for_tv(df)
    except Exception:
        return pd.DataFrame()

def fetch_macro_data(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches historical data for a given macro indicator."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date)
        # Macro data is usually just a line, so we just need time and value
        df = format_for_tv(df)
        if not df.empty:
            df = df.rename(columns={'close': 'value'})
            return df[['time', 'value']]
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
