import json


DATA_FILE = "data/processed/enhanced_vehicles.json"


with open(DATA_FILE, "r", encoding="utf-8") as file:
    cars = json.load(file)


def resolve_reference(parsed):
    reference_model = parsed.get("reference_model")

    if not reference_model:
        return parsed

    reference_car = None

    for car in cars:
        if reference_model.lower() in car["model"].lower():
            reference_car = car
            break

    if not reference_car:
        return parsed

    if parsed.get("body_type") is None:
        parsed["body_type"] = reference_car["body_type"]

    if parsed.get("fuel_type") is None:
        parsed["fuel_type"] = reference_car.get("fuel_type")

    if parsed.get("seats") is None:
        parsed["seats"] = reference_car["seating_capacity"]

    return parsed