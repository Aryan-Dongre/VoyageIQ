from . import weather_bp
from voyageiq.blueprint.weather.forms import WeatherSearchForm
from voyageiq.services.weather_service import WeatherService
from flask import jsonify, render_template, request

@weather_bp.route("/weather", methods=["GET", "POST"])
def weather_search():

    form  = WeatherSearchForm()

    weather_results  =None

    if form.validate_on_submit():

        service = WeatherService()

        weather_results = service.search_weather(form)

       

    return render_template(
        "weather/weather.html",
        form=form,
        weather_results=weather_results
    )    
