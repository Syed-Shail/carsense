import json
import ollama
from json_repair import repair_json


def normalize_parsed(parsed, cars):
    # Fix fake budgets
    if parsed.get("budget") == -1:
        parsed["budget"] = None

    comparison = parsed.get("comparison")

    # If LLM accidentally puts model name into comparison
    if comparison and parsed.get("reference_model") is None:
        comparison_lower = comparison.lower()

        for car in cars:
            if comparison_lower in car["model"].lower():
                parsed["reference_model"] = car["model"]
                parsed["comparison"] = None
                break

    return parsed


def parse_query(query, cars):
    prompt = f"""
Extract vehicle constraints.

Return ONLY valid JSON.

Use ONLY these keys:
- budget
- body_type
- seats
- fuel_type
- reference_model
- comparison
- intent

Do NOT create extra keys.
Do NOT explain.
Do NOT use markdown.
Do NOT guess missing values.

Schema:
{{
    "budget": null,
    "body_type": null,
    "seats": null,
    "fuel_type": null,
    "reference_model": null,
    "comparison": null,
    "intent": []
}}

Rules:
- Convert lakh values into integers
- intent must be short tags only like:
  ["family"], ["offroad"], ["performance"]
- missing values must be null

Query:
{query}
"""

    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": """
You are a JSON extraction engine.

Rules:
- Output ONLY valid JSON.
- Never explain.
- Never add comments.
- Never add markdown.
- Never add text before or after JSON.
- Never infer extra information.
- Missing fields must be null.
- Use only the provided schema keys.
"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response["message"]["content"]

    print("RAW LLM OUTPUT:")
    print(output)

    # Extract only first JSON block
    lines = output.splitlines()
    clean_lines = []
    started = False

    for line in lines:
        if "{" in line:
            started = True

        if started:
            clean_lines.append(line)

        if "}" in line:
            break

    json_string = "\n".join(clean_lines)

    print("EXTRACTED JSON:")
    print(json_string)

    # Repair malformed JSON
    fixed_json = repair_json(json_string)

    print("FIXED JSON:")
    print(fixed_json)

    # Normalize into dict
    if isinstance(fixed_json, str):
        parsed = json.loads(fixed_json)
    else:
        parsed = fixed_json

    if isinstance(parsed, str):
        parsed = json.loads(parsed)

    # Apply post-processing normalization
    parsed = normalize_parsed(parsed, cars)

    print("FINAL PARSED:")
    print(parsed)

    return parsed