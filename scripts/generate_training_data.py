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


for _ in range(10000):
    user_budget = random.randint(400000, 5000000)
    user_seats = random.choice([4, 5, 6, 7])
    user_priority = random.choice(priorities)

    car = random.choice(cars)

    min_price = min(
        variant["pricing"]["ex_showroom"]
        for variant in car["variants"]
    )

    price_fit = max(0, 1 - (min_price / user_budget))

    seat_fit = 1 if car["seating_capacity"] >= user_seats else 0

    scores = car["ai"]

    final_score = 0


    if user_priority == "family":
        final_score = (
            0.35 * scores["family_score"] +
            0.30 * scores["safety_score"] +
            0.20 * seat_fit * 10 +
            0.15 * price_fit * 10
        )

    elif user_priority == "performance":
        final_score = (
            0.60 * scores["performance_score"] +
            0.20 * scores["safety_score"] +
            0.20 * price_fit * 10
        )

    elif user_priority == "city":
        final_score = (
            0.50 * scores["city_score"] +
            0.30 * scores["efficiency_score"] +
            0.20 * price_fit * 10
        )

    elif user_priority == "luxury":
        final_score = (
            0.60 * scores["luxury_score"] +
            0.20 * scores["performance_score"] +
            0.20 * scores["safety_score"]
        )

    elif user_priority == "offroad":
        final_score = (
            0.50 * scores["offroad_score"] +
            0.30 * scores["performance_score"] +
            0.20 * scores["safety_score"]
        )

    elif user_priority == "safety":
        final_score = (
            0.70 * scores["safety_score"] +
            0.20 * scores["family_score"] +
            0.10 * price_fit * 10
        )

    elif user_priority == "efficiency":
        final_score = (
            0.60 * scores["efficiency_score"] +
            0.30 * scores["city_score"] +
            0.10 * price_fit * 10
        )


    chosen = 1 if final_score >= 6.5 else 0


    training_rows.append({
        "budget": user_budget,
        "seats": user_seats,
        "body_type": car["body_type"],
        "priority": user_priority,
        "car_price": min_price,
        "family_score": scores["family_score"],
        "performance_score": scores["performance_score"],
        "city_score": scores["city_score"],
        "luxury_score": scores["luxury_score"],
        "offroad_score": scores["offroad_score"],
        "safety_score": scores["safety_score"],
        "efficiency_score": scores["efficiency_score"],
        "chosen": chosen
    })


fieldnames = training_rows[0].keys()

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(training_rows)


print("Improved training data generated.")