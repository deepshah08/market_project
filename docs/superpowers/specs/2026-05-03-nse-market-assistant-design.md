# NSE Market Assistant - Design Specification

## Overview
A Python-based (Streamlit) interactive web application serving as a Market Assistant for the Indian stock market (NSE). The application focuses on historical correlations between macroeconomic/geopolitical factors and the market, and provides an AI-summarized news section for relevant financial and economic updates.

## Architecture
- **Frontend & UI Framework:** Streamlit (Python)
- **Charting Library:** Plotly
- **Data Processing:** Pandas
- **Data Sources:**
  - Macroeconomic Data: `yfinance`, `pandas_datareader` (FRED)
  - News Data: `BeautifulSoup`/`requests` (Web scraping)
  - AI Summarization: Google Gemini API (or similar free-tier LLM API)

## Components

### Tab A: Macro Correlation Hub
- Central interactive Plotly chart mapping the Nifty 50 index (`^NSEI`) against selectable macro indicators (Crude Oil, 10Y US Bond Yields, INR/USD exchange rate).
- Correlation Matrix showing historical correlations between the Nifty 50 and selected macro indicators.

### Tab B: Geopolitical & Economic News Scanner
- A feed of recently scraped news categorized by topic (Finance, Geopolitics, Corporate).
- AI Summary next to each headline that extracts the potential market impact of the news.

### Tab C: Kite Integration (Placeholder)
- A section outlining future integration plans for fetching portfolio data, setting up alerts, and backtesting strategies based on insights from the other tabs.

## Error Handling
- The app will handle API rate limits and web scraping errors gracefully, displaying placeholder data or a warning message to the user rather than crashing the application.
- All LLM interactions will have fallback responses if the API fails or times out.

## Testing Strategy
- Core data processing and correlation functions will have unit tests using `pytest`.
- Web scraping functions will be tested against mock HTML responses to ensure resilience against minor layout changes.
