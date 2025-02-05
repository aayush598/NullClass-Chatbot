import streamlit as st
from sentiment_analysis import chatbot_response

# Set Streamlit Page Config
st.set_page_config(page_title="Sentiment Chatbot", page_icon="💬", layout="centered")

# Streamlit UI
st.title("💬 Sentiment Chatbot")
st.write("Enter your message below and the chatbot will analyze the sentiment.")

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
user_input = st.text_input("You:", key="input", placeholder="Type your message...")

if user_input:
    # Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get Chatbot Response
    response = chatbot_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display Chatbot Response
    with st.chat_message("assistant"):
        st.write(response)

# Add Clear Button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
