import yfinance as yf
import pandas as pd
import requests
import datetime
try:
    from nsepython import index_pe_pb_div
except ImportError:
    index_pe_pb_div = None

def format_for_tv(df: pd.DataFrame) -> pd.DataFrame:
    """Formats yfinance/nsepython dataframe for TradingView Lightweight Charts using clean Unix Timestamps (seconds)."""
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
    
    # Convert to clean Unix Timestamps (Nanoseconds as integers)
    # This is the ONLY format that survives the library's internal pd.to_datetime() // 10^9 
    # logic across different Pandas versions (1.x and 2.x).
    df['time'] = pd.to_datetime(df['time_dt']).dt.tz_localize(None).apply(lambda x: int(x.timestamp() * 10**9))
    
    # Drop rows with invalid dates
    df = df.dropna(subset=['time'])
    
    df = df.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    })
    
    # Ensure standard columns are present and numeric
    for col in ['open', 'high', 'low', 'close', 'volume']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Final column selection
    target_cols = ['time', 'open', 'high', 'low', 'close', 'volume']
    existing_cols = [c for c in target_cols if c in df.columns]
    
    # Reset index and sort
    return df[existing_cols].sort_values('time').reset_index(drop=True)

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
    """Fetches macro data from FRED via direct CSV download to bypass pandas_datareader issues."""
    try:
        import io
        url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
        # Use verify=False to bypass common macOS Python SSL certificate issues
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text), parse_dates=['observation_date'], na_values='.')
            df = df.rename(columns={'observation_date': 'time_dt', series_id: 'value'})
            
            # Format to unix timestamp (nanoseconds as integers)
            df['time'] = pd.to_datetime(df['time_dt']).dt.tz_localize(None).apply(lambda x: int(x.timestamp() * 10**9))
            
            # Clean up
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            df = df.dropna(subset=['time', 'value'])
            return df[['time', 'value']].sort_values('time').reset_index(drop=True)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

def fetch_nifty_pe_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches Nifty 50 PE ratio history using nsepython."""
    if not index_pe_pb_div:
        return pd.DataFrame()
    
    try:
        # nsepython requires dates in "DD-Mon-YYYY" format
        start_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        start_str = start_obj.strftime("%d-%b-%Y")
        end_str = end_obj.strftime("%d-%b-%Y")
        
        df = index_pe_pb_div("NIFTY 50", start_str, end_str)
        if df is not None and not df.empty:
            df = df.copy()
            # Format to unix timestamp (nanoseconds as integers)
            df['time_dt'] = pd.to_datetime(df['DATE'], format='%d %b %Y')
            df['time'] = df['time_dt'].dt.tz_localize(None).apply(lambda x: int(x.timestamp() * 10**9))
            df['value'] = pd.to_numeric(df['pe'], errors='coerce')
            
            return df[['time', 'value']].dropna().sort_values(by='time').reset_index(drop=True)
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
