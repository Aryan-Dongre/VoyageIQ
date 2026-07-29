from voyageiq.models.target_trip_model import TargetTripModel

class TravelTripService:

    @staticmethod
    def create_target_trip(form, user_id):

        # This function will send the data to the target trip table to insert the data it receive from the form 
        # It only work when new trip is created


        target_trip_data = {
                        "user_id": user_id,
                        "origin": form.origin.data,
                        "destination": form.destination.data,

                        "travelers": form.travelers.data,
                        "travel_class": form.travel_class.data,

                        "start_month": form.start_month.data,
                        "end_month": form.end_month.data,
                        "travel_year": form.travel_year.data,

                        "flight_min_price": form.flight_min_price.data,
                        "flight_max_price": form.flight_max_price.data,

                        "hotel_min_price": form.hotel_min_price.data,
                        "hotel_max_price": form.hotel_max_price.data
                     }      
        target_trip_id = TargetTripModel.create_target_trip(target_trip_data)  

        return target_trip_id
        

    @staticmethod
    def get_user_target_trips(user_id): 
         # This function is retrieves all save target trip
         # for this we are using user_id to fetch all the information related to that id

        target_trips = TargetTripModel.get_user_target_trips(user_id)

        return target_trips   
    
    @staticmethod
    def get_target_trip(target_trip_id, user_id):
        # This func is use to load a particular trip
        # this will hepl in find search, edit, and delete the trip
        # It will retrieve that particular data from db

        target_trip = TargetTripModel.get_target_trip_by_id(target_trip_id)

        if not target_trip:
            return None
        
        if target_trip["user_id"]!= user_id:
            return None
        
        return target_trip
    
    @staticmethod
    def update_target_trip(target_trip_id, form, user_id):

        # It is use to modify the existing trip 

        target_trip = TargetTripModel.get_target_trip_by_id(target_trip_id)  # To load that particular trip

        if not target_trip:
            return False
        
        if target_trip["user_id"]!= user_id:
            return False
        
        target_trip_data = {
            "origin": form.origin.data,
            "destination": form.destination.data,

            "travelers": form.travelers.data,
            "travel_class": form.travel_class.data,

            "start_month": form.start_month.data,
            "end_month": form.end_month.data,
            "travel_year": form.travel_year.data,

            "flight_min_price": form.flight_min_price.data,
            "flight_max_price": form.flight_max_price.data,

            "hotel_min_price": form.hotel_min_price.data,
            "hotel_max_price": form.hotel_max_price.data
        }
        
        return TargetTripModel.update_target_trip(target_trip_id, target_trip_data)  # It send the new update data to model to save it in db
       
    
    @staticmethod
    def delete_target_trip(target_trip_id, user_id):

        # To remove the trip 

        target_trip = TargetTripModel.get_target_trip_by_id(target_trip_id) # To load a trip

        if not target_trip:
            return False
        
        if target_trip["user_id"]!= user_id:
            return False
        
        return TargetTripModel.delete_target_trip(target_trip_id)