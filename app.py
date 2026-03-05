import streamlit as st
import pandas as pd
import re
import os
import time
from datetime import datetime

import google.generativeai as genai

# Load API key from environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------------------------------------------------------
# Streamlit Page Config
# ---------------------------------------------------------
st.set_page_config(page_title="Log Intelligence Console", layout="wide")

# ---------------------------------------------------------
# Log Parsing Pattern
# ---------------------------------------------------------
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) - - \[(?P<timestamp>.*?)\] '
    r'"(?P<method>\S+) (?P<endpoint>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\d+) "-" "(?P<agent>[^"]+)"'
)

def parse_log_line(line):
    match = LOG_PATTERN.search(line)
    if not match:
        return None
    data = match.groupdict()
    try:
        data["timestamp"] = datetime.strptime(data["timestamp"], "%d/%b/%Y:%H:%M:%S -0600")
    except:
        return None
    return data

def parse_logs(uploaded_file):
    lines = uploaded_file.read().decode("utf-8").splitlines()
    parsed = [parse_log_line(line) for line in lines]
    parsed = [p for p in parsed if p]
    return pd.DataFrame(parsed)

# ---------------------------------------------------------
# AI Query (Gemini)
# ---------------------------------------------------------
def ai_query(prompt, df):
    if df.empty:
        return "No log data available for analysis."

    context = df.tail(50).to_string()

    full_prompt = f"""
You are an expert log analyst. Use the log data below to answer the question.

LOG DATA:
{context}

QUESTION:
{prompt}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(full_prompt)
    return response.text

# ---------------------------------------------------------
# Live Log Tailing
# ---------------------------------------------------------
LIVE_LOG_PATH = os.path.join("logs", "live_app.log")

def tail_live_log(path):
    if "log_pointer" not in st.session_state:
        st.session_state.log_pointer = 0

    if not os.path.exists(path):
        return []

    new_lines = []
    with open(path, "r", encoding="utf-8") as f:
        f.seek(st.session_state.log_pointer)
        for line in f:
            new_lines.append(line.strip())
        st.session_state.log_pointer = f.tell()

    return new_lines

def update_live_dataframe(df, new_lines):
    parsed = [parse_log_line(l) for l in new_lines]
    parsed = [p for p in parsed if p]
    if parsed:
        df = pd.concat([df, pd.DataFrame(parsed)], ignore_index=True)
    return df

# ---------------------------------------------------------
# UI Layout (Tabs)
# ---------------------------------------------------------
st.title("📊 Log Intelligence Console")

tab_upload, tab_live = st.tabs(["Upload Logs", "Live Log Stream"])

# ---------------------------------------------------------
# TAB 1: Upload Logs
# ---------------------------------------------------------
with tab_upload:
    uploaded_file = st.file_uploader("Upload log file", type=["log", "txt"])

    if uploaded_file:
        df = parse_logs(uploaded_file)
        st.success(f"Parsed {len(df)} log entries.")
        st.dataframe(df)

        st.subheader("Insights")
        col1, col2 = st.columns(2)

        with col1:
            st.write("Requests per endpoint")
            st.bar_chart(df["endpoint"].value_counts())

        with col2:
            st.write("Status code distribution")
            st.bar_chart(df["status"].value_counts())

        st.subheader("AI Summary")
        if st.button("Generate Summary"):
            summary = ai_query("Summarize the key patterns and anomalies.", df)
            st.write(summary)

        st.subheader("Ask Questions About Your Logs")
        user_q = st.text_input("Ask a question")
        if user_q:
            answer = ai_query(user_q, df)
            st.write(answer)

# ---------------------------------------------------------
# TAB 2: Live Log Stream
# ---------------------------------------------------------
from streamlit_autorefresh import st_autorefresh

with tab_live:
    st.header("Real-Time Log Stream")

    # Auto-refresh interval
    refresh_rate = st.slider("Refresh every (seconds)", 1, 10, 3, key="live_refresh_rate")

    # Initialize state
    if "live_df" not in st.session_state:
        st.session_state.live_df = pd.DataFrame()

    if "live_ai_summary" not in st.session_state:
        st.session_state.live_ai_summary = None

    if "live_ai_answer" not in st.session_state:
        st.session_state.live_ai_answer = None

    if "ai_action" not in st.session_state:
        st.session_state.ai_action = None

    if "ai_payload" not in st.session_state:
        st.session_state.ai_payload = None

    # Auto-refresh only when AI is not running
    if st.session_state.ai_action is None:
        st_autorefresh(interval=refresh_rate * 1000, key="live_autorefresh")

    # Read new log lines
    new_lines = tail_live_log(LIVE_LOG_PATH)
    st.session_state.live_df = update_live_dataframe(st.session_state.live_df, new_lines)
    df_live = st.session_state.live_df

    # Display logs
    st.subheader("Latest Logs")
    st.dataframe(df_live.tail(20))

    if not df_live.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.write("Requests per endpoint")
            st.bar_chart(df_live["endpoint"].value_counts())

        with col2:
            st.write("Status code distribution")
            st.bar_chart(df_live["status"].value_counts())

    # -----------------------------------------
    # SECTION BREAK
    # -----------------------------------------
    st.markdown("---")

    # -----------------------------------------
    # ASK AI ABOUT LIVE LOGS
    # -----------------------------------------
    st.subheader("Ask AI About Live Logs")
    st.caption("Using AI tools will temporarily pause live streaming. Refresh the page to resume streaming.")

    st.write("Quick Questions:")
    quick_col1, quick_col2 = st.columns(2)

    if quick_col1.button("Summarize last 200 calls", key="quick_200"):
        st.session_state.ai_action = "quick_200"
        st.session_state.ai_payload = df_live.tail(200)
        st.rerun()

    if quick_col1.button("Summarize last 15 minutes", key="quick_15m"):
        cutoff = datetime.now().timestamp() - (15 * 60)
        subset = df_live[df_live["timestamp"].apply(lambda t: t.timestamp()) >= cutoff]
        st.session_state.ai_action = "quick_15m"
        st.session_state.ai_payload = subset
        st.rerun()

    if quick_col2.button("Top endpoints (recent)", key="quick_top_endpoints"):
        st.session_state.ai_action = "top_endpoints"
        st.session_state.ai_payload = df_live
        st.rerun()

    if quick_col2.button("Detect anomalies", key="quick_anomalies"):
        st.session_state.ai_action = "detect_anomalies"
        st.session_state.ai_payload = df_live
        st.rerun()

    user_q_live = st.text_input("Ask a custom question about the live logs", key="live_question_input")

    if st.button("Ask", key="live_question_btn"):
        st.session_state.ai_action = "custom"
        st.session_state.ai_payload = (user_q_live, df_live)
        st.rerun()

    # -----------------------------------------
    # EXECUTE AI ACTION
    # -----------------------------------------
    if st.session_state.ai_action:
        st_autorefresh(interval=0)

        with st.spinner("Thinking…"):
            action = st.session_state.ai_action

            if action == "quick_200":
                st.session_state.live_ai_answer = ai_query("Summarize the last 200 calls.", st.session_state.ai_payload)

            elif action == "quick_15m":
                st.session_state.live_ai_answer = ai_query("Summarize the last 15 minutes of logs.", st.session_state.ai_payload)

            elif action == "top_endpoints":
                st.session_state.live_ai_answer = ai_query("Identify the top endpoints in the recent logs.", st.session_state.ai_payload)

            elif action == "detect_anomalies":
                st.session_state.live_ai_answer = ai_query("Detect anomalies in the recent logs.", st.session_state.ai_payload)

            elif action == "custom":
                question, df_payload = st.session_state.ai_payload
                st.session_state.live_ai_answer = ai_query(question, df_payload)

        st.session_state.ai_action = None
        st.session_state.ai_payload = None
        st.rerun()

    if st.session_state.live_ai_answer:
        st.success(st.session_state.live_ai_answer)

    # -----------------------------------------
    # SECTION BREAK
    # -----------------------------------------
    st.markdown("---")

    # -----------------------------------------
    # AI SUMMARY
    # -----------------------------------------
    st.subheader("AI Summary (Live Logs)")

    if st.button("Summarize Live Logs", key="live_summary_btn"):
        st.session_state.ai_action = "summary"
        st.session_state.ai_payload = df_live
        st.rerun()

    if st.session_state.ai_action == "summary":
        st_autorefresh(interval=0)

        with st.spinner("Analyzing logs…"):
            st.session_state.live_ai_summary = ai_query(
                "Summarize the latest traffic patterns and anomalies.",
                st.session_state.ai_payload
            )

        st.session_state.ai_action = None
        st.session_state.ai_payload = None
        st.rerun()

    if st.session_state.live_ai_summary:
        st.info(st.session_state.live_ai_summary)