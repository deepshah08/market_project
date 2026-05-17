# NSE Market Assistant - Design Specification V14 (Pivot)

## Overview
A Python-based (Streamlit) interactive web application serving as a Market Assistant for the Indian stock market (NSE). The application pivots to a **native Plotly synchronization engine** to ensure 100% reliability in rendering, date accuracy, and responsive design across all devices.

## Architecture
- **Frontend & UI Framework:** Streamlit (Python)
- **Charting Library:** Plotly (Synchronized Subplots)
  - Features: Locked X-axis, shared crosshairs, and synchronized zooming.
- **Data Processing:** Pandas (Native date handling)
- **Data Sources:**
  - Macroeconomic Data: `yfinance` (NSE), FRED (via direct API)
  - Valuation Data: `nsepython` (Historical Nifty P/E)
  - News Data: `BeautifulSoup`/`requests`
  - AI Summarization: Google Gemini API

## Components

### Tab A: Macro Hub (Synchronized Subplots)
- **Visualization:** A single Plotly figure with two vertical subplots.
  - Subplot 1 (Top): Nifty 50 Candlestick/Line chart.
  - Subplot 2 (Bottom): Selected Macro Indicator (USD/INR, VIX, Gold, P/E, or G-Sec).
- **Functionality:** 
  - Shared X-axis ensures zooming into a period on Nifty zooms the indicator simultaneously.
  - Hovering shows data points for both charts at the same time point.
  - Dropdown selector to switch between indicators.

### Tab B: Market Screener
- **Engine:** Official TradingView Stock Screener Widget (Embedded).

### Tab C: Geopolitical & Economic News Scanner
- AI-summarized news feed using Google Gemini.

### Tab D: Kite Integration (Future Scope)
- Placeholder for portfolio integration.

## Error Handling
- Native Streamlit error boundaries.
- Graceful fallbacks for missing data points.

## Testing Strategy
- Core data pipelines and subplot generation logic.
