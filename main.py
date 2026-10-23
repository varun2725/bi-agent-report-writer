# Orchestrator: Data Fetcher -> Insight Analyser -> Report Writer
# Author: Varun S
import json
import sys
from dotenv import load_dotenv
from agents.report_writer import report_writer_agent
from test_writer import real_llm, mock_llm

load_dotenv()


def run(csv_path: str, llm) -> str:
    try:
        from agents.data_fetcher import data_fetcher_agent
        from agents.insight_analyser import insight_analyser_agent
    except ImportError:
        print("Teammate agents not found, using sample_insights.json")
        with open("sample_insights.json", encoding="utf-8") as f:
            insights = json.load(f)
    else:
        data = data_fetcher_agent(csv_path)
        insights = insight_analyser_agent(data, llm)
    return report_writer_agent(insights, llm)


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "sales.csv"
    llm = real_llm if "live" in sys.argv else mock_llm
    print(run(csv_path, llm))