from flask import Flask, request, jsonify
from chatbot import chat_with_gemini, process_image
from database import get_analytics

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    """Handle text-based chat queries with optional image."""
    user_input = request.form.get("message", "").strip()
    image = request.files.get("image")

    if not user_input and not image:
        return jsonify({"error": "Please enter a message or upload an image."}), 400

    if image:
        image_path = f"static/uploads/{image.filename}"
        image.save(image_path)
        ai_response = process_image(image_path, user_input)
        return jsonify({"response": ai_response})

    elif user_input:
        ai_response, sentiment = chat_with_gemini(user_input)
        return jsonify({"response": ai_response, "sentiment": sentiment})

    return jsonify({"error": "Please enter a message or upload an image."}), 400

@app.route("/analytics", methods=["GET"])
def analytics():
    """Fetch sentiment analytics."""
    sentiment_data = get_analytics()
    return jsonify(sentiment_data)

if __name__ == "__main__":
    app.run(debug=True)
