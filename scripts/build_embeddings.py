import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

INPUT_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/enhanced_vehicles.json"
INDEX_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/car_index.faiss"

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_car_text(car):
    return f"{car['brand']} {car['model']} {car['body_type']} {car['segment']}"


with open(INPUT_FILE, "r") as file:
    cars = json.load(file)

car_texts = [build_car_text(car) for car in cars]

vectors = model.encode(car_texts)

dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)

index.add(np.array(vectors))

faiss.write_index(index, INDEX_FILE)

print("Embeddings built and stored.")