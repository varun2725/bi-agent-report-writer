# Report Writer Agent (Agent 3)

Part of the Business Intelligence Agent project (Data Fetcher → Insight Analyser → Report Writer).

Takes the Analyser's insights (JSON) and writes a plain-English weekly report as `weekly_report.md` using Gemini.

## Run
pip install -r requirements.txt
python test_writer.py          # mock LLM, no key needed
python test_writer.py live     # real Gemini (needs GEMINI_API_KEY in .env)

## Input format
{"metrics": {...}, "trends": [...], "anomalies": [...]}

Author: Varun S