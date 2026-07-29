from voyageiq.utils.api.hotel_api import HotelAPI
from voyageiq.models.hotel_model import create_hotel
from voyageiq.models.search_model import create_search

class HotelService:

    def search_hotels(self, form):
            
          # ye pura ek data hai jo user se form ke through aaya hai 
          # aur validation check hone ke baad ye jayenga seach table me 
            
        search_data = {
             "origin": None,
             "destination": form.destination.data,

            # check-in stored in departure_date
            "departure_date": form.check_in_date.data,

            # check-out stored in return_date
            "return_date": form.check_out_date.data,

            "adults": form.adults.data,
            "travel_class": None,
            "trip_type": None,
            "rooms": form.rooms.data,
            "search_type": "HOTEL"
        }

        search_id = create_search(search_data)
         
        # yaha ye api ek object hai jo base url and api key ko acess kar raha hai

        api = HotelAPI()

        # API key google hotel se data layengi waha ke set func ke according kam karengi 
        # phir yaha aaynega aur uske baad hotel table me jayenga pura data

        hotels = api.search_hotels(search_data)  # This will call the function and send into search table


        for hotel in hotels:

            create_hotel(search_id, hotel) # This will call the function and send into hotel table

        return hotels    