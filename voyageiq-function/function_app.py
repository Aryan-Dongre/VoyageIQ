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
            "https://serpapi.com/search.json",
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

