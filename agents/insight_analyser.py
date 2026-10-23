# TEMPORARY STAND-IN for Agent 2: Insight Analyser (owner: Elava)
# Replace this file with Elava's agent when it is ready.


def insight_analyser_agent(data: dict, llm_call=None) -> dict:
    weekly = data["weekly_totals"]
    wow = (weekly[-1]["revenue"] - weekly[-2]["revenue"]) / weekly[-2]["revenue"]
    top = max(data["by_category"], key=data["by_category"].get)
    mean, std = data["raw_stats"]["mean"], data["raw_stats"]["std"]

    anomalies = []
    for d in data["daily_totals"]:
        z = (d["revenue"] - mean) / std if std else 0
        if abs(z) > 2.5:
            kind = "spike" if z > 0 else "drop"
            pct = abs(round((d["revenue"] / mean - 1) * 100))
            anomalies.append({
                "date": d["date"],
                "issue": f"Revenue {kind} of {pct}% compared with the daily average",
                "possible_cause": "Not determined yet",
            })

    return {
        "date_range": data["date_range"],
        "metrics": {"total_revenue": round(sum(w["revenue"] for w in weekly), 2),
                    "wow_change": round(wow, 3)},
        "trends": [
            f"Revenue {'up' if wow >= 0 else 'down'} {abs(wow) * 100:.0f}% versus the previous week",
            f"{top} is the top category with {data['by_category'][top]:,.0f} in sales",
        ],
        "anomalies": anomalies,
    }