import yfinance as yf
import pandas as pd
import requests
import datetime
try:
    from nsepython import index_pe_pb_div
except ImportError:
    index_pe_pb_div = None

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
    
    # Drop rows with NaN in the 'close' column (or 'value' later) to prevent chart breaks
    if 'close' in df.columns:
        df = df.dropna(subset=['close'])
        return df[['time', 'open', 'high', 'low', 'close', 'volume']]
    
    return df

def fetch_nifty_data(start_date: str, end_date: str, interval: str = "1wk") -> pd.DataFrame:
    """Fetches Nifty 50 historical data with selectable interval."""
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        return format_for_tv(df)
    except Exception:
        return pd.DataFrame()

def fetch_macro_data(ticker_symbol: str, start_date: str, end_date: str, interval: str = "1wk") -> pd.DataFrame:
    """Fetches historical data for a given macro indicator with selectable interval."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        # Macro data is usually just a line, so we just need time and value
        df = format_for_tv(df)
        if not df.empty and 'close' in df.columns:
            df = df.rename(columns={'close': 'value'})
            return df[['time', 'value']]
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def fetch_nifty_pe_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches Nifty 50 PE ratio history using nsepython."""
    if not index_pe_pb_div:
        return pd.DataFrame()
    
    try:
        # nsepython requires dates in "DD-Mon-YYYY" or "DD-MM-YYYY" format
        # start_date and end_date come in as YYYY-MM-DD
        start_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        # Using DD-Mon-YYYY which is standard for NSE
        start_str = start_obj.strftime("%d-%b-%Y")
        end_str = end_obj.strftime("%d-%b-%Y")
        
        df = index_pe_pb_div("NIFTY 50", start_str, end_str)
        if df is not None and not df.empty:
            # df has 'Date', 'P/E', 'P/B', 'Div Yield'
            # Convert 'Date' back to 'YYYY-MM-DD' for TradingView
            df['Date'] = pd.to_datetime(df['Date'])
            df['time'] = df['Date'].dt.strftime('%Y-%m-%d')
            df['value'] = pd.to_numeric(df['P/E'], errors='coerce')
            df = df.dropna(subset=['value'])
            
            # Sort chronologically
            df = df.sort_values(by='Date')
            
            return df[['time', 'value']]
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
