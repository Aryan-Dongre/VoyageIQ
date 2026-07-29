from flask import Flask
from config import Config

from voyageiq.blueprint.auth import auth_bp
from voyageiq.blueprint.auth import routes
from voyageiq.blueprint.home import home_bp
from voyageiq.blueprint.flights import flight_bp
from voyageiq.blueprint.hotels import hotel_bp
from voyageiq.blueprint.weather import weather_bp
from voyageiq.blueprint.contact import contact_bp
from voyageiq.blueprint.dashboard import dashboard_bp
from voyageiq.blueprint.target_trip import target_trip_bp
from voyageiq.blueprint.profile import profile_bp

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(hotel_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(target_trip_bp)
    app.register_blueprint(profile_bp)

    return app