import streamlit as st
import requests

def get_gemini_response(user_input, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": user_input}]}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error: No response from API")
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    st.title("Chatbot using Gemini API")
    st.write("Enter your message below and get a response from Gemini AI.")
    
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    user_input = st.text_area("You:")
    
    if st.button("Send"):
        if api_key and user_input:
            response = get_gemini_response(user_input, api_key)
            st.text_area("Chatbot Response:", value=response, height=150, disabled=True)
        else:
            st.warning("Please enter both API key and a message.")

if __name__ == "__main__":
    main()