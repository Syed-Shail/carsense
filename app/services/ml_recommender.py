import json
import joblib


DATA_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/enhanced_vehicles.json"
MODEL_FILE ="/Users/shail/Desktop/Car Projecr/data/processed/ranker.pkl"


with open(DATA_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)


saved = joblib.load(MODEL_FILE)

model = saved["model"]
body_encoder = saved["body_encoder"]
priority_encoder = saved["priority_encoder"]


def recommend_ml(budget, seats, body_type, priority):
    results = []

    for car in cars:
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

        features = [
            budget,
            seats,
            body_encoder.transform([car["body_type"]])[0],
            priority_encoder.transform([priority])[0],
            min_price,
            car["ai"]["family_score"],
            car["ai"]["performance_score"],
            car["ai"]["city_score"],
            car["ai"]["luxury_score"],
            car["ai"]["offroad_score"],
            car["ai"]["safety_score"],
            car["ai"]["efficiency_score"]
        ]

        probability = model.predict_proba([features])[0][1]

        results.append({
            "brand": car["brand"],
            "model": car["model"],
            "score": probability,
            "price": min_price
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:5]


if __name__ == "__main__":
    recommendations = recommend_ml(
        budget=20000000,
        seats=5,
        body_type="Sedan",
        priority="performance"
    )

    for car in recommendations:
        print(car)