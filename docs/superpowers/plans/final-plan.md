# NSE Market Assistant V14 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Pivot to a stable, synchronized Plotly dual-pane layout.

**Architecture:** Use `plotly.subplots.make_subplots` with `shared_xaxes=True`. Refactor data fetchers to return standard DataFrames with clean Pandas Datetime indexes.

**Tech Stack:** Python 3, Streamlit, Plotly, pandas, yfinance, nsepython

---

### Task 1: Refactor Data Fetchers for Native Pandas/Plotly

**Files:**
- Modify: `src/data_fetcher.py`
- Modify: `tests/test_data_fetcher.py`

- [ ] **Step 1: Simplify `format_for_tv` (renaming to `standardize_data`)**

```python
def standardize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes yfinance data for native Plotly usage."""
    if df.empty: return pd.DataFrame()
    df = df.copy()
    # Keep DatetimeIndex, but ensure it's sorted and timezone-naive for Plotly
    if isinstance(df.index, pd.DatetimeIndex):
        df.index = df.index.tz_localize(None)
    return df.sort_index().dropna(how='all')
```

- [ ] **Step 2: Update all fetchers to return cleaned DataFrames**

- [ ] **Step 3: Verify unit tests pass.**

### Task 2: Implement Synchronized Plotly Subplots

**Files:**
- Modify: `src/app.py`

- [ ] **Step 1: Implement `create_synced_subplot_chart`**

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def create_synced_subplot_chart(nifty_df, indicator_df, indicator_name):
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05,
        row_heights=[0.6, 0.4]
    )
    
    # Nifty in Row 1
    fig.add_trace(go.Scatter(x=nifty_df.index, y=nifty_df['Close'], name='Nifty 50'), row=1, col=1)
    
    # Indicator in Row 2
    fig.add_trace(go.Scatter(x=indicator_df.index, y=indicator_df['value'], name=indicator_name), row=2, col=1)
    
    fig.update_layout(height=800, template='plotly_dark', hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
```

- [ ] **Step 2: Update `render_macro_tab` to use the new engine.**

- [ ] **Step 3: Run autonomous visual testing loop to verify stability.**
