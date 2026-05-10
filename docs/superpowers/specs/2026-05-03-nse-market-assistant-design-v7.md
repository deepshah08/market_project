# NSE Market Assistant - Design Specification V7

## Overview
A Python-based (Streamlit) interactive web application serving as a Market Assistant for the Indian stock market (NSE). The application focuses on analyzing historical correlations using synchronized weekly percentage-scale charts and providing a professional-grade stock screener.

## Architecture
- **Frontend & UI Framework:** Streamlit (Python)
- **Charting Library:** TradingView Lightweight Charts (`lightweight-charts-python`) using **Percentage Scale Overlay**.
- **Stock Screener:** TradingView Embedded Screener Widget (Indian Market).
- **Data Processing:** Pandas
- **Data Sources:**
  - Macroeconomic Data: `yfinance` (NSE), `pandas_datareader` (FRED for Bond Yields)
  - Valuation Data: `nsepython` (Historical Nifty P/E)
  - News Data: `BeautifulSoup`/`requests` (Google News RSS scraping)
  - AI Summarization: Google Gemini API

## Components

### Tab A: Macro Hub (Percentage Overlay)
- **Visualization:** Single-pane, full-width TradingView charts.
- **Scale:** **Percentage Mode** (`chart.price_scale(mode='percentage')`). This normalizes both the Nifty 50 and the indicator to start at 0% on the left of the screen, allowing for direct comparison of relative performance.
- **Interval:** **Weekly Data** (1wk) for better high-level trend analysis and noise reduction.
- **Type:** Line charts for both Nifty 50 and the indicator overlay.
- **Panels:**
  - Panel 1: Nifty 50 % vs USD/INR %
  - Panel 2: Nifty 50 % vs India VIX %
  - Panel 3: Nifty 50 % vs Gold Futures %
  - Panel 4: Nifty 50 % vs Nifty P/E Ratio %

### Tab B: Market Screener
- **Engine:** Official TradingView Stock Screener Widget.
- **Configuration:** Set to the Indian Market with technical and fundamental filtering.

### Tab C: Geopolitical & Economic News Scanner
- Feed of recently scraped news from Google News RSS with Gemini-generated market impact summaries.

### Tab D: Kite Integration (Future Scope)
- Placeholder for upcoming portfolio integration.

## Error Handling
- Robust NaN handling in DataFrames to prevent chart rendering failures.
- API timeouts and LLM fallbacks.

## Testing Strategy
- Core data fetchers (including weekly interval logic) tested via `pytest`.
- UI structure verification.
