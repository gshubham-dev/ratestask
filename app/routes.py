from flask import request, jsonify, Blueprint
from app.data_services import price_service, validate_slug_service, validate_port_service
import datetime

# Define a Blueprint for routing
routes_bp = Blueprint("routes", __name__)

@routes_bp.route("/rates", methods=["GET"])
def fetch_rates():
    """
    Endpoint to fetch average prices based on date range, origin, and destination.

    Returns:
        Response: JSON response with average prices or error message.
    """
    required_args = ["date_from", "date_to", "origin", "destination"]

    # Check for missing required parameters
    missing_params = [param for param in required_args if not request.args.get(param)]
    if missing_params:
        return (
            jsonify({"error": f"Required parameter(s) missing: {', '.join(missing_params)}"}),
            400
        )

    # Extract parameters from query string
    date_from, date_to, origin, destination = (
        request.args.get(param) for param in required_args
    )

    # Validate date formats
    if not validate_date_format(date_from) or not validate_date_format(date_to):
        return (
            jsonify({"error": "Invalid date format. Please use YYYY-MM-DD format."}),
            400
        )

    # Validate origin parameter (port code or region slug)
    if len(origin) <= 5 and origin.isupper():
        if not validate_port_service.port_exists(origin):
            return jsonify({"error": f"Port {origin} does not exist."}), 400
    else:
        if not validate_slug_service.slug_exists(origin):
            return jsonify({"error": f"Region {origin} does not exist."}), 400

    # Validate destination parameter (port code or region slug)
    if len(destination) <= 5 and destination.isupper():
        if not validate_port_service.port_exists(destination):
            return jsonify({"error": f"Port {destination} does not exist."}), 400
    else:
        if not validate_slug_service.slug_exists(destination):
            return jsonify({"error": f"Region {destination} does not exist."}), 400

    # Calculate average prices
    average_prices = price_service.calculate_average_prices(date_from, date_to, origin, destination)

    return jsonify(average_prices)

def validate_date_format(date_str: str) -> bool:
    """
    Check if the date string is in YYYY-MM-DD format.
    """
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

