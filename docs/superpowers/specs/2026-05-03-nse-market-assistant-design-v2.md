# NSE Market Assistant - Design Specification V2

## Overview
A Python-based (Streamlit) interactive web application serving as a Market Assistant for the Indian stock market (NSE). The application focuses on analyzing historical correlations between macroeconomic factors, prediction markets (Polymarket), and the NSE. It also provides an AI-summarized news section for relevant financial and geopolitical updates.

## Architecture
- **Frontend & UI Framework:** Streamlit (Python)
- **Charting Library:** Plotly (for interactive side-by-side charts)
- **Data Processing:** Pandas
- **Data Sources:**
  - Macroeconomic Data: `yfinance` (NSE), `pandas_datareader` (FRED for Bond Yields)
  - Prediction Markets: Polymarket Gamma API (for event probabilities)
  - News Data: `BeautifulSoup`/`requests` (Google News RSS scraping)
  - AI Summarization: Google Gemini API (or similar free-tier LLM)

## Components

### Tab A: Macro & Polymarket Correlation Hub
- **Controls:** Dropdowns to select the primary asset (e.g., Nifty 50) and a secondary indicator (Crude Oil, 10Y US Bond Yields, INR/USD, or specific Polymarket event probabilities).
- **Visualization:** Side-by-side interactive Plotly charts allowing users to visually track specific peaks and troughs between the two selected assets over time.

### Tab B: Geopolitical & Economic News Scanner
- A feed of recently scraped news from Google News RSS (focused on Indian Business/Finance).
- An AI-generated summary attached to each headline that extracts the potential market impact of the news event.

### Tab C: Kite Integration (Future Scope)
- A placeholder section outlining future integration plans for fetching portfolio data, setting up alerts, and backtesting strategies based on insights from the other tabs.

## Error Handling
- The app will handle API rate limits and web scraping errors gracefully, displaying placeholder data or a warning message to the user rather than crashing the application.
- All LLM and external API interactions will have fallback responses and timeouts.

## Testing Strategy
- Core data processing, API fetching, and correlation functions will have unit tests using `pytest`.
- Web scraping functions will be tested against mock XML/HTML responses to ensure resilience.
