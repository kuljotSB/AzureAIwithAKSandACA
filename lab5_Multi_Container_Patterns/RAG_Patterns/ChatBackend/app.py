import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
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
EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME", "text-embedding-ada-002")
QDRANT_CLIENT_URL = os.environ.get("QDRANT_CLIENT_URL", "http://localhost:6333")

openai_client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

# Initialize Qdrant client
qdrant_client = QdrantClient(url=os.environ.get("QDRANT_CLIENT_URL"))

def generate_vector_embeddings(text):
    # Will be primarily used to generate vector embeddings for the incoming user query
    embeddings = openai_client.embeddings.create(
        input = text,
        model=EMBEDDING_MODEL_NAME
    )

    print("Generated vector embeddings for the text: \n")
    print(embeddings.data[0].embedding)

    return embeddings.data[0].embedding

@app.route("/chat", methods=["POST"])
def chat():
    # Accepting a JSON payload with a "message" field from the user
    data = request.get_json()
    user_message = data.get("message", "")
    
    print("extracted user payload")

    # Generating Vector Embeddings for the User Query
    user_embeddings = generate_vector_embeddings(user_message)

    # Throwing a request to QDrantDB to retrieve the top-matched content along with the vector embeddings
    search_result = qdrant_client.query_points(
        collection_name = "margies_travel_embeddings",
        query = user_embeddings,
        with_vectors=True,
        with_payload=True,
        limit=2
    ).points

    # Retrieving the top text content that can be used to answer the user query
    supporting_text_content = search_result[0].payload.get("text")
    print("retrieved supporting text content:{}".format(supporting_text_content))
    
    # Sending a request to the GPT engine with the supporting text content
    gpt_response = openai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful RAG assistant."},
            {"role": "user", "content": f"""answer the user query using the provided supporting knowledge \n 
                                         user query: {user_message} \n
                                         supporting_text: {supporting_text_content}"""}
        ],
        max_tokens=8192,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=AZURE_OPENAI_MODEL_NAME,
    )

    return jsonify({
        "model": gpt_response.model,
        "reply": gpt_response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)