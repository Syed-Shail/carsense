import json


DATA_FILE = "/Users/shail/Desktop/Car Projecr/data/processed/enhanced_vehicles.json"


def load_cars():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def recommend(budget, body_type=None, seats=None, priority=None):
    cars = load_cars()
    results = []

    for car in cars:
        min_price = min(
            variant["pricing"]["ex_showroom"]
            for variant in car["variants"]
        )

        if min_price > budget:
            continue

        if body_type and car["body_type"].lower() != body_type.lower():
            continue

        if seats and car["seating_capacity"] < seats:
            continue

        score = 0

        if priority == "family":
            score += car["ai"]["family_score"]

        elif priority == "performance":
            score += car["ai"]["performance_score"]

        elif priority == "city":
            score += car["ai"]["city_score"]

        elif priority == "luxury":
            score += car["ai"]["luxury_score"]

        elif priority == "offroad":
            score += car["ai"]["offroad_score"]

        elif priority == "safety":
            score += car["ai"]["safety_score"]

        elif priority == "efficiency":
            score += car["ai"]["efficiency_score"]

        results.append({
            "brand": car["brand"],
            "model": car["model"],
            "starting_price": min_price,
            "score": score,
            "variants": len(car["variants"])
        })

    results.sort(
        key=lambda x: (x["score"], -x["starting_price"]),
        reverse=True
    )

    return results[:5]


if __name__ == "__main__":
    recommendations = recommend(
        budget = 10000000,
        seats = 2,
        priority= "safety"
    )

    for car in recommendations:
        print(car)