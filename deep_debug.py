import yfinance as yf
import pandas as pd
import datetime
import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'src'))
from data_fetcher import fetch_nifty_data, fetch_macro_data

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365*20)
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

print("--- Nifty Fetch ---")
nifty_df = fetch_nifty_data(start_str, end_str, interval="1wk")
print(nifty_df[['time', 'close']].head(10))

print("\n--- USD/INR Fetch ---")
usdinr_df = fetch_macro_data("INR=X", start_str, end_str, interval="1wk")
print(usdinr_df.head(10))
