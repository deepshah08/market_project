import streamlit as st
import plotly.graph_objects as go
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_polymarket_events
from news_scraper import get_latest_news
import datetime

def get_app_title():
    return "NSE Market Assistant"

def render_macro_tab():
    st.header("Macro & Polymarket Correlation Hub")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Nifty 50")
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=180)
        nifty_df = fetch_nifty_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        
        if not nifty_df.empty:
            fig_nifty = go.Figure(data=[go.Scatter(x=nifty_df.index, y=nifty_df['Close'], name='Nifty 50')])
            fig_nifty.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300)
            st.plotly_chart(fig_nifty, use_container_width=True)
        else:
            st.warning("Could not fetch Nifty data.")

    with col2:
        st.subheader("Secondary Indicator")
        indicator = st.selectbox("Select Indicator", ["Crude Oil (CL=F)", "US 10Y Bond (^TNX)", "Polymarket Events"])
        
        if indicator == "Polymarket Events":
            events = fetch_polymarket_events()
            if events:
                event_titles = [e.get('title', 'Unknown') for e in events]
                selected_event = st.selectbox("Select Event", event_titles)
                st.info("Polymarket probability charts require historical data APIs which are complex. Showing current active events for now.")
                st.write(f"Tracking: {selected_event}")
            else:
                st.warning("Could not fetch Polymarket events.")
        else:
            ticker = "CL=F" if "Crude" in indicator else "^TNX"
            macro_df = fetch_macro_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            if not macro_df.empty:
                fig_macro = go.Figure(data=[go.Scatter(x=macro_df.index, y=macro_df['Close'], name=indicator, line=dict(color='orange'))])
                fig_macro.update_layout(margin=dict(l=0, r=0, t=30, b=0), height=300)
                st.plotly_chart(fig_macro, use_container_width=True)
            else:
                st.warning(f"Could not fetch data for {indicator}.")

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
