# This flie contant the logic related to the matching hotel and flight nothing else


from datetime import datetime, date
import calendar

from voyageiq.models.target_trip_model import TargetTripModel
from voyageiq.utils.api.flight_api import FlightAPI
from voyageiq.utils.api.hotel_api import HotelAPI

class TargetTripMatchService:

    @staticmethod
    def _generate_search_dates(start_month, end_month, travel_year):

        current_date = datetime.today()

        day = 1  # default day
        
        # Check current month and year

        if(travel_year == current_date.year and start_month==current_date.month):
            day = current_date.day

        # validate day for start month

        start_month_last_day = calendar.monthrange(travel_year, start_month)[1]

        departure_day = min(day, start_month_last_day)  # if the day is not belong to the moth so it will take min value 

        departure_date = date(
            travel_year,
            start_month,
            departure_day
        )     

        # validate same day for end month 
        end_month_last_day = calendar.monthrange(
                 travel_year, 
                 end_month)[1]
        
        return_day = min(day, end_month_last_day)

        return_date = date(
            travel_year,
            end_month,
            return_day
        )

        return departure_date, return_date

    @staticmethod
    def _add_flight_status(flights, trip):

        max_price = float(trip["flight_max_price"])

        tolerance_price = (max_price*1.20)

        for flight in flights:

            price = flight.get("price")

            if price is None:
                flight["match_status"] = "unknown"
                continue

            if price <=max_price:
                flight["match_status"] = "perfect_match"
            
            elif price <=  tolerance_price:
                flight["match_status"] = "close_match"

            else:
                flight["match_status"] = "above_budget"
        
        return flights                


    @staticmethod
    def _add_hotel_match_status(hotels, trip):

        max_price = float(trip["hotel_max_price"])

        tolerance_price = (max_price*1.20)

        for hotel in hotels:
            price = hotel.get("price_per_night")

            if price is None:
                hotel["match_status"] =  "unknown"
                continue

            if price <= max_price:
                hotel["match_status"] = "perfect_match"

            elif price<= tolerance_price:
                hotel["match_status"] = "close_match"

            else:
                hotel["match_status"] = "above_budget"

        return hotels  

    @staticmethod
    def find_matches(target_trip_id, user_id):

        trip = TargetTripModel.get_target_trip_by_id(target_trip_id)

        if not trip:
            return None

        departure_date, return_date = (
                        TargetTripMatchService._generate_search_dates(
                            trip["start_month"],
                            trip["end_month"],
                            trip["travel_year"]
                        )
        )

        flight_search_data = {
            "origin": trip["origin"],
            "destination": trip["destination"],
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": trip["travelers"],
            "travel_class": trip["travel_class"],
            "trip_type": "round_trip"
        }   

        flight_api = FlightAPI()

        flights = flight_api.search_flights(flight_search_data)

        flights = (
            TargetTripMatchService._add_flight_status(flights,trip)
                  )

        hotel_search_data = {
            "destination": trip["destination"],
            "departure_date": departure_date,
            "return_date": return_date,
            "adults": trip["travelers"],
            "rooms": 1
            }  

        hotel_api = HotelAPI()

        hotels = hotel_api.search_hotels(
            hotel_search_data
        )

        hotels = (TargetTripMatchService._add_hotel_match_status(hotels, trip))

    
        return {
            "trip": trip,
            "departure_date": departure_date,
            "return_date": return_date,
            "flights": flights,
            "hotels": hotels
        }         