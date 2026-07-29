from flask import current_app
import requests
class HotelAPI:

    def __init__(self):
        self.api_key = current_app.config["SERPAPI_API_KEY"]
        self.base_url = "https://serpapi.com/search.json"

    def search_hotels(self, search_data):

        params = {  # to send the data to the API in its format
            "engine": "google_hotels",
            "q": search_data["destination"],
            "gl": "in",
            "currency": "INR",
            "check_in_date": str(search_data["departure_date"]),  # Api string formate me date leta hai
            "check_out_date": str(search_data["return_date"]),
            "rooms": search_data["rooms"],
            "adults": search_data["adults"],
            "api_key": self.api_key
        }    

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=30)
            
            response.raise_for_status()

            data = response.json()

            return self._extract_hotels(
                   data,
                    search_data["destination"])
        
        except requests.RequestException as e:
            current_app.logger.error(f"Hotel API request failed: {e}")
            return []
        
        except Exception as e:
            current_app.logger.error(f"Error processing hotel API response: {e}")
            return []
        
    def _extract_hotels(self, data, destination):   # this function is use to extracct the use full information from the API key 

        hotels = []

        properties = data.get("properties", [])

        for hotel in properties:

           
            # Hotel Image
     

            images = hotel.get("images", [])

            hotel_image = None

            if images:
                hotel_image = images[0].get("thumbnail")

            
            # Hotel Location
            

            location = hotel.get("address")

            if not location:

                nearby = hotel.get("nearby_places", [])

                if nearby:
                    location = nearby[0].get("name")
                else:
                    location = destination

            
            # Hotel Price
            

            rate_info = hotel.get("rate_per_night", {})

            price = rate_info.get("extracted_lowest")

            hotels.append({

                "hotel_name": hotel.get("name"),

                "location": location,

                "amenities": ", ".join(
                    hotel.get("amenities", [])
                ),

                "star_rating": hotel.get("overall_rating"),

                "review_score": hotel.get("overall_rating"),

                "review_count": hotel.get("reviews"),

                "room_type": hotel.get("type"),

                "price_per_night": price,

                "currency": "INR",

                "hotel_image": hotel_image,

                "api_source": "SERPAPI"

            })


        return hotels