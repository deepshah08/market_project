import streamlit as st
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_polymarket_events
from news_scraper import get_latest_news
import datetime

def get_app_title():
    return "NSE Market Assistant"

def render_macro_tab():
    st.header("Macro & Polymarket Correlation Hub")
    from lightweight_charts.widgets import StreamlitChart
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Controls")
        indicator = st.selectbox("Select Overlay Indicator", ["None", "Crude Oil (CL=F)", "US 10Y Bond (^TNX)", "Polymarket Events"])
        if indicator == "Polymarket Events":
            events = fetch_polymarket_events()
            if events:
                event_titles = [e.get('title', 'Unknown') for e in events]
                selected_event = st.selectbox("Select Event", event_titles)
                st.info("Polymarket overlay requires historical API. Showing current events only.")
            else:
                st.warning("Could not fetch Polymarket events.")

    with col2:
        st.subheader("Nifty 50 vs Overlay")
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=365) # Show 1 year
        
        nifty_df = fetch_nifty_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        
        if not nifty_df.empty:
            chart = StreamlitChart(width=800, height=500)
            chart.set(nifty_df) # Main series is Candlestick by default
            
            if indicator not in ["None", "Polymarket Events"]:
                ticker = "CL=F" if "Crude" in indicator else "^TNX"
                macro_df = fetch_macro_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                if not macro_df.empty:
                    # Create a line series with a secondary price scale
                    line = chart.create_line(name=indicator, color='rgba(255, 165, 0, 0.8)', price_scale_id='right')
                    line.set(macro_df)
                else:
                    st.warning(f"Could not fetch overlay data for {indicator}.")
            
            chart.load()
        else:
            st.warning("Could not fetch Nifty 50 data.")

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
