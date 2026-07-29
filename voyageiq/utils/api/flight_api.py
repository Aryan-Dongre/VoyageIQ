from flask import current_app
import requests

class FlightAPI:

    def __init__(self):

        self.api_key = current_app.config["SERPAPI_API_KEY"]

        self.base_url = "https://serpapi.com/search.json"

    def search_flights(self, search_data):

        params = {
            "engine": "google_flights",
            "departure_id": search_data["origin"],    # set parameters acc to our search 
            "arrival_id" : search_data["destination"],
            "outbound_date": str(search_data["departure_date"]),
            "adults" : search_data["adults"],
            "currency": "INR",
            "gl": "in",
            "api_key":self.api_key
        }

        # Round trip
        if search_data["trip_type"] =="round_trip":

            params["type"] =1

            params["return_date"] = str(search_data["return_date"])
        else:

            params["type"] = 2

        # Cabin class
        cabin_map = {
                    "economy": 1,
                    "premium_economy": 2,
                    "business": 3,
                    "first": 4
                }  

        params["travel_class"] = cabin_map.get(
                     search_data["travel_class"],
                     1
        )   
        
        response = requests.get(   # this will send request to api
            self.base_url,
            params=params
        )

        data =  response.json()    

        

        return self._extract_flights(data)

    def _extract_flights(self, data):

        flight_list = []

        for flight in data.get("best_flights", []):

            first_flight = flight["flights"][0] 
            last_flight = flight["flights"][-1] 

            flight_data = {

                "airline": first_flight.get("airline"),
                
                "flight_number": first_flight.get("flight_number"),
                
                "departure_airport":first_flight["departure_airport"].get("name"),

                "departure_city":first_flight["departure_airport"].get("id"),

                "arrival_airport":last_flight["arrival_airport"].get("name"),

                "arrival_city":last_flight["arrival_airport"].get("id"),

                "stopover_airports": None,

                "departure_time":first_flight["departure_airport"].get("time"),

                "arrival_time":last_flight["arrival_airport"].get("time"),

                "duration_minutes":flight.get("total_duration"),

                "cabin_class":first_flight.get("travel_class"),

                "price":flight.get("price"),

                "currency":data["search_parameters"].get("currency"),

                "api_source": "SERPAPI"
                
            }  
            

            flight_list.append(flight_data)

        return flight_list
        


        
        