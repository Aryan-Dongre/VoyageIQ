from flask import Blueprint

weather_bp = Blueprint("weather", __name__)

from voyageiq.blueprint.weather import routes