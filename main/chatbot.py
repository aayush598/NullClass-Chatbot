
import requests
import os
from transformers import pipeline
import base64
from database import insert_chat, update_analytics

# Load Sentiment Analysis Model (DistilBERT)
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def analyze_sentiment(text):
    """Analyze sentiment of user input."""
    result = sentiment_model(text)[0]
    return result['label'].lower()

def extract_topic(text):
    """Extract topic from user input."""
    keywords = ["order", "pricing", "support", "refund", "product", "service"]
    for keyword in keywords:
        if keyword in text.lower():
            return keyword
    return "other"

def chat_with_gemini(user_input):
    """Get AI-generated response from Gemini API."""
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": user_input}]}]}
    response = requests.post(GEMINI_URL, json=data, headers=headers)
    ai_response = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't generate a response.")
    sentiment = analyze_sentiment(user_input)
    topic = extract_topic(user_input)
    insert_chat(user_input, ai_response, sentiment, topic)
    return ai_response, sentiment