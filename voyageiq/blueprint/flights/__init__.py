from flask import Blueprint

flight_bp = Blueprint("flight", __name__, url_prefix="/flight")

from voyageiq.blueprint.flights import routes