from . import flight_bp

from flask import jsonify, render_template, request

from voyageiq.services.flight_service import FlightService
from voyageiq.blueprint.flights.forms import FlightSearchForm
from voyageiq.models.airport_model import search_airports

@flight_bp.route("/flights", methods=["GET", "POST"])
def flight_search():

    form = FlightSearchForm()

    flights =None

    if form.validate_on_submit():

        service = FlightService()
        flights = service.search_flight(form)

    return render_template("flights/search.html",
                                form=form, 
                                flights=flights)

@flight_bp.route("/airports/search")
def airport_search():

    keyword = request.args.get("q", "")

    if len(keyword) <1 :
        return jsonify([])
    
    airports = search_airports(keyword)

    return jsonify(airports)