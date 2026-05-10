import streamlit as st
import streamlit.components.v1 as components
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

@st.cache_data
def get_cached_pe(start_str, end_str):
    return fetch_nifty_pe_data(start_str, end_str)

def create_percentage_overlay_chart(primary_df, secondary_df, indicator_name, line_color):
    """Helper to create a single-pane chart with Percentage Scale overlay."""
    if primary_df.empty:
        st.warning("Primary data (Nifty 50) missing or could not be fetched.")
        return
        
    chart = StreamlitChart(width=1000, height=500)
    
    # 1. Set the price scale to percentage mode
    chart.price_scale(mode='percentage')
    
    # 2. Render Nifty as a Line chart
    nifty_line = chart.create_line(name='Nifty 50', color='rgba(0, 123, 255, 1)')
    
    # CRITICAL FIX: The charting library assumes nanosecond resolution.
    # If the input data uses microsecond or second resolution (common in Pandas 2.0+),
    # the library's internal conversion results in timestamps 1000x smaller,
    # causing the "Jan '70" bug. We force nanosecond resolution here.
    formatted_nifty = primary_df[['time', 'close']].copy()
    formatted_nifty['time'] = pd.to_datetime(formatted_nifty['time']).dt.tz_localize(None).dt.as_unit('ns')
    formatted_nifty = formatted_nifty.rename(columns={'close': 'Nifty 50'})
    nifty_line.set(formatted_nifty)
    
    # 3. Add the Indicator as an overlay line
    if not secondary_df.empty:
        line = chart.create_line(name=indicator_name, color=line_color)
        formatted_secondary = secondary_df[['time', 'value']].copy()
        formatted_secondary['time'] = pd.to_datetime(formatted_secondary['time']).dt.tz_localize(None).dt.as_unit('ns')
        formatted_secondary = formatted_secondary.rename(columns={'value': indicator_name})
        line.set(formatted_secondary)
    else:
        st.warning(f"Secondary data ({indicator_name}) missing for this period.")
        
    chart.load()

def render_macro_tab():
    st.header("Macro Correlation Hub (Weekly % Overlay)")
    
    end_date = datetime.date.today()
    # 20 Years of history
    start_date = end_date - datetime.timedelta(days=365*20) 
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    with st.spinner("Fetching weekly data..."):
        nifty_df = get_cached_nifty(start_str, end_str)
        # Debug: show the data structure
        st.write("Debug Nifty Data (first 5 rows):")
        st.write(nifty_df.head())
        st.write(f"Time column type: {type(nifty_df['time'].iloc[0])}")

    # Panel 1: Nifty vs USD/INR
    st.subheader("1. Nifty 50 vs USD/INR Exchange Rate (% Change)")
    with st.spinner("Loading USD/INR..."):
        usdinr_df = get_cached_macro("INR=X", start_str, end_str)
        create_percentage_overlay_chart(nifty_df, usdinr_df, "USD/INR", 'rgba(255, 165, 0, 1)')

    st.divider()

    # Panel 2: Nifty vs VIX
    st.subheader("2. Nifty 50 vs India VIX (% Change)")
    with st.spinner("Loading India VIX..."):
        vix_df = get_cached_macro("^INDIAVIX", start_str, end_str)
        create_percentage_overlay_chart(nifty_df, vix_df, "India VIX", 'rgba(255, 0, 0, 1)')

    st.divider()

    # Panel 3: Nifty vs Gold
    st.subheader("3. Nifty 50 vs Gold (Futures) (% Change)")
    with st.spinner("Loading Gold..."):
        gold_df = get_cached_macro("GC=F", start_str, end_str)
        create_percentage_overlay_chart(nifty_df, gold_df, "Gold", 'rgba(255, 215, 0, 1)')

    st.divider()
    
    # Panel 4: Nifty vs PE Ratio
    st.subheader("4. Nifty 50 vs Nifty P/E Ratio (% Change)")
    with st.spinner("Loading Nifty P/E..."):
        pe_df = get_cached_pe(start_str, end_str)
        create_percentage_overlay_chart(nifty_df, pe_df, "Nifty P/E", 'rgba(0, 255, 0, 1)')

    st.divider()

    # Panel 5: Nifty vs India 10Y G-Sec (Index Proxy)
    st.subheader("5. Nifty 50 vs India 10Y G-Sec Index (% Change)")
    with st.spinner("Loading 10Y Benchmark..."):
        # ^N10YGBM is the Nifty 10 yr Benchmark G-Sec Index
        yield_df = get_cached_macro("^N10YGBM", start_str, end_str)
        create_percentage_overlay_chart(nifty_df, yield_df, "10Y G-Sec Index", 'rgba(128, 0, 128, 1)')

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
