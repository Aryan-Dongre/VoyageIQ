from flask import current_app
import requests

class FlightAPI:

    def __init__(self):

        self.base_url = current_app.config["FLIGHT_API_URL"]

    def search_flights(self, search_data):

        params = {
           "origin": search_data["origin"],
           "destination": search_data["destination"],
           "departure_date": str(
                search_data["departure_date"]
            ),
            "adults": search_data["adults"],
            "travel_class": search_data["travel_class"],
            "trip_type": search_data["trip_type"]
        }

        # Round trip
        if search_data["trip_type"] =="round_trip":

            params["return_date"] = str(search_data["return_date"])

        try:
            response = requests.get(
                f"{self.base_url}/api/flights",
                 params=params,
                timeout=30
            ) 

            response.raise_for_status() 

            data = response.json()

            return data.get("flights", [])

        except requests.RequestException as e:

            current_app.logger.error(
                f"Flight Function request failed: {e}"
            )
            return []

        except (ValueError, TypeError) as e:
              current_app.logger.error(
                f"Invalid Flight Function response: {e}"
            )

              return []

        except Exception as e:

            current_app.logger.error(
                f"Error processing Flight Function response: {e}"
            )

            return []

    
        


        
        