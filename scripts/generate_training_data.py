import json
import random
import csv


INPUT_FILE = "data/processed/enhanced_vehicles.json"
OUTPUT_FILE = "data/processed/training_data.csv"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)


priorities = [
    "family",
    "performance",
    "city",
    "luxury",
    "offroad",
    "safety",
    "efficiency"
]


training_rows = []


for _ in range(5000):
    user_budget = random.randint(400000, 5000000)
    user_seats = random.choice([4, 5, 6, 7])
    user_priority = random.choice(priorities)

    car = random.choice(cars)

    min_price = min(
        variant["pricing"]["ex_showroom"]
        for variant in car["variants"]
    )

    feature_map = {
        "family": car["ai"]["family_score"],
        "performance": car["ai"]["performance_score"],
        "city": car["ai"]["city_score"],
        "luxury": car["ai"]["luxury_score"],
        "offroad": car["ai"]["offroad_score"],
        "safety": car["ai"]["safety_score"],
        "efficiency": car["ai"]["efficiency_score"]
    }

    relevant_score = feature_map[user_priority]

    chosen = 0

    if (
        min_price <= user_budget
        and car["seating_capacity"] >= user_seats
        and relevant_score >= 7
    ):
        chosen = 1

    training_rows.append({
        "budget": user_budget,
        "seats": user_seats,
        "body_type": car["body_type"],
        "priority": user_priority,
        "car_price": min_price,
        "family_score": car["ai"]["family_score"],
        "performance_score": car["ai"]["performance_score"],
        "city_score": car["ai"]["city_score"],
        "luxury_score": car["ai"]["luxury_score"],
        "offroad_score": car["ai"]["offroad_score"],
        "safety_score": car["ai"]["safety_score"],
        "efficiency_score": car["ai"]["efficiency_score"],
        "chosen": chosen
    })


fieldnames = training_rows[0].keys()

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(training_rows)


print("Training data generated.")