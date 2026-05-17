import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_fetcher import fetch_nifty_data, fetch_macro_data, fetch_nifty_pe_data
from news_scraper import get_latest_news
import datetime

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

def create_synced_subplot_chart(nifty_df, indicator_df, indicator_name, line_color):
    """Creates a high-precision two-pane synchronized Plotly chart."""
    if nifty_df.empty:
        st.warning("Primary data (Nifty 50) missing or could not be fetched.")
        return

    # Create subplots: Top for Nifty, Bottom for Indicator
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        row_heights=[0.65, 0.35],
        subplot_titles=("NIFTY 50", f"{indicator_name}")
    )

    # 1. Top Pane: Nifty Candlesticks
    fig.add_trace(
        go.Candlestick(
            x=nifty_df.index,
            open=nifty_df['Open'],
            high=nifty_df['High'],
            low=nifty_df['Low'],
            close=nifty_df['Close'],
            name='Nifty 50'
        ),
        row=1, col=1
    )

    # 2. Bottom Pane: Indicator Line
    if not indicator_df.empty:
        # Convert rgb(r, g, b) to rgba(r, g, b, 0.1) safely
        rgba_fill = line_color.replace('rgb', 'rgba').replace(')', ', 0.1)')
        fig.add_trace(
            go.Scatter(
                x=indicator_df.index, 
                y=indicator_df['value'], 
                name=indicator_name,
                line=dict(color=line_color, width=2),
                fill='tozeroy',
                fillcolor=rgba_fill
            ),
            row=2, col=1
        )
    else:
        st.warning(f"Indicator data ({indicator_name}) missing for this period.")

    # 3. Styling & Sync (High Detail Crosshairs)
    fig.update_layout(
        height=800,
        template='plotly_dark',
        showlegend=False,
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis_rangeslider_visible=False,
        hovermode='x unified',
        # Spike lines (Crosshairs) configuration
        xaxis=dict(
            showspikes=True,
            spikemode='across',
            spikesnap='cursor',
            spikethickness=1,
            spikecolor="#999999",
            spikedash="dash"
        )
    )
    
    # Sync spikelines across subplots
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor', showline=True, showgrid=True)
    fig.update_yaxes(fixedrange=False)

    st.plotly_chart(fig, use_container_width=True)

def render_macro_tab():
    st.header("Macro Correlation Hub (Synchronized Engine)")
    
    # 1. Selection Controls
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        indicator = st.selectbox(
            "Select Macro Indicator", 
            ["USD/INR", "India VIX", "Gold Futures", "Nifty P/E Ratio", "India 10Y G-Sec"]
        )
    with col2:
        timeframe = st.selectbox(
            "Select Timeframe",
            ["Max", "10Y", "5Y", "3Y", "1Y", "6M", "YTD"],
            index=0
        )
    
    # 2. Timeframe Setup
    end_date = datetime.date.today()
    if timeframe == "Max":
        start_date = end_date - datetime.timedelta(days=365*25)
    elif timeframe == "10Y":
        start_date = end_date - datetime.timedelta(days=365*10)
    elif timeframe == "5Y":
        start_date = end_date - datetime.timedelta(days=365*5)
    elif timeframe == "3Y":
        start_date = end_date - datetime.timedelta(days=365*3)
    elif timeframe == "1Y":
        start_date = end_date - datetime.timedelta(days=365)
    elif timeframe == "6M":
        start_date = end_date - datetime.timedelta(days=180)
    elif timeframe == "YTD":
        start_date = datetime.date(end_date.year, 1, 1)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    # 3. Data Fetching
    with st.spinner(f"Fetching data for {indicator}..."):
        nifty_df = get_cached_nifty(start_str, end_str)
        
        indicator_df = pd.DataFrame()
        line_color = 'rgb(255, 165, 0)' # Orange
        
        if indicator == "USD/INR":
            indicator_df = get_cached_macro("INR=X", start_str, end_str)
        elif indicator == "India VIX":
            indicator_df = get_cached_macro("^INDIAVIX", start_str, end_str)
            line_color = 'rgb(255, 0, 0)' # Red
        elif indicator == "Gold Futures":
            indicator_df = get_cached_macro("GC=F", start_str, end_str)
            line_color = 'rgb(255, 215, 0)' # Gold
        elif indicator == "Nifty P/E Ratio":
            indicator_df = get_cached_pe(start_str, end_str)
            line_color = 'rgb(0, 255, 255)' # Cyan
        elif indicator == "India 10Y G-Sec":
            from data_fetcher import fetch_fred_data
            indicator_df = fetch_fred_data("INDIRLTLT01STM", start_str, end_str)
            line_color = 'rgb(128, 0, 128)' # Purple

    # 4. Rendering
    create_synced_subplot_chart(nifty_df, indicator_df, indicator, line_color)

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
