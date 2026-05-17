import pandas as pd
import datetime

t = pd.to_datetime('2007-09-17')
ns = t.value
s = ns // 10**9
print(f"Nanoseconds: {ns}")
print(f"Seconds: {s}")

df = pd.DataFrame({'time': [t]})
df_int = df['time'].astype('int64')
print(f"DataFrame astype(int64): {df_int.iloc[0]}")
