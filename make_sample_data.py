import numpy as np
import pandas as pd

np.random.seed(42)
dates = pd.date_range("2026-07-20", "2026-10-18")
cats = {"Electronics": 900, "Clothing": 500, "Groceries": 400, "Home": 300}

rows = []
for d in dates:
    for c, base in cats.items():
        rows.append({"date": d.date(), "category": c,
                     "revenue": round(base * np.random.uniform(0.85, 1.15), 2)})
df = pd.DataFrame(rows)

# Planted anomalies so we can check the Analyser finds them
df.loc[df["date"] == pd.Timestamp("2026-09-15").date(), "revenue"] *= 0.4   # drop
df.loc[df["date"] == pd.Timestamp("2026-10-05").date(), "revenue"] *= 2.2   # spike

df.to_csv("sales.csv", index=False)
print("sales.csv created:", len(df), "rows")