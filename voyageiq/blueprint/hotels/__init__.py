from flask import Blueprint

hotel_bp = Blueprint('hotel', __name__)

from voyageiq.blueprint.hotels import routes