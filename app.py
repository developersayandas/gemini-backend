from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Message is required"}), 400

    payload = {
        "contents": [{"parts": [{"text": user_input}]}]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={API_KEY}",
        json=payload
    )

    if response.ok:
        gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"response": gemini_reply})
    else:
        return jsonify({"error": "Failed to get response"}), 500

if __name__ == "__main__":
    app.run(debug=True)