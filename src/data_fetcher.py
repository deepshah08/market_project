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
