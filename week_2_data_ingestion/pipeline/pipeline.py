import sys
import pandas as pd


print("Hello pipeline")
print("arguments", sys.argv)
month = sys.argv[1]
df = pd.DataFrame({"day": [1, 2], "number_of_passengers": [3, 4]})
df['month'] = month
print(df)

df.to_parquet(f"output_{month}.parquet")

print(f"month: {month}")
