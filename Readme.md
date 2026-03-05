📊 Log Intelligence Console
Real‑Time Apache Log Monitoring, Insights & AI‑Powered Analysis
Powered by Google Gemini AI

📁 Table of Contents
• 	Overview
• 	Features
• 	Dependencies
• 	Installation
• 	Project Structure
• 	Credits

<a name="overview"></a>
<details><summary><strong>📘 Overview</strong></summary>
Log Intelligence Console is a real‑time Apache log analysis dashboard built with Streamlit.
It combines live log streaming, interactive charts, and Google Gemini AI to deliver instant insights into traffic patterns, anomalies, and operational behavior.
Designed for developers, SREs, DevOps engineers, and analysts who need fast, intelligent visibility into their systems.
</details>

<a name="features"></a>
<details><summary><strong>✨ Features</strong></summary>
🔍 Upload & Analyze Logs
• 	Upload  or  Apache log files
• 	Automatic parsing using regex
• 	Interactive DataFrame preview
• 	Charts for:
• 	Requests per endpoint
• 	Status code distribution
• 	AI‑powered:
• 	Summary of key patterns
• 	Natural‑language Q&A

📡 Live Log Stream
• 	Reads from  in real time
• 	Auto-refreshing table of latest log entries
• 	Live charts:
• 	Endpoint frequency
• 	Status code distribution
• 	Smooth updates without flicker
• 	Session‑safe state management

🤖 AI‑Powered Insights (Google Gemini)
Powered by Google Gemini 2.5 Flash
AI capabilities include:
• 	Summaries of latest traffic
• 	Anomaly detection
• 	Endpoint analysis
• 	Time‑window summaries
• 	Custom natural‑language questions
Quick‑action AI buttons:
• 	Summarize last 200 calls
• 	Summarize last 15 minutes
• 	Detect anomalies
• 	Identify top endpoints
AI execution temporarily pauses live streaming to ensure stable output.

🧠 Intelligent Refresh Control
• 	Live streaming auto-refreshes every 1–10 seconds
• 	AI actions run in a non-refresh frame
• 	Prevents:
• 	Interrupted AI calls
• 	Blinking output
• 	Lost responses
• 	Ensures:
• 	Smooth charts
• 	Stable AI results
</details>

<a name="dependencies"></a>
<details><summary><strong>🛠️ Dependencies</strong></summary>
Python Packages

System Requirements
• 	Python 3.10+
• 	Internet access for Google Gemini API
• 	A valid Google AI Studio API key
</details>

<a name="installation"></a>
<details><summary><strong>🔧 Installation & Setup</strong></summary>
1. Clone the repository

2. Install dependencies

3. Set your Google Gemini API key
Windows PowerShell:

Restart your terminal after setting the key.
4. Start the app

</details>

<a name="project-structure"></a>
<details><summary><strong>📁 Project Structure</strong></summary>

</details>

<a name="credits"></a>
<details><summary><strong>🤝 Credits</strong></summary>
• 	Google Gemini 2.5 Flash — AI summaries, anomaly detection, and natural‑language insights
• 	Streamlit — UI framework
• 	Pandas — Data processing
</details>