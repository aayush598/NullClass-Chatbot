import streamlit as st
import pandas as pd
import plotly.express as px
import random
import datetime

# Sample Data (Replace with real MongoDB data)
data = [
    {"user_id": "U1", "query": "How to reset?", "timestamp": "2025-02-07", "category": "Troubleshooting", "satisfaction_rating": 4},
    {"user_id": "U2", "query": "Battery issue?", "timestamp": "2025-02-07", "category": "Battery", "satisfaction_rating": 5},
    {"user_id": "U3", "query": "Device not working", "timestamp": "2025-02-06", "category": "Troubleshooting", "satisfaction_rating": 3},
    {"user_id": "U4", "query": "Warranty info?", "timestamp": "2025-02-06", "category": "General Info", "satisfaction_rating": 4},
    {"user_id": "U5", "query": "WiFi connection issue", "timestamp": "2025-02-05", "category": "Connectivity", "satisfaction_rating": 2},
]

df = pd.DataFrame(data)
df["timestamp"] = pd.to_datetime(df["timestamp"])  # Convert timestamp to datetime

# ---- Streamlit UI ----
st.set_page_config(page_title="Chatbot Analytics", layout="wide")

st.title("🤖 Chatbot Analytics Dashboard")
st.markdown("### Key Metrics")

# Metrics Display
col1, col2, col3 = st.columns(3)
col1.metric("📊 Total Queries", len(df))
col2.metric("🔥 Most Common Topic", df["category"].mode()[0])
col3.metric("⭐ Avg. Satisfaction", round(df["satisfaction_rating"].mean(), 1))

# ---- Charts ----
st.markdown("### 📈 Query Trends Over Time")
trend_data = df.groupby(df["timestamp"].dt.date).size().reset_index(name="queries")
fig_trend = px.line(trend_data, x="timestamp", y="queries", markers=True, title="Chatbot Usage Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("### 🏆 Most Common Topics")
topic_data = df["category"].value_counts().reset_index()
topic_data.columns = ["Category", "Count"]
fig_topics = px.bar(topic_data, x="Category", y="Count", title="Most Asked Topics", text="Count")
st.plotly_chart(fig_topics, use_container_width=True)

st.markdown("### 🎭 User Satisfaction Ratings")
rating_data = df["satisfaction_rating"].value_counts().reset_index()
rating_data.columns = ["Rating", "Count"]
fig_rating = px.pie(rating_data, names="Rating", values="Count", title="User Satisfaction Distribution")
st.plotly_chart(fig_rating, use_container_width=True)

# ---- Future Enhancements ----
st.markdown("#### 🚀 Future Enhancements")
st.write("- Real-time updates with MongoDB")
st.write("- NLP analysis for sentiment insights")
st.write("- User engagement heatmaps")
