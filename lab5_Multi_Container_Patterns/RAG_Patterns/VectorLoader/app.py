from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct
import json
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Initialize Qdrant client
qdrant_client = QdrantClient(url=os.environ.get("QDRANT_CLIENT_URL"))

# Creating a Collection
qdrant_client.create_collection(
    collection_name="margies_travel_embeddings",
    vectors_config=VectorParams(size=1536, distance=Distance.DOT)
)

# Load data from data.json
with open("data.json", "r") as json_file:
    data = json.load(json_file)

# Construct the points list (this will be used when upserting vector embeddings)
embedding_points = [
    PointStruct(
        id=index + 1,  # Use 1-based indexing for IDs
        vector=entry["vector"],  # Embedding vector
        payload={"text": entry["text"]}  # Use extracted text as payload
    )
    for index, entry in enumerate(data)
]

print("created the vector embeddings point collection \n")
print(embedding_points)

# Now lets upsert our vector embeddings into the recently created collection

operation_info = qdrant_client.upsert(
    collection_name="margies_travel_embeddings",
    wait=True,
    points=embedding_points
)

print("upserted vector embeddings with operation_info: \n")
print(operation_info)
