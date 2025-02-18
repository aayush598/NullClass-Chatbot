from flask import Flask, request, jsonify
from chatbot import chat_with_gemini
from database import get_analytics

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    """Handle text-based chat queries."""
    user_input = request.form.get("message", "").strip()
    
    if user_input:
        ai_response, sentiment, topic = chat_with_gemini(user_input)
        return jsonify({"response": ai_response, "sentiment": sentiment, "topic": topic})
    
    return jsonify({"error": "Please enter a message."}), 400

@app.route("/analytics", methods=["GET"])
def analytics():
    """Fetch chatbot analytics."""
    return jsonify(get_analytics())

if __name__ == "__main__":
    app.run(debug=True)
