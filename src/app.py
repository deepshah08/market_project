import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_nifty_pe_data
from news_scraper import get_latest_news
import datetime
from lightweight_charts.widgets import StreamlitChart

def get_app_title():
    return "NSE Market Assistant"

@st.cache_data
def get_cached_nifty(start_str, end_str):
    return fetch_nifty_data(start_str, end_str, interval="1wk")

@st.cache_data
def get_cached_macro(ticker, start_str, end_str):
    return fetch_macro_data(ticker, start_str, end_str, interval="1wk")

@st.cache_data(ttl=3600)
def get_cached_pe(start_str, end_str):
    return fetch_nifty_pe_data(start_str, end_str)

def create_dual_pane_chart(primary_df, secondary_df, indicator_name, line_color):
    """Creates a two-pane synchronized chart (Top: Nifty, Bottom: Indicator) with responsive width."""
    if primary_df.empty:
        st.warning("Primary data (Nifty 50) missing.")
        return
        
    # Using height=800 and width=None (default) for responsive behavior
    chart = StreamlitChart(height=800)
    
    # Render Nifty in the top pane
    chart.set(primary_df)
    
    # Create subchart (Bottom pane), synced with main
    if not secondary_df.empty:
        # 0.4 height means 40% of the main chart height
        subchart = chart.create_subchart(height=0.4, sync=True)
        line = subchart.create_line(name=indicator_name, color=line_color)
        
        # Match column name to line name for library compatibility
        formatted_secondary = secondary_df.rename(columns={'value': indicator_name})
        line.set(formatted_secondary)
    else:
        st.warning(f"Data for {indicator_name} missing.")
        
    # FIX for invisible charts: Force the internal container to fill the Streamlit iframe
    chart.run_script("""
        var container = document.getElementById('container');
        if (container) {
            container.style.width = '100%';
            container.style.height = '100vh';
        }
    """)
        
    chart.load()

def render_macro_tab():
    st.header("Macro Correlation Hub (Dual-Pane Sync)")
    
    # 1. Selection Controls
    col1, col2 = st.columns([1, 2])
    with col1:
        indicator = st.selectbox(
            "Select Macro Indicator", 
            ["USD/INR", "India VIX", "Gold Futures", "Nifty P/E Ratio", "India 10Y G-Sec"]
        )
    
    # 2. Timeframe Setup
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365*20) 
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    # 3. Data Fetching
    with st.spinner(f"Fetching data for {indicator}..."):
        nifty_df = get_cached_nifty(start_str, end_str)
        
        indicator_df = pd.DataFrame()
        line_color = 'rgba(255, 165, 0, 1)' # Default Orange
        
        if indicator == "USD/INR":
            indicator_df = get_cached_macro("INR=X", start_str, end_str)
        elif indicator == "India VIX":
            indicator_df = get_cached_macro("^INDIAVIX", start_str, end_str)
            line_color = 'rgba(255, 0, 0, 1)'
        elif indicator == "Gold Futures":
            indicator_df = get_cached_macro("GC=F", start_str, end_str)
            line_color = 'rgba(255, 215, 0, 1)'
        elif indicator == "Nifty P/E Ratio":
            indicator_df = get_cached_pe(start_str, end_str)
            line_color = 'rgba(0, 255, 0, 1)'
        elif indicator == "India 10Y G-Sec":
            from data_fetcher import fetch_fred_data
            indicator_df = fetch_fred_data("INDIRLTLT01STM", start_str, end_str)
            line_color = 'rgba(128, 0, 128, 1)'

    # 4. Rendering
    create_dual_pane_chart(nifty_df, indicator_df, indicator, line_color)

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
