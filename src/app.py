import streamlit as st

def get_app_title():
    return "NSE Market Assistant"

def render_macro_tab():
    st.header("Macro Correlation Hub")
    st.write("Historical market correlations will appear here.")

def render_news_tab():
    st.header("Geopolitical & Economic News")
    st.write("AI-summarized news feed.")

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
