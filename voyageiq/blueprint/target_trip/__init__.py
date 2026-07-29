from flask import Blueprint

target_trip_bp  = Blueprint('target_trip', __name__,
                            url_prefix="/target_trip")

from voyageiq.blueprint.target_trip import routes