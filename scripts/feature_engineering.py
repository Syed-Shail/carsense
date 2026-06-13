import json


INPUT_FILE = "data/processed/cleaned_vehicles.json"
OUTPUT_FILE = "data/processed/enhanced_vehicles.json"


def get_price_bucket(price):
    if price <= 500000:
        return "budget"
    elif price <= 1000000:
        return "mid_range"
    elif price <= 2000000:
        return "premium"
    return "luxury"


def calculate_family_score(car):
    score = 0

    if car["seating_capacity"] >= 5:
        score += 3

    for variant in car["variants"]:
        if variant["safety"]["airbags"] >= 4:
            score += 2
        if variant["features"]["camera_360"]:
            score += 1
        if variant["features"]["connected_tech"]:
            score += 1

    return min(score, 10)


def calculate_performance_score(car):
    score = 0

    for variant in car["variants"]:
        bhp = variant["engine"]["bhp"]
        top_speed = variant["engine"]["top_speed"]

        if bhp >= 100:
            score += 4
        elif bhp >= 70:
            score += 2

        if top_speed >= 180:
            score += 4
        elif top_speed >= 150:
            score += 2

    return min(score, 10)


def calculate_city_score(car):
    score = 0

    for variant in car["variants"]:
        mileage = variant["efficiency"]["city"]

        if mileage >= 18:
            score += 4

    if car["dimensions"]["length"] <= 4000:
        score += 3

    if car["dimensions"]["turning_radius"] <= 5:
        score += 3

    return min(score, 10)


def calculate_luxury_score(car):
    score = 0

    for variant in car["variants"]:
        features = variant["features"]

        if features["sunroof"]:
            score += 2
        if features["ventilated_seats"]:
            score += 2
        if features["wireless_charging"]:
            score += 2
        if features["connected_tech"]:
            score += 2
        if features["camera_360"]:
            score += 2

    return min(score, 10)


def calculate_offroad_score(car):
    score = 0

    if car["dimensions"]["ground_clearance"] >= 180:
        score += 4

    if car["base_specs"]["drive"] in ["AWD", "4WD"]:
        score += 4

    if car["body_type"] == "SUV":
        score += 2

    return min(score, 10)


def calculate_safety_score(car):
    score = 0

    for variant in car["variants"]:
        safety = variant["safety"]

        if safety["ncap"] >= 4:
            score += 4
        if safety["airbags"] >= 6:
            score += 3
        if safety["abs"]:
            score += 1
        if safety["esp"]:
            score += 1
        if safety["adas_level_2"]:
            score += 1

    return min(score, 10)


def calculate_efficiency_score(car):
    score = 0

    for variant in car["variants"]:
        arai = variant["efficiency"]["arai"]

        if arai >= 20:
            score += 5
        elif arai >= 15:
            score += 3

    return min(score, 10)


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)


for car in cars:
    min_price = min(
        variant["pricing"]["ex_showroom"]
        for variant in car["variants"]
    )

    car["ai"] = {
        "price_bucket": get_price_bucket(min_price),
        "family_score": calculate_family_score(car),
        "performance_score": calculate_performance_score(car),
        "city_score": calculate_city_score(car),
        "luxury_score": calculate_luxury_score(car),
        "offroad_score": calculate_offroad_score(car),
        "safety_score": calculate_safety_score(car),
        "efficiency_score": calculate_efficiency_score(car)
    }


with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(cars, file, indent=4)

print("Feature engineering complete.")