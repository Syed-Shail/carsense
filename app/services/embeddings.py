import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/enhanced_vehicles.json"
INDEX_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/car_index.faiss"

model = SentenceTransformer("all-MiniLM-L6-v2")


with open(DATA_FILE, "r") as file:
    cars = json.load(file)

index = faiss.read_index(INDEX_FILE)


def semantic_search(query, top_k=5):
    query_vector = model.encode([query])

    distances, indices = index.search(
        np.array(query_vector),
        top_k
    )

    return [cars[i] for i in indices[0]]

if __name__ == "__main__":
    query = "offroading 6 seater suv"

    results = semantic_search(query)

    for car in results:
        print(car["brand"], car["model"])