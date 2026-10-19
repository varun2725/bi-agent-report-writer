# Agent: Report Writer
# Author: Varun

import json

REQUIRED_KEYS = ["metrics", "trends", "anomalies"]


def validate_insights(insights: dict) -> None:
    """Stop early with a clear message if the Analyser's output is incomplete."""
    missing = [k for k in REQUIRED_KEYS if k not in insights]
    if missing:
        raise ValueError(f"Insights are missing required keys: {missing}")


def build_prompt(insights: dict) -> str:
    return f"""You are a business analyst writing a weekly report for
non-technical managers. Use plain English and avoid jargon.

Data insights:
{json.dumps(insights, indent=2)}

Write the report in Markdown with these sections:
## Executive Summary (2-3 sentences)
## Key Trends
## Anomalies and Possible Causes
## Recommendations (3 actionable bullets)

If there are no anomalies, say so clearly. Only use facts from the data above."""


def report_writer_agent(insights: dict, llm_call, output_path: str = "weekly_report.md") -> str:
    validate_insights(insights)
    report = llm_call(build_prompt(insights))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    return report