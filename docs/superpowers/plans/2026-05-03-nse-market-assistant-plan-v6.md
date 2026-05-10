# NSE Market Assistant V6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a professional-grade Market Screener tab using the TradingView embedded widget.

**Architecture:** Utilize `streamlit.components.v1.html` to embed the TradingView Stock Screener JS snippet. Configure it for the Indian market and integrate it into the main tabbed interface of the Streamlit application.

**Tech Stack:** Python 3, Streamlit

---

### Task 1: Implement Market Screener Component

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
Expected: FAIL with "ImportError: cannot import name 'render_screener_tab'"

- [ ] **Step 3: Implement the screener function**

```python
# Add import to top of src/app.py:
import streamlit.components.v1 as components

# Add function to src/app.py:
def render_screener_tab():
    st.header("Market Screener (Powered by TradingView)")
    
    # TradingView Screener Widget HTML/JS snippet
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
```

- [ ] **Step 4: Update the UI Tab layout**

```python
# Update the main block in src/app.py:
if __name__ == "__main__":
    st.set_page_config(page_title=get_app_title(), layout="wide")
    st.title(get_app_title())
    
    # Reordered tabs to put Screener second
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

- [ ] **Step 5: Run test to verify it passes**

Run: `source venv/bin/activate && arch -arm64 pytest tests/test_app.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add src/app.py tests/test_app.py
git commit -m "feat: add professional TradingView Market Screener tab"
```
