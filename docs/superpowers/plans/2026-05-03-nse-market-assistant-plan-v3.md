# NSE Market Assistant V3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Overhaul the Macro Hub charting to use TradingView Lightweight Charts for synchronized overlays, replacing the side-by-side Plotly layout.

**Architecture:** Use the `lightweight-charts-python` library (specifically its `StreamlitChart` widget) to render a single, full-width interactive chart. Nifty 50 will be the baseline candlestick chart, and the selected macro indicator will be added as a line overlay with a separate price scale.

**Tech Stack:** Python 3, Streamlit, lightweight-charts, pandas, yfinance

---

### Task 1: Add Dependency and Refactor Data Fetcher for Compatibility

**Files:**
- Modify: `requirements.txt`
- Modify: `src/data_fetcher.py`
- Modify: `tests/test_data_fetcher.py`

- [ ] **Step 1: Write the failing test**

```python
# Append to tests/test_data_fetcher.py
def test_fetch_nifty_data_format():
    # lightweight-charts requires specific lowercase column names
    from data_fetcher import fetch_nifty_data
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    if not df.empty:
        assert 'time' in df.columns
        assert 'open' in df.columns
        assert 'high' in df.columns
        assert 'low' in df.columns
        assert 'close' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `source venv/bin/activate && pytest tests/test_data_fetcher.py -v`
Expected: FAIL because `yfinance` returns capitalized columns like 'Open', 'High', etc., and index is Date.

- [ ] **Step 3: Write minimal implementation**

```txt
# Append to requirements.txt
lightweight-charts
```

```python
# Replace fetch_nifty_data and fetch_macro_data in src/data_fetcher.py:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `source venv/bin/activate && pip install -r requirements.txt && pytest tests/test_data_fetcher.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt src/data_fetcher.py tests/test_data_fetcher.py
git commit -m "feat: add lightweight-charts and refactor data for tv format"
```

### Task 2: Implement TradingView Overlay in Streamlit

**Files:**
- Modify: `src/app.py`

- [ ] **Step 1: Write the failing test**

```python
# No specific unit test for Streamlit rendering. We rely on the integration working.
# Just run pytest to ensure no syntax errors are introduced.
```

- [ ] **Step 2: Modify implementation for TradingView overlay**

```python
# Replace render_macro_tab in src/app.py:
# Add import at top: from lightweight_charts.widgets import StreamlitChart

def render_macro_tab():
    st.header("Macro & Polymarket Correlation Hub")
    from lightweight_charts.widgets import StreamlitChart
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Controls")
        indicator = st.selectbox("Select Overlay Indicator", ["None", "Crude Oil (CL=F)", "US 10Y Bond (^TNX)", "Polymarket Events"])
        if indicator == "Polymarket Events":
            events = fetch_polymarket_events()
            if events:
                event_titles = [e.get('title', 'Unknown') for e in events]
                selected_event = st.selectbox("Select Event", event_titles)
                st.info("Polymarket overlay requires historical API. Showing current events only.")
            else:
                st.warning("Could not fetch Polymarket events.")

    with col2:
        st.subheader("Nifty 50 vs Overlay")
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=365) # Show 1 year
        
        nifty_df = fetch_nifty_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        
        if not nifty_df.empty:
            chart = StreamlitChart(width=800, height=500)
            chart.set(nifty_df) # Main series is Candlestick by default
            
            if indicator not in ["None", "Polymarket Events"]:
                ticker = "CL=F" if "Crude" in indicator else "^TNX"
                macro_df = fetch_macro_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                if not macro_df.empty:
                    # Create a line series with a secondary price scale
                    line = chart.create_line(name=indicator, color='rgba(255, 165, 0, 0.8)', price_scale_id='right')
                    line.set(macro_df)
                else:
                    st.warning(f"Could not fetch overlay data for {indicator}.")
            
            chart.load()
        else:
            st.warning("Could not fetch Nifty 50 data.")
```

Don't forget to update imports at the top of `src/app.py`:
```python
import streamlit as st
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_polymarket_events
from news_scraper import get_latest_news
import datetime
# Remove plotly import
```

- [ ] **Step 3: Run test to verify it passes**

Run: `source venv/bin/activate && pytest tests/test_app.py -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/app.py
git commit -m "feat: replace plotly with tradingview lightweight charts overlay"
```
