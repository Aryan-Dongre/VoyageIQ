from . import hotel_bp
from flask import jsonify, render_template, request

from voyageiq.services.hotel_service import HotelService
from voyageiq.blueprint.hotels.forms import HotelSearchForm

@hotel_bp.route("/hotel", methods=["GET", "POST"])
def hotel_search():

    form = HotelSearchForm()

    hotels = None

    if form.validate_on_submit():

        service = HotelService()

        hotels = service.search_hotels(form)

    return render_template(
        "hotel/search.html",
        form=form,
        hotels=hotels
    )    