import os
from flask import Flask, request, jsonify
from openai import AzureOpenAI
from dotenv import load_dotenv
app = Flask(__name__)

# Read configuration from environment variables
load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_API_URL")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_OPENAI_MODEL_NAME = os.getenv("AZURE_MODEL_NAME")
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"

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
        model=AZURE_OPENAI_MODEL_NAME,
    )

    return jsonify({
        "model": response.model,
        "reply": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)