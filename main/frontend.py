import streamlit as st
import requests
import sqlite3
import pandas as pd

API_URL = "http://127.0.0.1:5000/chat"

st.set_page_config(page_title="AI Chatbot", layout="wide")

st.title("💬 AI Chatbot with Sentiment Analysis")

# Sidebar for analytics
st.sidebar.header("📊 Chatbot Analytics")

# Chat interface
user_input = st.text_input("You: ")

if user_input:
    response = requests.post(API_URL, json={"message": user_input})
    
    # Debugging: Print Response
    print(response.text)  # Show raw response in the terminal

    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        st.write("Raw Response:", response.text)
    else:
        chatbot_response = response_data.get("response", "Error in chatbot response")
        sentiment = response_data.get("sentiment", "neutral")
        
        # Display chatbot response
        st.write(f"🤖 AI: {chatbot_response}")
        st.write(f"🧠 Sentiment: {sentiment}")


# Display analytics
conn = sqlite3.connect("chatbot.db")
analytics = pd.read_sql_query("SELECT * FROM analytics WHERE id = 1", conn)
conn.close()

if not analytics.empty:
    st.sidebar.metric(label="Total Queries", value=analytics["query_count"].values[0])
    st.sidebar.metric(label="Positive Sentiments", value=analytics["positive_count"].values[0])
    st.sidebar.metric(label="Negative Sentiments", value=analytics["negative_count"].values[0])
    st.sidebar.metric(label="Neutral Sentiments", value=analytics["neutral_count"].values[0])

# Display chat history
st.sidebar.subheader("Chat History")
conn = sqlite3.connect("chatbot.db")
chat_history = pd.read_sql_query("SELECT * FROM chats ORDER BY timestamp DESC LIMIT 10", conn)
conn.close()

for _, row in chat_history.iterrows():
    st.sidebar.write(f"🗨️ {row['user_input']}")
    st.sidebar.write(f"🤖 {row['sentiment']}")
    st.sidebar.write("---")
