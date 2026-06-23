from flask import Blueprint, request, jsonify
from services.hybrid_recommender import hybrid_recommend
from services.query_parser import parse_query
from services.reference_resolver import resolve_reference
from services.reference_resolver import cars
api = Blueprint("api", __name__)


@api.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    query = data.get("query")

    parsed = parse_query(query, cars)
    parsed = resolve_reference(parsed)

    results = hybrid_recommend(
        query=query,
        budget=parsed.get("budget") or 5000000,
        seats=parsed.get("seats") or 5,
        body_type=parsed.get("body_type") or "SUV",
        priority=(parsed.get("intent") or ["family"])[0]
    )

    return jsonify({
        "parsed_query": parsed,
        "recommendations": results
    })