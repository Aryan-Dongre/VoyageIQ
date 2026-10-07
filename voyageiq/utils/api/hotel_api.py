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