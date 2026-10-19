import json
import sys
from dotenv import load_dotenv
from agents.report_writer import report_writer_agent

load_dotenv()  # loads GEMINI_API_KEY from your .env file


def mock_llm(prompt: str) -> str:
    return "## Executive Summary\n(mock report: the file-saving works)"


def real_llm(prompt: str) -> str:
    from google import genai
    client = genai.Client()  # reads GEMINI_API_KEY automatically
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )
    return response.text


if __name__ == "__main__":
    with open("sample_insights.json", encoding="utf-8") as f:
        insights = json.load(f)

    live = len(sys.argv) > 1 and sys.argv[1] == "live"
    llm = real_llm if live else mock_llm
    print(report_writer_agent(insights, llm))