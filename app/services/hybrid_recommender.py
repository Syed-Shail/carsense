import re
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer



DATA_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/enhanced_vehicles.json"
INDEX_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/car_index.faiss"

model = SentenceTransformer("all-MiniLM-L6-v2")


with open(DATA_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)

index = faiss.read_index(INDEX_FILE)
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded")

print("Loading cars...")
with open(DATA_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)
print("Cars loaded")

print("Loading FAISS index...")
index = faiss.read_index(INDEX_FILE)
print("FAISS loaded")

def parse_query(query):
    constraints = {
        "budget": None,
        "seats": None,
        "body_type": None
    }

    budget_match = re.search(r'under\s+(\d+)', query.lower())
    if budget_match:
        constraints["budget"] = int(budget_match.group(1)) * 100000

    seats_match = re.search(r'(\d+)\s*seats?', query.lower())
    if seats_match:
        constraints["seats"] = int(seats_match.group(1))

    body_types = ["suv", "sedan", "hatchback", "muv"]
    for body in body_types:
        if body in query.lower():
            constraints["body_type"] = body.capitalize()

    return constraints


def semantic_candidates(query, top_k=50):
    query_vector = model.encode([query])

    distances, indices = index.search(
        np.array(query_vector),
        top_k
    )

    return [cars[i] for i in indices[0]]


def apply_filters(candidates, constraints):
    filtered = []

    for car in candidates:
        min_price = min(
            variant["pricing"]["ex_showroom"]
            for variant in car["variants"]
        )

        if constraints["budget"] and min_price > constraints["budget"]:
            continue

        if constraints["seats"] and car["seating_capacity"] < constraints["seats"]:
            continue

        if constraints["body_type"] and car["body_type"].lower() != constraints["body_type"].lower():
            continue

        filtered.append(car)

    return filtered


def rerank(cars_list, query):
    scored = []

    query_lower = query.lower()

    for car in cars_list:
        score = 0

        if "rugged" in query_lower or "offroad" in query_lower:
            score += car["ai"]["offroad_score"]

        if "family" in query_lower:
            score += car["ai"]["family_score"]

        if "performance" in query_lower or "sporty" in query_lower:
            score += car["ai"]["performance_score"]

        if "safe" in query_lower:
            score += car["ai"]["safety_score"]

        if "efficient" in query_lower or "mileage" in query_lower:
            score += car["ai"]["efficiency_score"]

        scored.append({
            "brand": car["brand"],
            "model": car["model"],
            "score": score,
            "price": min(
                variant["pricing"]["ex_showroom"]
                for variant in car["variants"]
            )
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:5]


def hybrid_recommend(query):
    print("Parsing query...")
    constraints = parse_query(query)

    print("Getting semantic candidates...")
    candidates = semantic_candidates(query)

    print("Applying filters...")
    filtered = apply_filters(candidates, constraints)

    print("Reranking...")
    ranked = rerank(filtered, query)

    return ranked


if __name__ == "__main__":
    query = "Need a rugged SUV less then 20 lakh with 7 seats"

    results = hybrid_recommend(query)

    for car in results:
        print(car)