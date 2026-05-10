import yfinance as yf
import pandas as pd
import requests
import datetime
try:
    from nsepython import index_pe_pb_div
except ImportError:
    index_pe_pb_div = None

def format_for_tv(df: pd.DataFrame) -> pd.DataFrame:
    """Formats yfinance/nsepython dataframe for TradingView Lightweight Charts using clean YYYY-MM-DD strings."""
    if df.empty:
        return pd.DataFrame()
    
    df = df.copy()
    
    # Identify the actual datetime source
    if isinstance(df.index, pd.DatetimeIndex):
        df['time_dt'] = df.index
    else:
        # Check for date columns
        date_cols = [c for c in df.columns if 'date' in str(c).lower() or 'time' in str(c).lower()]
        if date_cols:
            df['time_dt'] = pd.to_datetime(df[date_cols[0]])
        else:
            return pd.DataFrame()
    
    # Convert to clean datetime.date objects
    # This is often the most reliable format for library-agnostic date handling
    df['time'] = pd.to_datetime(df['time_dt']).dt.tz_localize(None).dt.date
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['time'])
    
    # Clean up and rename columns
    df = df.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    })
    
    # Standardize columns
    target_cols = ['time', 'open', 'high', 'low', 'close', 'volume']
    existing_cols = [c for c in target_cols if c in df.columns]
    
    # Final cleanup: drop any remaining NaNs and sort
    return df[existing_cols].dropna().sort_values('time').reset_index(drop=True)

def fetch_nifty_data(start_date: str, end_date: str, interval: str = "1wk") -> pd.DataFrame:
    """Fetches Nifty 50 historical data."""
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        return format_for_tv(df)
    except Exception:
        return pd.DataFrame()

def fetch_macro_data(ticker_symbol: str, start_date: str, end_date: str, interval: str = "1wk") -> pd.DataFrame:
    """Fetches historical data for a given macro indicator."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        df = format_for_tv(df)
        if not df.empty and 'close' in df.columns:
            df = df.rename(columns={'close': 'value'})
            return df[['time', 'value']]
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def fetch_fred_data(series_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches macro data from FRED."""
    try:
        df = web.DataReader(series_id, 'fred', start_date, end_date)
        df = format_for_tv(df)
        if not df.empty:
            # FRED usually has one column with the series ID as name
            df = df.rename(columns={series_id: 'value'})
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
            # Force cleanup and conversion
            df = df.copy()
            df['time_dt'] = pd.to_datetime(df['DATE'])
            df['time'] = df['time_dt'].dt.date
            df['value'] = pd.to_numeric(df['pe'], errors='coerce')
            
            # Drop invalid values and sort
            return df[['time', 'value']].dropna().sort_values(by='time').reset_index(drop=True)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
