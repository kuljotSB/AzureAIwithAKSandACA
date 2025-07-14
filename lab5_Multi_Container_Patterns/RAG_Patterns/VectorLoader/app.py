from flask import Flask, request, jsonify
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables
load_dotenv()
QDRANT_URL = os.environ.get("QDRANT_CLIENT_URL")
COLLECTION_NAME = "margies_travel_embeddings"

# Init Flask app
app = Flask(__name__)

# Init Qdrant client
qdrant_client = QdrantClient(url=QDRANT_URL)

# Initial vector loading (runs once on startup)
def preload_vectors():
    print("Waiting for Qdrant to be ready...")
    time.sleep(20)  # optional, if Qdrant might be slow to start
    print("Initializing collection...")

    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.DOT)
        )
        print(f"Collection '{COLLECTION_NAME}' created.")

        # Load vectors from file
        with open("data.json", "r") as f:
            data = json.load(f)

        points = [
            PointStruct(
                id=i + 1,
                vector=entry["vector"],
                payload={"text": entry["text"]}
            ) for i, entry in enumerate(data)
        ]

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=points
        )
        print(f"Upserted {len(points)} vectors.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")


# Route to add a single vector
@app.route("/add-vector", methods=["POST"])
def add_vector():
    try:
        data = request.get_json()
        vector = data["vector"]
        text = data.get("text", "")
        vector_id = data.get("id")

        if not vector_id:
            vector_id = int(time.time() * 1000)  # use timestamp as unique ID

        point = PointStruct(
            id=vector_id,
            vector=vector,
            payload={"text": text}
        )

        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=[point]
        )

        return jsonify({"status": "success", "id": vector_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Run the preload and then start Flask server
if __name__ == "__main__":
    preload_vectors()
    app.run(host="0.0.0.0", port=5173)
