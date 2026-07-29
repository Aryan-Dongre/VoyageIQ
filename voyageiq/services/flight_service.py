from voyageiq.utils.api.flight_api import FlightAPI
from voyageiq.models.flight_model import create_flight
from voyageiq.models.search_model import create_search

class FlightService:

    def search_flight(self, form):

        # This is use to take data from form 

        search_data = {
            "origin":form.origin.data,
            "destination": form.destination.data,
            "departure_date": form.departure_date.data,
            "return_date": form.return_date.data,
            "adults" : form.adults.data,
            "travel_class" : form.travel_class.data,
            "trip_type" : form.trip_type.data,
            "rooms": None,
            "search_type": "FLIGHT"
        }

        search_id = create_search(search_data)   # It will call the function to insert the data in serach table

        api = FlightAPI()

        flights = api.search_flights(search_data)

        for flight in flights:

            create_flight(search_id, flight)  # It will call the function to insert the data in flight table

        return flights
    
    
