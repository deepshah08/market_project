import datetime
try:
    from nsepython import index_pe_pb_div
except ImportError as e:
    print(f"Import Error: {e}")
    index_pe_pb_div = None

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)
start_str = start_date.strftime("%d-%b-%Y")
end_str = end_date.strftime("%d-%b-%Y")

print(f"Fetching NIFTY 50 from {start_str} to {end_str}")
try:
    df = index_pe_pb_div("NIFTY 50", start_str, end_str)
    if df is not None:
        print(f"Success! Shape: {df.shape}")
        print(df.head())
    else:
        print("Returned None")
except Exception as e:
    print(f"Fetch Error: {e}")
