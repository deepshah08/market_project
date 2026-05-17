import pandas as pd
import datetime

def library_logic(df):
    df = df.copy()
    # Library assumes this will be in nanoseconds
    df['time'] = pd.to_datetime(df['time'])
    # Force to nanoseconds to fix the bug
    df['time'] = df['time'].dt.as_unit('ns')
    # Now the library's internal code will work:
    ts = df['time'].astype('int64') // 10 ** 9
    return ts.iloc[0]

# Simulate yfinance-like data (which might be in [s] or [us])
df = pd.DataFrame({
    'time': pd.to_datetime(['2007-09-17'], utc=True)
})
print(f"Original unit: {df['time'].dtype}")

res = library_logic(df)
print(f"Final Timestamp: {res}")
print(f"Date from TS: {datetime.datetime.fromtimestamp(res)}")
