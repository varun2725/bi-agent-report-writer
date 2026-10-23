# TEMPORARY STAND-IN for Agent 1: Data Fetcher (owner: Balveer)
# Replace this file with Balveer's agent when it is ready.
import pandas as pd


def data_fetcher_agent(csv_path: str) -> dict:
    df = pd.read_csv(csv_path, parse_dates=["date"]).dropna()
    df = df[df["revenue"] > 0]
    daily = df.groupby("date")["revenue"].sum().sort_index()
    weekly = daily.resample("W").sum()
    return {
        "date_range": f"{daily.index.min().date()} to {daily.index.max().date()}",
        "weekly_totals": [{"week": str(i.date()), "revenue": round(float(v), 2)} for i, v in weekly.items()],
        "daily_totals": [{"date": str(i.date()), "revenue": round(float(v), 2)} for i, v in daily.items()],
        "by_category": {k: round(float(v), 2) for k, v in df.groupby("category")["revenue"].sum().items()},
        "raw_stats": {"mean": round(float(daily.mean()), 2), "std": round(float(daily.std()), 2)},
    }