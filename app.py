from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    if not GEMINI_API_KEY:
        return jsonify({'error': 'API key not set'}), 500

    # Gemini API request setup
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{"parts": [{"text": user_input}]}]
    }
    params = {
        "key": GEMINI_API_KEY
    }

    response = requests.post(url, headers=headers, params=params, json=payload)

    if response.status_code == 200:
        data = response.json()
        try:
            reply = data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'reply': reply})
        except (IndexError, KeyError):
            return jsonify({'error': 'Invalid response structure'}), 500
    else:
        return jsonify({'error': 'API call failed', 'details': response.text}), 500

@app.route('/')
def home():
    return "Gemini AI backend is running."

if __name__ == '__main__':
    app.run(debug=True)
