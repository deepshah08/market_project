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
        return pd.DataFrame()
    
    # Force a fresh copy to avoid view warnings
    df = df.copy()
    
    # Identify the actual datetime column or index
    if not isinstance(df.index, pd.DatetimeIndex):
        date_cols = [c for c in df.columns if 'date' in str(c).lower() or 'time' in str(c).lower()]
        if date_cols:
            df['time_raw'] = pd.to_datetime(df[date_cols[0]])
        else:
            if 'index' in df.columns:
                try:
                    df['time_raw'] = pd.to_datetime(df['index'])
                except:
                    return pd.DataFrame()
            else:
                return pd.DataFrame()
    else:
        df['time_raw'] = df.index
    
    # Convert to clean YYYY-MM-DD string, dropping timezone
    df['time'] = pd.to_datetime(df['time_raw']).dt.tz_localize(None).dt.strftime('%Y-%m-%d')
    df = df.dropna(subset=['time'])
    
    df = df.rename(columns={
        'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    })
    
    # Drop NaNs in close to avoid chart distortion
    if 'close' in df.columns:
        df = df.dropna(subset=['close'])
    
    return df.sort_values('time')

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
            # df has 'Date', 'P/E', 'P/B', 'Div Yield'
            # Force cleanup and conversion
            df = df.copy()
            df['time_raw'] = pd.to_datetime(df['Date'])
            df['time'] = df['time_raw'].dt.strftime('%Y-%m-%d')
            df['value'] = pd.to_numeric(df['P/E'], errors='coerce')
            
            # Drop invalid values and sort
            df = df.dropna(subset=['time', 'value'])
            df = df.sort_values(by='time_raw')
            
            return df[['time', 'value']]
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()
