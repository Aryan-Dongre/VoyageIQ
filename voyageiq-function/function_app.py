import json
import logging
import os
from datetime import date

import azure.functions as func
import requests

from models.airport_model import search_airports



app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


# HOTEL SEARCH

@app.route(route="hotels", methods=["GET", "POST"],
           auth_level=func.AuthLevel.ANONYMOUS)
def hotels(req: func.HttpRequest) -> func.HttpResponse:
    try:
        payload = (
            req.get_json()
            if req.method == "POST"
            else dict(req.params)
        )
    except ValueError:
        return _json_response(
            {"error": "Request body must be valid JSON."},
            400
        )

    validation_error = _validate_payload(payload)

    if validation_error:
        return _json_response(
            {"error": validation_error},
            400
        )

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        logging.error("SERPAPI_API_KEY is not configured")

        return _json_response(
            {"error": "Hotel search is not configured."},
            500
        )
    # Prepare parameters for the SERPAPI request
    params = {
        "engine": "google_hotels",
        "q": payload["destination"].strip(),
        "gl": "in",
        "currency": "INR",
        "check_in_date": payload["check_in_date"],
        "check_out_date": payload["check_out_date"],
        "rooms": payload["rooms"],
        "adults": payload["adults"],
        "api_key": api_key,
    }

    try:
        response = requests.get(
            "https://serpapi.com/search.json",  # The URL for the SERPAPI hotel search endpoint
            params=params,
            timeout=30
        )

        response.raise_for_status()

        hotels = [
            _normalize_hotel(item)
            for item in response.json().get("properties", [])
        ]

    except requests.RequestException:
        logging.exception("SERPAPI hotel request failed")

        return _json_response(
            {"error": "Hotel provider is unavailable."},
            502
        )

    except (TypeError, ValueError):
        logging.exception(
            "SERPAPI returned an invalid response"
        )

        return _json_response(
            {"error": "Hotel provider returned invalid data."},
            502
        )

    return _json_response(
        {
            "destination": params["q"],
            "hotels": hotels
        }
    )


def _validate_payload(payload: dict) -> str | None:
    required = (
        "destination",
        "check_in_date",
        "check_out_date",
        "adults",
        "rooms"
    )

    missing = [
        field
        for field in required
        if field not in payload or payload[field] in (None, "")
    ]

    if missing:
        return (
            f"Missing required fields: {', '.join(missing)}."
        )

    if (
        not isinstance(payload["destination"], str)
        or len(payload["destination"].strip()) < 2
    ):
        return "destination must contain at least 2 characters."

    try:
        check_in = date.fromisoformat(
            str(payload["check_in_date"])
        )

        check_out = date.fromisoformat(
            str(payload["check_out_date"])
        )

        adults = int(payload["adults"])
        rooms = int(payload["rooms"])

    except (TypeError, ValueError):
        return (
            "Dates must use YYYY-MM-DD and "
            "adults/rooms must be integers."
        )

    if check_in < date.today():
        return "check_in_date cannot be in the past."

    if check_out <= check_in:
        return "check_out_date must be after check_in_date."

    if not 1 <= adults <= 10:
        return "adults must be between 1 and 10."

    if not 1 <= rooms <= 5:
        return "rooms must be between 1 and 5."

    return None


def _normalize_hotel(hotel: dict) -> dict:
    images = hotel.get("images") or []
    nearby_places = hotel.get("nearby_places") or []
    rate = hotel.get("rate_per_night") or {}

    return {
        "hotel_name": hotel.get("name"),
        "location": (
            hotel.get("address")
            or (
                nearby_places[0].get("name")
                if nearby_places
                else None
            )
        ),
        "amenities": ", ".join(
            hotel.get("amenities") or []
        ),
        "star_rating": hotel.get("overall_rating"),
        "review_score": hotel.get("overall_rating"),
        "review_count": hotel.get("reviews"),
        "room_type": hotel.get("type"),
        "price_per_night": rate.get("extracted_lowest"),
        "currency": "INR",
        "hotel_image": (
            images[0].get("thumbnail")
            if images
            else None
        ),
        "api_source": "SERPAPI",
    }



# AIRPORT SEARCH

@app.route(
    route="airports",
    methods=["GET"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def airports(req: func.HttpRequest) -> func.HttpResponse:
    keyword = req.params.get("q", "").strip()

    if not keyword:
        return func.HttpResponse(
            json.dumps([]),
            status_code=200,
            mimetype="application/json"
        )

    try:
        airports = search_airports(keyword)

        result = [
            {
                "airport_code": airport["airport_code"],
                "city_name": airport["city_name"],
                "airport_name": airport["airport_name"]
            }
            for airport in airports
        ]

        return func.HttpResponse(
            json.dumps(result),
            status_code=200,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Airport search failed")

        return func.HttpResponse(
            json.dumps({
                "error": "Airport search failed"
            }),
            status_code=500,
            mimetype="application/json"
        )


# COMMON RESPONSE HELPER

def _json_response(
    body: dict,
    status_code: int = 200
) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps(body),
        status_code=status_code,
        mimetype="application/json"
    )


# Flight Part
# FLIGHT SEARCH

@app.route(
    route="flights",
    methods=["GET", "POST"],
    auth_level=func.AuthLevel.ANONYMOUS
)
def flights(req: func.HttpRequest) -> func.HttpResponse:

    try:
        payload = (
            req.get_json()
            if req.method == "POST"
            else dict(req.params)
        )

    except ValueError:
        return _json_response(
            {"error": "Request body must be valid JSON."},
            400
        )

    validation_error = _validate_flight_payload(payload)

    if validation_error:
        return _json_response(
            {"error": validation_error},
            400
        )

    api_key = os.getenv("SERPAPI_API_KEY")

    if not api_key:
        logging.error("SERPAPI_API_KEY is not configured")

        return _json_response(
            {"error": "Flight search is not configured."},
            500
        )

    cabin_map = {
        "economy": 1,
        "premium_economy": 2,
        "business": 3,
        "first": 4
    }

    params = {
        "engine": "google_flights",
        "departure_id": payload["origin"].strip(),
        "arrival_id": payload["destination"].strip(),
        "outbound_date": payload["departure_date"],
        "adults": int(payload["adults"]),
        "currency": "INR",
        "gl": "in",
        "travel_class": cabin_map.get(
            payload["travel_class"],
            1
        ),
        "api_key": api_key
    }

    if payload["trip_type"] == "round_trip":

        params["type"] = 1
        params["return_date"] = payload["return_date"]

    else:

        params["type"] = 2

    try:

        response = requests.get(
            "https://serpapi.com/search.json",
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        flights_data = [
            _normalize_flight(flight, data)
            for flight in data.get("best_flights", [])
        ]

    except requests.RequestException:

        logging.exception(
            "SERPAPI flight request failed"
        )

        return _json_response(
            {"error": "Flight provider is unavailable."},
            502
        )

    except (TypeError, ValueError, KeyError):

        logging.exception(
            "SERPAPI returned an invalid flight response"
        )

        return _json_response(
            {"error": "Flight provider returned invalid data."},
            502
        )

    return _json_response(
        {
            "origin": params["departure_id"],
            "destination": params["arrival_id"],
            "flights": flights_data
        }
    )

# Validation function for flight payload
def _validate_flight_payload(payload:dict)-> str| None:

    required = (
        "origin",
        "destination",
        "departure_date",
        "adults",
        "travel_class",
        "trip_type"
    )

    missing = [
        field
        for field in required
        if field not in payload or payload[field] in (None, "")
    ]

    if missing:
        return (
            f"Missing required fields: {', '.join(missing)}."
        )

    if not isinstance(payload["origin"], str):
        return "origin must be valid airport code."

    if not isinstance(payload["destination"], str):
        return "destination must be a valid airport code."

    try:

        departure_date = date.fromisoformat(
            str(payload["departure_date"])
        )

        adults = int(payload["adults"])

    except (TypeError, ValueError):

        return (
            "departure_date must use YYYY-MM-DD "
            "and adults must be an integer."
        )

    if departure_date < date.today():
        return "departure_date cannot be in the past."

    if not 1 <= adults <= 10:
        return "adults must be between 1 and 10."

    valid_classes = {
        "economy",
        "premium_economy",
        "business",
        "first"
    }

    if payload["travel_class"] not in valid_classes:
        return "Invalid travel_class."

    valid_trip_types = {
        "one_way",
        "round_trip"
    }

    if payload["trip_type"] not in valid_trip_types:
        return "Invalid trip_type."

    if payload["trip_type"] == "round_trip":

        if not payload.get("return_date"):
            return "return_date is required for round_trip."

        try:

            return_date = date.fromisoformat(
                str(payload["return_date"])
            )

        except (TypeError, ValueError):

            return "return_date must use YYYY-MM-DD."

        if return_date <= departure_date:
            return "return_date must be after departure_date."

    return None

def _normalize_flight(
    flight: dict,
    data: dict
) -> dict:

    segments = flight.get("flights") or []

    if not segments:
        return {}

    first_flight = segments[0]
    last_flight = segments[-1]

    departure_airport = (
        first_flight.get("departure_airport") or {}
    )

    arrival_airport = (
        last_flight.get("arrival_airport") or {}
    )

    search_parameters = (
        data.get("search_parameters") or {}
    )

    return {
        "airline": first_flight.get("airline"),

        "flight_number": first_flight.get(
            "flight_number"
        ),

        "departure_airport": departure_airport.get(
            "name"
        ),

        "departure_city": departure_airport.get(
            "id"
        ),

        "arrival_airport": arrival_airport.get(
            "name"
        ),

        "arrival_city": arrival_airport.get(
            "id"
        ),

        "stopover_airports": None,

        "departure_time": departure_airport.get(
            "time"
        ),

        "arrival_time": arrival_airport.get(
            "time"
        ),

        "duration_minutes": flight.get(
            "total_duration"
        ),

        "cabin_class": first_flight.get(
            "travel_class"
        ),

        "price": flight.get(
            "price"
        ),

        "currency": search_parameters.get(
            "currency",
            "INR"
        ),

        "api_source": "SERPAPI"
    }