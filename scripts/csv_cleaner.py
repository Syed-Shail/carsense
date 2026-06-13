import csv
import json
from collections import defaultdict


INPUT_FILE = "data/raw/vehicles.csv"
OUTPUT_FILE = "data/processed/cleaned_vehicles.json"


def parse_bool(value):
    if str(value).strip().lower() == "true":
        return True
    return False


def parse_number(value):
    try:
        if "." in str(value):
            return float(value)
        return int(value)
    except:
        return value


cars = {}

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        model_key = f"{row['Identification Brand']}_{row['Identification Model']}"

        variant_data = {
            "variant_name": row["Identification Variant"],
            "year": parse_number(row["Identification Year"]),

            "pricing": {
                "ex_showroom": parse_number(row["Pricing Delhi Ex Showroom Price"]),
                "on_road": parse_number(row["Pricing Delhi On Road Price"]),
                "resale_value": row["Pricing Delhi Resale Value"],
                "insurance_cost": parse_number(row["Pricing Delhi Insurance Cost"])
            },

            "engine": {
                "bhp": parse_number(row["Engine Bhp"]),
                "torque": parse_number(row["Engine Torque"]),
                "transmission": row["Engine Transmission"],
                "gears": parse_number(row["Engine Gears"]),
                "zero_to_hundred": parse_number(row["Engine 0 100 Sec"]),
                "top_speed": parse_number(row["Engine Top Speed"])
            },

            "efficiency": {
                "arai": parse_number(row["Efficiency Mileage Arai"]),
                "city": parse_number(row["Efficiency Mileage City"]),
                "highway": parse_number(row["Efficiency Mileage Highway"]),
                "tank_capacity": parse_number(row["Efficiency Tank Capacity"])
            },

            "ev": {
                "is_ev": parse_bool(row["Ev Data Is Ev"]),
                "battery_kwh": parse_number(row["Ev Data Battery Kwh"]),
                "range_km": parse_number(row["Ev Data Range Km"]),
                "charging_ac_hours": parse_number(row["Ev Data Charging Ac Hours"]),
                "charging_dc_min": parse_number(row["Ev Data Charging Dc Min"])
            },

            "safety": {
                "ncap": parse_number(row["Safety Ncap Stars"]),
                "airbags": parse_number(row["Safety Airbags"]),
                "abs": parse_bool(row["Safety Abs"]),
                "esp": parse_bool(row["Safety Esp"]),
                "hill_hold": parse_bool(row["Safety Hill Hold"]),
                "isofix": parse_bool(row["Safety Isofix"]),
                "tpms": parse_bool(row["Safety Tpms"]),
                "adas_level_2": parse_bool(row["Safety Adas Level 2"])
            },

            "features": {
                "sunroof": parse_bool(row["Features Sunroof"]),
                "ventilated_seats": parse_bool(row["Features Ventilated Seats"]),
                "cruise_control": parse_bool(row["Features Cruise Control"]),
                "keyless_entry": parse_bool(row["Features Keyless Entry"]),
                "touchscreen": parse_number(row["Features Touchscreen Inch"]),
                "camera_360": parse_bool(row["Features 360 Camera"]),
                "wireless_charging": parse_bool(row["Features Wireless Charging"]),
                "connected_tech": parse_bool(row["Features Connected Tech"]),
                "led_lights": parse_bool(row["Features Led Lights"]),
                "alloy_wheels": parse_bool(row["Features Alloy Wheels"])
            },

            "warranty": {
                "years": parse_number(row["Warranty Years"]),
                "km": parse_number(row["Warranty Km"]),
                "service_km": parse_number(row["Warranty Service Km"])
            }
        }

        if model_key not in cars:
            cars[model_key] = {
                "brand": row["Identification Brand"],
                "model": row["Identification Model"],
                "body_type": row["Identification Body Type"],
                "seating_capacity": parse_number(row["Identification Seating Capacity"]),
                "segment": row["Identification Segment"],

                "base_specs": {
                    "engine_cc": parse_number(row["Engine Cc"]),
                    "cylinders": parse_number(row["Engine Cylinders"]),
                    "fuel_type": row["Efficiency Fuel Type"],
                    "turbo": parse_bool(row["Engine Turbo"]),
                    "drive": row["Engine Drive"]
                },

                "dimensions": {
                    "length": parse_number(row["Dimensions Length"]),
                    "width": parse_number(row["Dimensions Width"]),
                    "height": parse_number(row["Dimensions Height"]),
                    "wheelbase": parse_number(row["Dimensions Wheelbase"]),
                    "ground_clearance": parse_number(row["Dimensions Ground Clearance"]),
                    "weight": parse_number(row["Dimensions Weight Kg"]),
                    "boot_space": parse_number(row["Dimensions Boot Liters"]),
                    "turning_radius": parse_number(row["Dimensions Turning Radius"])
                },

                "variants": []
            }

        cars[model_key]["variants"].append(variant_data)


with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
    json.dump(list(cars.values()), output, indent=4)

print("Cleaning complete.")