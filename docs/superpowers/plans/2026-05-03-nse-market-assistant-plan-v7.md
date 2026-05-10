# NSE Market Assistant V7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Overhaul charts to use weekly line charts with percentage scale overlays, and add a TradingView Market Screener.

**Architecture:** Update `data_fetcher.py` to support variable intervals (defaulting to weekly). Refactor `app.py` to use `chart.price_scale(mode='percentage')` for synchronized overlays on a single axis. Add the Market Screener tab using the TradingView widget.

**Tech Stack:** Python 3, Streamlit, lightweight-charts, pandas, yfinance, nsepython

---

### Task 1: Refactor Data Fetcher for Weekly Intervals

**Files:**
- Modify: `src/data_fetcher.py`
- Modify: `tests/test_data_fetcher.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_data_fetcher.py
def test_fetch_nifty_data_weekly():
    from data_fetcher import fetch_nifty_data
    df = fetch_nifty_data("2023-01-01", "2023-12-31", interval="1wk")
    # Verify we get significantly fewer rows than daily (~52)
    assert len(df) < 100
```

- [ ] **Step 2: Run test to verify it fails**

Run: `source venv/bin/activate && arch -arm64 pytest tests/test_data_fetcher.py -v`
Expected: FAIL with "TypeError: fetch_nifty_data() got an unexpected keyword argument 'interval'"

- [ ] **Step 3: Update fetcher to support interval**

```python
# Replace fetch_nifty_data and fetch_macro_data in src/data_fetcher.py:

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
        df = format_for_tv(df)
        if not df.empty and 'close' in df.columns:
            df = df.rename(columns={'close': 'value'})
            return df[['time', 'value']]
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `source venv/bin/activate && arch -arm64 pytest tests/test_data_fetcher.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/data_fetcher.py tests/test_data_fetcher.py
git commit -m "feat: add support for weekly intervals in data fetchers"
```

### Task 2: Implement V7 Charting and Market Screener

**Files:**
- Modify: `src/app.py`
- Modify: `tests/test_app.py`

- [ ] **Step 1: Write the failing test**

```python
# Append to tests/test_app.py
def test_screener_tab_exists():
    from app import render_screener_tab
    assert callable(render_screener_tab)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `source venv/bin/activate && arch -arm64 pytest tests/test_app.py -v`
Expected: FAIL with ImportError.

- [ ] **Step 3: Implement Percentage Overlay UI and Screener Tab**

```python
# Overwrite src/app.py content:
import streamlit as st
import streamlit.components.v1 as components
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_nifty_pe_data
from news_scraper import get_latest_news
import datetime
from lightweight_charts.widgets import StreamlitChart

def get_app_title():
    return "NSE Market Assistant"

def create_percentage_overlay_chart(primary_df, secondary_df, indicator_name, line_color):
    """Helper to create a single-pane chart with Percentage Scale overlay."""
    if primary_df.empty:
        st.warning("Primary data missing.")
        return
        
    chart = StreamlitChart(width=1000, height=500)
    
    # 1. Set the price scale to percentage mode
    chart.price_scale(mode='percentage')
    
    # 2. Render Nifty as a Line chart for clean overlay (or Candlestick if preferred)
    # We use create_line then set() to force a line chart for the main series
    nifty_line = chart.create_line(name='Nifty 50', color='rgba(0, 123, 255, 1)')
    # Renaming column so line.set works correctly (matching fix from previous step)
    formatted_nifty = primary_df.rename(columns={'close': 'Nifty 50'})
    nifty_line.set(formatted_nifty)
    
    # 3. Add the Indicator as an overlay line on the SAME scale
    if not secondary_df.empty:
        line = chart.create_line(name=indicator_name, color=line_color)
        formatted_secondary = secondary_df.rename(columns={'value': indicator_name})
        line.set(formatted_secondary)
    else:
        st.warning(f"Secondary data ({indicator_name}) missing.")
        
    chart.load()

def render_macro_tab():
    st.header("Macro Correlation Hub (V7 - Weekly % Overlay)")
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365*2) # Show 2 years for weekly view
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    with st.spinner("Fetching weekly data..."):
        nifty_df = fetch_nifty_data(start_str, end_str, interval="1wk")

    # Panels
    st.subheader("1. Nifty 50 vs USD/INR (% Change)")
    with st.spinner("Loading USD/INR..."):
        usdinr_df = fetch_macro_data("INR=X", start_str, end_str, interval="1wk")
        create_percentage_overlay_chart(nifty_df, usdinr_df, "USD/INR", 'rgba(255, 165, 0, 1)')

    st.divider()

    st.subheader("2. Nifty 50 vs India VIX (% Change)")
    with st.spinner("Loading India VIX..."):
        vix_df = fetch_macro_data("^INDIAVIX", start_str, end_str, interval="1wk")
        create_percentage_overlay_chart(nifty_df, vix_df, "India VIX", 'rgba(255, 0, 0, 1)')

    st.divider()

    st.subheader("3. Nifty 50 vs Gold (% Change)")
    with st.spinner("Loading Gold..."):
        gold_df = fetch_macro_data("GC=F", start_str, end_str, interval="1wk")
        create_percentage_overlay_chart(nifty_df, gold_df, "Gold", 'rgba(255, 215, 0, 1)')

def render_screener_tab():
    st.header("Market Screener (TradingView)")
    screener_html = """
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
      {
      "width": "100%",
      "height": "600",
      "defaultColumn": "overview",
      "defaultScreen": "general",
      "market": "india",
      "showToolbar": true,
      "colorTheme": "dark",
      "locale": "en"
    }
      </script>
    </div>
    """
    components.html(screener_html, height=650)

def render_news_tab():
    st.header("Geopolitical & Economic News Scanner")
    if st.button("Refresh News"):
        with st.spinner("Fetching and summarizing news..."):
            news_items = get_latest_news()
            if news_items:
                for item in news_items:
                    with st.expander(item['title']):
                        st.write(f"**Date:** {item['date']}")
                        st.write(f"**AI Impact Summary:** {item['summary']}")
                        st.markdown(f"[Read full article]({item['link']})")
            else:
                st.warning("No news fetched.")

def render_kite_tab():
    st.header("Kite Integration")
    st.write("Coming Soon: Portfolio, Backtesting, and Alerts.")

if __name__ == "__main__":
    st.set_page_config(page_title=get_app_title(), layout="wide")
    st.title(get_app_title())
    
    tab1, tab2, tab3, tab4 = st.tabs(["Macro Hub", "Market Screener", "News Scanner", "Kite (Future)"])
    
    with tab1:
        render_macro_tab()
    with tab2:
        render_screener_tab()
    with tab3:
        render_news_tab()
    with tab4:
        render_kite_tab()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `source venv/bin/activate && arch -arm64 pytest tests/test_app.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/app.py tests/test_app.py
git commit -m "feat: implement weekly line charts with percentage scale and Market Screener"
```
