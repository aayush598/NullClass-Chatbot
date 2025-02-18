import requests
import os
from database import insert_chat

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def analyze_text_with_gemini(text):
    """Analyze sentiment and extract topic using Gemini API."""
    headers = {"Content-Type": "application/json"}
    prompt = (
        f"Analyze sentiment of this text and return only one word: 'positive', 'neutral', or 'negative'.\n"
        f"Extract topic from this text in a single word.\n"
        f"Return output in the format: <sentiment>\\n<topic>\n"
        f"Text: {text}"
    )
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    response = requests.post(GEMINI_URL, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        content_parts = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])

        if content_parts:
            analysis_result = content_parts[0].get("text", "").strip().split("\n")  # Correct splitting
            sentiment = analysis_result[0].strip() if len(analysis_result) > 0 else "neutral"
            topic = analysis_result[1].strip() if len(analysis_result) > 1 else "unknown"
        else:
            sentiment, topic = "neutral", "unknown"
    else:
        sentiment, topic = "neutral", "unknown"

    return sentiment, topic

def chat_with_gemini(user_input):
    """Get AI-generated response along with sentiment and topic analysis."""
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": user_input}]}]}

    response = requests.post(GEMINI_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        ai_response = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response available.")
    else:
        ai_response = "Error: Failed to get response from Gemini API."

    # Sentiment and topic analysis
    sentiment, topic = analyze_text_with_gemini(user_input)

    # Save chat to database
    insert_chat(user_input, ai_response, sentiment, topic)

    return ai_response, sentiment, topic
