# NSE Market Assistant V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement interactive side-by-side charts for macroeconomic and Polymarket correlations, and integrate LLM-based news summarization.

**Architecture:** Extend existing data fetchers to pull Crude Oil, Bond Yields, and Polymarket data. Integrate Google Gemini API for summarizing scraped news. Update Streamlit UI to render Plotly charts and the enhanced news feed.

**Tech Stack:** Python 3, Streamlit, pandas, yfinance, plotly, requests, google-genai, pytest

---

### Task 1: Update Dependencies and LLM Stub

**Files:**
- Modify: `requirements.txt`
- Create: `src/llm_summarizer.py`
- Create: `tests/test_llm_summarizer.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm_summarizer.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from llm_summarizer import summarize_news

def test_summarize_news():
    # Test with a mock response or empty key handling
    summary = summarize_news("RBI holds interest rates steady.")
    assert isinstance(summary, str)
    assert len(summary) > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_llm_summarizer.py -v`
Expected: FAIL with "ImportError: cannot import name 'summarize_news'"

- [ ] **Step 3: Write minimal implementation**

```txt
# Append to requirements.txt
google-genai
```

```python
# src/llm_summarizer.py
import os
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

def summarize_news(headline: str) -> str:
    """Summarizes news using Gemini API, or returns a default message if no key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or not genai:
        return f"AI Summary (Mock): Market impact for '{headline}' is neutral."
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Briefly summarize the potential Indian stock market impact of this headline in 1-2 sentences: {headline}"
        )
        return response.text
    except Exception as e:
        return f"AI Summary Error: {str(e)}"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pip install -r requirements.txt && pytest tests/test_llm_summarizer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt src/llm_summarizer.py tests/test_llm_summarizer.py
git commit -m "feat: add llm summarizer module and dependencies"
```

### Task 2: Extend Data Fetcher for Macro and Polymarket

**Files:**
- Modify: `src/data_fetcher.py`
- Modify: `tests/test_data_fetcher.py`

- [ ] **Step 1: Write the failing test**

```python
# Append to tests/test_data_fetcher.py
from data_fetcher import fetch_macro_data, fetch_polymarket_events

def test_fetch_macro_data():
    df = fetch_macro_data("CL=F", "2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)

def test_fetch_polymarket_events():
    events = fetch_polymarket_events()
    assert isinstance(events, list)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_fetcher.py -v`
Expected: FAIL with ImportError for the new functions.

- [ ] **Step 3: Write minimal implementation**

```python
# Append to src/data_fetcher.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_fetcher.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/data_fetcher.py tests/test_data_fetcher.py
git commit -m "feat: add macro and polymarket data fetchers"
```

### Task 3: Integrate LLM with News Scraper

**Files:**
- Modify: `src/news_scraper.py`

- [ ] **Step 1: Write the failing test**

No new test needed, existing test checks for "summary" key. We will modify the implementation to use the actual summarizer.

- [ ] **Step 2: Modify implementation to use LLM**

```python
# Replace src/news_scraper.py content with:
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from .llm_summarizer import summarize_news

def get_latest_news() -> list:
    """Fetches recent financial news via Google News RSS and adds AI summaries."""
    url = "https://news.google.com/rss/search?q=India+Business+Finance&hl=en-IN&gl=IN&ceid=IN:en"
    news_items = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('./channel/item')[:5]: # Reduced to 5 to save API calls
                title = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ""
                summary = summarize_news(title)
                news_items.append({"title": title, "link": link, "date": pubDate, "summary": summary})
    except Exception as e:
        pass
    return news_items
```

- [ ] **Step 3: Run test to verify it passes**

Run: `pytest tests/test_news_scraper.py -v`
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add src/news_scraper.py
git commit -m "feat: integrate llm summarization into news scraper"
```

### Task 4: Build Side-by-Side Charts and News UI

**Files:**
- Modify: `src/app.py`

- [ ] **Step 1: Write the implementation for Tab A and Tab B**

```python
# Replace src/app.py content with:
import streamlit as st
import plotly.graph_objects as go
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_polymarket_events
from news_scraper import get_latest_news
import datetime

def get_app_title():
    return "NSE Market Assistant"

def render_macro_tab():
    st.header("Macro & Polymarket Correlation Hub")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Nifty 50")
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=180)
        nifty_df = fetch_nifty_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        
        if not nifty_df.empty:
            fig_nifty = go.Figure(data=[go.Scatter(x=nifty_df.index, y=nifty_df['Close'], name='Nifty 50')])
            fig_nifty.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300)
            st.plotly_chart(fig_nifty, use_container_width=True)
        else:
            st.warning("Could not fetch Nifty data.")

    with col2:
        st.subheader("Secondary Indicator")
        indicator = st.selectbox("Select Indicator", ["Crude Oil (CL=F)", "US 10Y Bond (^TNX)", "Polymarket Events"])
        
        if indicator == "Polymarket Events":
            events = fetch_polymarket_events()
            if events:
                event_titles = [e.get('title', 'Unknown') for e in events]
                selected_event = st.selectbox("Select Event", event_titles)
                st.info("Polymarket probability charts require historical data APIs which are complex. Showing current active events for now.")
                st.write(f"Tracking: {selected_event}")
            else:
                st.warning("Could not fetch Polymarket events.")
        else:
            ticker = "CL=F" if "Crude" in indicator else "^TNX"
            macro_df = fetch_macro_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            if not macro_df.empty:
                fig_macro = go.Figure(data=[go.Scatter(x=macro_df.index, y=macro_df['Close'], name=indicator, line=dict(color='orange'))])
                fig_macro.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300)
                st.plotly_chart(fig_macro, use_container_width=True)
            else:
                st.warning(f"Could not fetch data for {indicator}.")

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
    
    tab1, tab2, tab3 = st.tabs(["Macro Hub", "News Scanner", "Kite (Future)"])
    
    with tab1:
        render_macro_tab()
    with tab2:
        render_news_tab()
    with tab3:
        render_kite_tab()
```

- [ ] **Step 2: Run test to verify it passes**

Run: `pytest tests/test_app.py -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add src/app.py
git commit -m "feat: implement side-by-side charts and news UI"
```
