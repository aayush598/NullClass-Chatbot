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
    return result['label'].lower()  # Convert "POSITIVE" -> "positive"

def chat_with_gemini(user_input):
    """Get AI-generated response from Gemini API."""
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": user_input}]}]}

    response = requests.post(GEMINI_URL, json=data, headers=headers)
    if response.status_code == 200:
        ai_response = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't generate a response.")
    else:
        ai_response = "Error: Failed to get response from Gemini API."

    # Sentiment analysis
    sentiment = analyze_sentiment(user_input)

    # Save chat to database
    insert_chat(user_input, ai_response, sentiment)
    update_analytics(sentiment)

    return ai_response, sentiment

def process_image(image_path, user_prompt):
    """Process image with user-provided prompt using Gemini API."""
    headers = {"Content-Type": "application/json"}

    # Convert image to Base64
    with open(image_path, "rb") as img_file:
        encoded_image = base64.b64encode(img_file.read()).decode("utf-8")

    # Correct JSON structure
    data = {
        "contents": [{
            "parts": [
                {"inline_data": {"mime_type": "image/jpeg", "data": encoded_image}},  # Fixing image format
                {"text": user_prompt}  # User-provided prompt
            ]
        }]
    }

    response = requests.post(GEMINI_URL, json=data, headers=headers)

    if response.status_code == 200:
        ai_response = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No description available.")
    else:
        print("⚠️ Gemini API Error:", response.text)  # Debugging error
        ai_response = "Error: Failed to process the image."

    return ai_response
