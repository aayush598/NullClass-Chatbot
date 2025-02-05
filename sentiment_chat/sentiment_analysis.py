import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Function to check if VADER lexicon is available
def is_vader_available():
    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
        return True
    except LookupError:
        return False

# Download VADER lexicon only if not available
if not is_vader_available():
    nltk.download('vader_lexicon')

# Initialize sentiment analysis models
sia = SentimentIntensityAnalyzer()
sentiment_model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english", revision="af0f99b")


def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER (Lexicon-based)."""
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return "positive"
    elif score['compound'] <= -0.05:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment_bert(text):
    """Analyze sentiment using a Pre-trained Transformer (BERT-based)."""
    result = sentiment_model(text)[0]
    return result['label'].lower()  # Convert 'POSITIVE'/'NEGATIVE' to lowercase

def chatbot_response(text, model="vader"):
    """Generate chatbot responses based on sentiment analysis."""
    if model == "vader":
        sentiment = analyze_sentiment_vader(text)
    else:
        sentiment = analyze_sentiment_bert(text)

    return sentiment
