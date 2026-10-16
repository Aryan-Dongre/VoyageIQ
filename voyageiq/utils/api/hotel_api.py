from flask import current_app
import requests
class HotelAPI:

    def __init__(self):
        self.base_url = current_app.config["HOTEL_API_URL"]
        

    def search_hotels(self, search_data):

        params = {  # to send the data to the API in its format
            "destination": search_data["destination"],
            "check_in_date": str(search_data["departure_date"]),
            "check_out_date": str(search_data["return_date"]),
            "rooms": search_data["rooms"],
            "adults": search_data["adults"]
        }    

        try:
            response = requests.get(
                f"{self.base_url}/api/hotels",
                params=params,
                timeout=30)
            
            response.raise_for_status()

            data = response.json()

            return data.get("hotels", [])
        
        except requests.RequestException as e:
            current_app.logger.error(f"Hotel API request failed: {e}")
            return []


        except (ValueError, TypeError) as e:
            current_app.logger.error(f"Invalid Hotel Function response: {e}")
            return []

        except Exception as e:
            current_app.logger.error(f"Error processing hotel function response: {e}")
            return []
        