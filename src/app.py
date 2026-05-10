import streamlit as st
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_nifty_pe_data
from news_scraper import get_latest_news
import datetime
from lightweight_charts.widgets import StreamlitChart

def get_app_title():
    return "NSE Market Assistant"

def create_overlay_chart(primary_df, secondary_df, indicator_name, line_color):
    """Helper to create a standard StreamlitChart overlay."""
    if primary_df.empty:
        st.warning("Primary data missing.")
        return
        
    chart = StreamlitChart(width=1000, height=400)
    chart.set(primary_df)
    
    if not secondary_df.empty:
        line = chart.create_line(name=indicator_name, color=line_color, price_scale_id='right')
        # lightweight-charts expects the value column to match the line name
        formatted_secondary = secondary_df.rename(columns={'value': indicator_name})
        line.set(formatted_secondary)
    else:
        st.warning(f"Secondary data ({indicator_name}) missing.")
        
    chart.load()

def render_macro_tab():
    st.header("Macro Correlation Hub (V4)")
    
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365) # 1 Year
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    with st.spinner("Fetching market and macro data..."):
        # Fetch base Nifty 50 data once
        nifty_df = fetch_nifty_data(start_str, end_str)

    # Panel 1: Nifty vs USD/INR
    st.subheader("1. Nifty 50 vs USD/INR Exchange Rate")
    with st.spinner("Loading USD/INR..."):
        usdinr_df = fetch_macro_data("INR=X", start_str, end_str)
        create_overlay_chart(nifty_df, usdinr_df, "USD/INR", 'rgba(255, 165, 0, 0.8)')

    st.divider()

    # Panel 2: Nifty vs VIX
    st.subheader("2. Nifty 50 vs India VIX")
    with st.spinner("Loading India VIX..."):
        vix_df = fetch_macro_data("^INDIAVIX", start_str, end_str)
        create_overlay_chart(nifty_df, vix_df, "India VIX", 'rgba(255, 0, 0, 0.8)')

    st.divider()

    # Panel 3: Nifty vs Gold
    st.subheader("3. Nifty 50 vs Gold (Futures)")
    with st.spinner("Loading Gold..."):
        gold_df = fetch_macro_data("GC=F", start_str, end_str)
        create_overlay_chart(nifty_df, gold_df, "Gold", 'rgba(255, 215, 0, 0.8)')

    st.divider()

    # Panel 4: Nifty vs PE Ratio
    st.subheader("4. Nifty 50 vs P/E Ratio")
    with st.spinner("Loading Nifty P/E Ratio..."):
        pe_df = fetch_nifty_pe_data(start_str, end_str)
        create_overlay_chart(nifty_df, pe_df, "Nifty P/E", 'rgba(0, 0, 255, 0.8)')


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
