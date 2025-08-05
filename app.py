from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv

# Load .env file if exists (for local testing)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load your Gemini API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=api_key)

# Use the flash model (faster + more quota)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "No message received"}), 400

        response = model.generate_content(user_message)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
