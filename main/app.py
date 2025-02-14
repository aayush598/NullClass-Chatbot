from flask import Flask, request, jsonify
from chatbot import chat_with_gemini
from database import create_tables

app = Flask(__name__)

# Ensure DB is created
create_tables()

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "No input provided"}), 400

        user_input = data["message"]
        response, sentiment = chat_with_gemini(user_input)

        return jsonify({"response": response, "sentiment": sentiment})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
