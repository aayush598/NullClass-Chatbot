import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

BACKEND_URL = "http://127.0.0.1:5000"

st.title("💬 AI Chatbot with Text & Image Processing")

# Unified Input Field
st.subheader("Chat or Upload an Image")
user_input = st.text_area("Enter your message (or leave blank if only uploading an image):")
uploaded_file = st.file_uploader("Optional: Upload an image for analysis", type=["jpg", "png", "jpeg"])

if st.button("Send"):
    # Prepare request payload
    data = {"message": user_input}
    files = {"image": uploaded_file} if uploaded_file is not None else None

    if uploaded_file:
        response = requests.post(f"{BACKEND_URL}/chat", files=files, data=data)
    else:
        response = requests.post(f"{BACKEND_URL}/chat", data=data)

    if response.status_code == 200:
        response_data = response.json()
        st.write("🤖 AI Response:", response_data.get("response"))
        if "sentiment" in response_data:
            st.write("📝 Sentiment:", response_data.get("sentiment"))
    else:
        st.write("⚠️ Error:", response.text)

# Display Analytics
st.subheader("📊 Chatbot Analytics")

if st.button("Show Analytics"):
    response = requests.get(f"{BACKEND_URL}/analytics")
    if response.status_code == 200:
        analytics_data = response.json()
        
        if analytics_data:
            df = pd.DataFrame(analytics_data)
            st.write("### Query Metrics")
            st.bar_chart(df[df["metric"].str.contains("total_queries")].set_index("metric"))
            
            st.write("### Sentiment Distribution")
            sentiment_df = df[df["metric"].str.contains("sentiment_")]
            st.bar_chart(sentiment_df.set_index("metric"))
            
            st.write("### Common Topics")
            topic_df = df[df["metric"].str.contains("topic_")]
            st.bar_chart(topic_df.set_index("metric"))
            
        else:
            st.write("📉 No analytics data available yet.")
    else:
        st.write("⚠️ Error fetching analytics data.")