import yfinance as yf
import pandas as pd
import requests
import datetime
try:
    from nsepython import index_pe_pb_div
except ImportError:
    index_pe_pb_div = None

def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes market data for native Plotly usage with clean Datetime indexes."""
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    
    # Ensure we have a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        date_cols = [c for c in df.columns if 'date' in str(c).lower() or 'time' in str(c).lower()]
        if date_cols:
            df.index = pd.to_datetime(df[date_cols[0]])
        elif 'index' in df.columns:
            df.index = pd.to_datetime(df['index'])
    
    # Standardize: Sort, Remove Timezone, Drop empty
    df.index = pd.to_datetime(df.index).tz_localize(None)
    return df.sort_index().dropna(how='all')

def fetch_nifty_data(start_date: str, end_date: str, interval: str = "1wk") -> pd.DataFrame:
    """Fetches Nifty 50 historical data."""
    try:
        ticker = yf.Ticker("^NSEI")
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        return standardize_data(df)
    except Exception:
        return pd.DataFrame()

def fetch_macro_data(ticker_symbol: str, start_date: str, end_date: str, interval: str = "1wk") -> pd.DataFrame:
    """Fetches historical data for a given macro indicator."""
    try:
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start_date, end=end_date, interval=interval)
        df = standardize_data(df)
        if not df.empty and 'Close' in df.columns:
            df = df.rename(columns={'Close': 'value'})
            return df[['value']]
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def fetch_fred_data(series_id: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches macro data from FRED via direct CSV download."""
    try:
        import io
        url = f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}'
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text), parse_dates=['observation_date'], na_values='.')
            df = df.rename(columns={'observation_date': 'time_dt', series_id: 'value'})
            df.index = pd.to_datetime(df['time_dt'])
            df = standardize_data(df)
            return df[['value']]
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def fetch_nifty_pe_data(start_date: str, end_date: str) -> pd.DataFrame:
    """Fetches Nifty 50 PE ratio history using nsepython."""
    if not index_pe_pb_div:
        return pd.DataFrame()
    
    try:
        start_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        start_str = start_obj.strftime("%d-%b-%Y")
        end_str = end_obj.strftime("%d-%b-%Y")
        
        df = index_pe_pb_div("NIFTY 50", start_str, end_str)
        if df is not None and not df.empty:
            df = df.copy()
            df.index = pd.to_datetime(df['DATE'], format='%d %b %Y')
            df['value'] = pd.to_numeric(df['pe'], errors='coerce')
            df = standardize_data(df)
            return df[['value']]
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()
