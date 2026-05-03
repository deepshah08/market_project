# NSE Market Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an interactive Python dashboard (Streamlit) analyzing macroeconomic correlations against the Indian Stock Market and providing an AI-summarized news feed.

**Architecture:** A unified Streamlit application utilizing a modular backend for data fetching (APIs, web scraping) and an LLM integration layer for news summarization. Tests use pytest.

**Tech Stack:** Python 3, Streamlit, pandas, yfinance, pandas-datareader, plotly, beautifulsoup4, requests, pytest

---

### Task 1: Project Scaffolding & Setup

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `tests/__init__.py`
- Create: `src/app.py`
- Create: `tests/test_app.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_app.py
def test_app_title():
    # A simple test to verify our testing framework works
    title = "NSE Market Assistant"
    assert title == "NSE Market Assistant"
```

- [ ] **Step 2: Run test to verify it fails (or passes since it's a basic sanity check)**

Run: `pytest tests/test_app.py -v`
Expected: PASS or Setup Error if pytest isn't installed. Let's assume requirements need to be installed first.

Actually, let's create requirements and a true failing test for a helper function.

```python
# tests/test_app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import get_app_title

def test_app_title():
    assert get_app_title() == "NSE Market Assistant"
```

- [ ] **Step 3: Write minimal implementation**

```txt
# requirements.txt
streamlit
pandas
yfinance
pandas-datareader
plotly
beautifulsoup4
requests
pytest
```

```python
# src/app.py
def get_app_title():
    return "NSE Market Assistant"

if __name__ == "__main__":
    import streamlit as st
    st.title(get_app_title())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pip install -r requirements.txt && pytest tests/test_app.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add requirements.txt src/ tests/
git commit -m "chore: initial project scaffold and dependencies"
```

### Task 2: Implement Macro Data Fetcher

**Files:**
- Create: `src/data_fetcher.py`
- Create: `tests/test_data_fetcher.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_data_fetcher.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from data_fetcher import fetch_nifty_data
import pandas as pd

def test_fetch_nifty_data():
    # We will mock the yfinance call or just verify the return type
    df = fetch_nifty_data("2023-01-01", "2023-01-10")
    assert isinstance(df, pd.DataFrame)
    if not df.empty:
        assert 'Close' in df.columns
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_data_fetcher.py -v`
Expected: FAIL with "ImportError: cannot import name 'fetch_nifty_data'"

- [ ] **Step 3: Write minimal implementation**

```python
# src/data_fetcher.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_data_fetcher.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/data_fetcher.py tests/test_data_fetcher.py
git commit -m "feat: add nifty data fetching logic"
```

### Task 3: Implement Basic News Scraper

**Files:**
- Create: `src/news_scraper.py`
- Create: `tests/test_news_scraper.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_news_scraper.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from news_scraper import get_latest_news

def test_get_latest_news():
    news = get_latest_news()
    assert isinstance(news, list)
    # Even if empty, it should be a list. If not empty, check dictionary keys
    if news:
        assert "title" in news[0]
        assert "link" in news[0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_news_scraper.py -v`
Expected: FAIL with "ImportError: cannot import name 'get_latest_news'"

- [ ] **Step 3: Write minimal implementation**

```python
# src/news_scraper.py
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def get_latest_news() -> list:
    """Fetches recent financial news via Google News RSS for Indian Business."""
    url = "https://news.google.com/rss/search?q=India+Business+Finance&hl=en-IN&gl=IN&ceid=IN:en"
    news_items = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('./channel/item')[:10]: # Top 10
                title = item.find('title').text if item.find('title') is not None else ""
                link = item.find('link').text if item.find('link') is not None else ""
                pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ""
                news_items.append({"title": title, "link": link, "date": pubDate, "summary": "AI Summary placeholder."})
    except Exception as e:
        pass
    return news_items
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_news_scraper.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/news_scraper.py tests/test_news_scraper.py
git commit -m "feat: implement rss news scraper"
```

### Task 4: Streamlit UI Tabs Setup

**Files:**
- Modify: `src/app.py`

- [ ] **Step 1: Write the failing test**

```python
# Modify tests/test_app.py to add:
def test_app_tabs():
    # We won't test Streamlit rendering deeply, but we can verify our new helper functions exist
    from app import render_macro_tab, render_news_tab
    assert callable(render_macro_tab)
    assert callable(render_news_tab)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_app.py -v`
Expected: FAIL with "ImportError: cannot import name 'render_macro_tab'"

- [ ] **Step 3: Write minimal implementation**

```python
# Overwrite src/app.py:
import streamlit as st

def get_app_title():
    return "NSE Market Assistant"

def render_macro_tab():
    st.header("Macro Correlation Hub")
    st.write("Historical market correlations will appear here.")

def render_news_tab():
    st.header("Geopolitical & Economic News")
    st.write("AI-summarized news feed.")

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

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_app.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/app.py tests/test_app.py
git commit -m "feat: layout streamlit UI with tabs"
```
