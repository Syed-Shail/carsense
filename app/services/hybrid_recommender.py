import json
import faiss
import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


DATA_FILE = "data/processed/enhanced_vehicles.json"
INDEX_FILE = "data/processed/car_index.faiss"
MODEL_FILE = "data/processed/ranker.pkl"


print("Loading model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
print("Embedding model loaded")


with open(DATA_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)

index = faiss.read_index(INDEX_FILE)

saved = joblib.load(MODEL_FILE)

ranker = saved["model"]
body_encoder = saved["body_encoder"]
priority_encoder = saved["priority_encoder"]


def semantic_candidates(query, top_k=50):
    query_vector = embedding_model.encode([query])

    distances, indices = index.search(
        np.array(query_vector),
        top_k
    )

    return [cars[i] for i in indices[0]]


def apply_filters(candidates, budget, seats, body_type):
    filtered = []

    for car in candidates:
        min_price = min(
            variant["pricing"]["ex_showroom"]
            for variant in car["variants"]
        )

        if min_price > budget:
            continue

        if car["seating_capacity"] < seats:
            continue

        if car["body_type"].lower() != body_type.lower():
            continue

        filtered.append(car)

    return filtered


def ml_rerank(filtered_cars, budget, seats, priority):
    ranked = []

    for car in filtered_cars:
        min_price = min(
            variant["pricing"]["ex_showroom"]
            for variant in car["variants"]
        )

        features = pd.DataFrame([{
            "budget": budget,
            "seats": seats,
            "body_type": body_encoder.transform([car["body_type"]])[0],
            "priority": priority_encoder.transform([priority])[0],
            "car_price": min_price,
            "family_score": car["ai"]["family_score"],
            "performance_score": car["ai"]["performance_score"],
            "city_score": car["ai"]["city_score"],
            "luxury_score": car["ai"]["luxury_score"],
            "offroad_score": car["ai"]["offroad_score"],
            "safety_score": car["ai"]["safety_score"],
            "efficiency_score": car["ai"]["efficiency_score"]
        }])

        probability = ranker.predict_proba(features)[0][1]

        ranked.append({
            "brand": car["brand"],
            "model": car["model"],
            "score": probability,
            "price": min_price
        })

    ranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:5]


def hybrid_recommend(query, budget, seats, body_type, priority):
    print("Semantic retrieval...")
    candidates = semantic_candidates(query)

    print("Applying filters...")
    filtered = apply_filters(
        candidates,
        budget,
        seats,
        body_type
    )

    print("ML reranking...")
    ranked = ml_rerank(
        filtered,
        budget,
        seats,
        priority
    )

    return ranked


if __name__ == "__main__":
    results = hybrid_recommend(
        query="Need a rugged family SUV for long trips",
        budget=10000000,
        seats=5,
        body_type="SUV",
        priority="luxury"
    )

    for car in results:
        print(car)