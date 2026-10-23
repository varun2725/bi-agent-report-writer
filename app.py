# Streamlit dashboard for the BI Agent pipeline
# Author: Varun S
import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv
from agents.data_fetcher import data_fetcher_agent
from agents.insight_analyser import insight_analyser_agent
from agents.report_writer import report_writer_agent
from test_writer import real_llm, mock_llm

load_dotenv()
st.set_page_config(page_title="BI Agent", layout="wide")
st.title("Business Intelligence Agent")

uploaded = st.sidebar.file_uploader("Upload sales CSV (date, category, revenue)", type="csv")
use_live = st.sidebar.checkbox("Use Gemini (live)", value=True)
source = uploaded if uploaded else "sales.csv"

if st.button("Generate weekly report"):
    llm = real_llm if use_live else mock_llm
    with st.spinner("Agents are working..."):
        data = data_fetcher_agent(source)
        insights = insight_analyser_agent(data, llm)
        report = report_writer_agent(insights, llm)
    st.session_state.update(data=data, insights=insights, report=report)

if "report" in st.session_state:
    data = st.session_state["data"]
    insights = st.session_state["insights"]
    report = st.session_state["report"]
    m = insights["metrics"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Total revenue", f"{m['total_revenue']:,.0f}")
    c2.metric("Week over week", f"{m['wow_change'] * 100:.0f}%")
    c3.metric("Anomalies found", len(insights["anomalies"]))

    daily = pd.DataFrame(data["daily_totals"])
    daily["date"] = pd.to_datetime(daily["date"])
    chart = alt.Chart(daily).mark_line().encode(x="date:T", y="revenue:Q")

    anom = pd.DataFrame(insights["anomalies"])
    if not anom.empty:
        anom["date"] = pd.to_datetime(anom["date"])
        anom = anom.merge(daily, on="date")
        points = alt.Chart(anom).mark_point(size=120, color="red", filled=True).encode(
            x="date:T", y="revenue:Q", tooltip=["date:T", "issue"])
        chart = chart + points

    st.subheader("Daily revenue (anomalies in red)")
    st.altair_chart(chart)

    left, right = st.columns(2)
    left.subheader("Revenue by category")
    left.bar_chart(pd.Series(data["by_category"]))
    right.subheader("Weekly revenue")
    right.bar_chart(pd.DataFrame(data["weekly_totals"]).set_index("week"))

    st.subheader("Weekly report")
    st.markdown(report)
    st.download_button("Download report (.md)", report, file_name="weekly_report.md")