from voyageiq.utils.api.flight_api import FlightAPI
from voyageiq.utils.api.hotel_api import HotelAPI
from voyageiq.utils.api.weather_api import WeatherAPI

from voyageiq.services.weather_service import WeatherService

class DashboardService:
    
    def analyze_trip(self, form):

        search_data = {
            "origin": form.origin.data,
            "destination": form.destination.data,
            "departure_date": form.departure_date.data,
            "return_date": form.return_date.data,
            "adults": form.adults.data,
            "travel_class": form.travel_class.data,
            "trip_type": form.trip_type.data,

            # for hotel
            "rooms":1
        }

        flight_api = FlightAPI()
        hotel_api = HotelAPI()
        weather_api = WeatherAPI()
        weather_service = WeatherService()

        # Flight part
        try :
            flights = flight_api.search_flights(search_data)
            flights = flights[:3]

        except Exception:
            flights = []

        # Hotel part
        try:
            hotels = hotel_api.search_hotels(search_data)
            hotels = hotels[:3]
        
        except Exception:
            hotels=[]    

        # Weather part
        try:
            weather_data = weather_api.search_weather(search_data["destination"])

            if weather_data:
                current_weather = weather_data["current_weather"]

                current_weather["weather_condition"] = (
                             weather_service.get_weather_condition(
                               current_weather["weather_code"]
                           )
                )

                current_weather["weather_icon"] = (weather_service.get_weather_icon(current_weather["weather_code"]))

                weather_data["recommendations"] = (weather_service.generate_recommendations(current_weather,weather_data["forecast"]))

                budget_data  = self.caluculate_budget(flights, hotels)

                trip_score = self.calculate_trip_score(weather_data, budget_data)

                recommendation = self.generate_recommendation(trip_score, budget_data, weather_data)

        except Exception:
            weather_data = None
            budget_data = None
            trip_score = None
            recommendation = None

        return {
                "flights": flights,
                "hotels": hotels,
                "weather": weather_data,
                "budget": budget_data,
                "trip_score": trip_score,
                "recommendation": recommendation
            }

    def caluculate_budget(self, flights, hotels):

        if not flights or not hotels:
            return None
        
        # Cheapest flight 
        cheapest_flight = min(flights,
                               key=lambda flight: (  
                                   # key = lambda help karta hai kis bases pe compare karna hai wo batane me 
                                   # flights to ek dictionaries provide karti hai price and airline ke sath 
                                   # to kis bases me compare karna hai wo lambda batata hai
                                   flight["price"]
                                   if flight["price"] is not None
                                   else float("inf")  # inf means infinity mean a very large value
                               ))
        
        cheapest_hotel = min(hotels,
                             key=lambda hotel:
                             hotel["price_per_night"]
                             if hotel["price_per_night"] is not None
                             else float("inf"))
        
        flight_price = cheapest_flight["price"] or 0
        hotel_price = cheapest_hotel["price_per_night"] or 0

        total_budget = flight_price + hotel_price

        return {

                "cheapest_flight": cheapest_flight,

                "cheapest_hotel": cheapest_hotel,

                "flight_name": cheapest_flight["airline"],

                "flight_price": flight_price,

                "hotel_name": cheapest_hotel["hotel_name"],

                "hotel_price": hotel_price,

                "budget": total_budget
            }
    
    def calculate_trip_score(self, weather_data, budget_data):

        score = 10

        if not weather_data:
            score -= 2

        if not budget_data:
            score -= 2

        if weather_data:

            current_weather = weather_data[
                "current_weather"
            ]

            temperature = current_weather[
                "temperature"
            ]

            forecast = weather_data[
                "forecast"
            ]

            max_rain = max(
                [
                    day.get(
                        "rain_percent",
                        0
                    )
                    for day in forecast
                ],
                default=0
            )

            if max_rain >= 70:
                score -= 3

            elif max_rain >= 40:
                score -= 2

            if temperature < 10:
                score -= 2

            elif temperature > 35:
                score -= 2

        if budget_data:

            budget = budget_data["budget"]

            if budget > 60000:
                score -= 3

            elif budget > 40000:
                score -= 1

        return max(1, score)
    

    def generate_recommendation(self, trip_score, budget_data, weather_data):

        if trip_score >= 8:

            status = "Highly Recommended"

            message = (
                "Excellent weather conditions "
                "and reasonable travel cost."
            )

        elif trip_score >= 6:

            status = "Recommended"

            message = (
                "Good travel option with "
                "acceptable weather and budget."
            )

        elif trip_score >= 4:

            status = "Consider Different Dates"

            message = (
                "Travel is possible, but weather "
                "or pricing could improve."
            )

        else:

            status = "Not Recommended"

            message = (
                "Poor weather conditions or "
                "high travel cost."
            )

        return {

            "trip_score": trip_score,

            "status": status,

            "message": message,

            "recommended_flight":
                budget_data["cheapest_flight"],

            "recommended_hotel":
                budget_data["cheapest_hotel"],

            "weather_summary":
                weather_data["current_weather"]
                ["weather_condition"]

        }