import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from openai import AzureOpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Read configuration from environment variables
AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_API_URL")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_API_KEY")
AZURE_OPENAI_MODEL_NAME = os.environ.get("AZURE_MODEL_NAME")
AZURE_OPENAI_API_VERSION = os.environ.get("AZURE_API_VERSION", "2024-12-01-preview")

client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        max_tokens=8192,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=AZURE_OPENAI_MODEL_NAME,
    )

    return jsonify({
        "model": response.model,
        "reply": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)