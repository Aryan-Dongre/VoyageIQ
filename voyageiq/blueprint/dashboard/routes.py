from . import   dashboard_bp 
from flask import render_template, redirect
from flask import jsonify, request

from voyageiq.utils.decorators import login_required

from voyageiq.services.flight_service import FlightService
from voyageiq.blueprint.flights.forms import FlightSearchForm
from voyageiq.models.airport_model import search_airports

from voyageiq.services.hotel_service import HotelService
from voyageiq.blueprint.hotels.forms import HotelSearchForm

from voyageiq.blueprint.weather.forms import WeatherSearchForm
from voyageiq.services.weather_service import WeatherService

from voyageiq.services.dashboard_service import DashboardService
from voyageiq.blueprint.dashboard.forms import DashboardForm

from flask import request

@dashboard_bp.route("/", methods=["GET", "POST"])
@login_required
def dashboard():



    form = DashboardForm()

    dashboard_data = None

    if form.validate_on_submit():

        service = DashboardService()
        dashboard_data = service.analyze_trip(form)

      

    return render_template(
        "dashboard/dashboard.html",
        form=form,
        dashboard_data=dashboard_data
    )


@dashboard_bp.route("/flights", methods=["GET", "POST"])
@login_required
def flight():
    form = FlightSearchForm()

    flights =None

    if form.validate_on_submit():

        service = FlightService()
        flights = service.search_flight(form)

    return render_template("dashboard/flight/flight.html",
                                form=form, 
                                flights=flights)

@dashboard_bp.route("/airport/search")
@login_required
def airport_search():

    keyword = request.args.get("q", "")

    if len(keyword) <1 :
        return jsonify([])
    
    airports = search_airports(keyword)

    return jsonify(airports)


@dashboard_bp.route("/hotels", methods=["GET", "POST"])
@login_required
def hotel():

    form = HotelSearchForm()

    hotels = None

    if form.validate_on_submit():

        service = HotelService()

        hotels = service.search_hotels(form)

    return render_template(
        "dashboard/hotel/hotel.html",
        form=form,
        hotels=hotels
    )    

@dashboard_bp.route("/weather", methods=["GET", "POST"])
@login_required
def weather():

    form  = WeatherSearchForm()

    weather_results  =None

    if form.validate_on_submit():

        service = WeatherService()

        weather_results = service.search_weather(form)

       

    return render_template(
        "dashboard/weather/weather.html",
        form=form,
        weather_results=weather_results
    )    
