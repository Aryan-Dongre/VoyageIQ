from voyageiq.utils.api.weather_api import WeatherAPI
from voyageiq.models.weather_model import create_weather
from voyageiq.models.search_model import create_search

# The whole logic present over here

class WeatherService:

    def search_weather(self, form):  # this is the main function 

        search_data = {
            "origin" : None,

            "destination": form.destination.data,

            "departure_date": None,

            "return_date": None,

            "adults": None,

            "travel_class": None,

            "trip_type": None,

            "rooms": None,

            "search_type": "WEATHER"
        }

        search_id = create_search(search_data)

        api = WeatherAPI()  # it is the obj which can be use to call any func of WeatherAPI

        weather_data =  api.search_weather(
                          search_data["destination"]
                        )
        
        if not weather_data:
           return None
        current_weather = weather_data["current_weather"]
         
        # API  weather condition ka code diya ham wo code ke resptive word ko user ko denge 
         
        current_weather["weather_condition"] = (
                            self.get_weather_condition(
                                   current_weather["weather_code"]
                            )
                        )
        # same code ko icon and word  ke sath represent karenge

        current_weather["weather_icon"] =(
                          self.get_weather_icon(
                                 current_weather["weather_code"]
                            )
                        )
        
        weather_data["recommendations"] = (
                                           self.generate_recommendations(
                                          current_weather,
                                           weather_data["forecast"]
                                         ) 
                                         )
        
        create_weather(search_id,weather_data)
        
        return weather_data
    
            # In this way we are presenting the data {
                    #"temperature": 26.9,

                    #"weather_code": 55,

                    #"weather_condition": "Dense Drizzle",

                    #"weather_icon": "fa-solid fa-cloud-rain"
                #}
    
    WEATHER_CODES = {
                    0: "Clear Sky",

                    1: "Mainly Clear",

                    2: "Partly Cloudy",

                    3: "Overcast",

                    45: "Fog",

                    48: "Depositing Fog",

                    51: "Light Drizzle",

                    53: "Moderate Drizzle",

                    55: "Dense Drizzle",

                    61: "Slight Rain",

                    63: "Moderate Rain",

                    65: "Heavy Rain",

                    80: "Rain Showers",

                    95: "Thunderstorm",

                    96: "Thunderstorm With Hail",

                    99: "Heavy Thunderstorm"
                }
    
    def get_weather_condition(self, weather_code):
          # This func will tell about the condition of weather 
        
        return self.WEATHER_CODES.get(
                  weather_code,
                  "Unknown Weather"
        )
    
    def get_weather_icon(self, weather_code):

        if weather_code == 0:
            return "fa-solid fa-sun"
        
        if weather_code in [1,2]:
            return  "fa-solid fa-cloud-sun"
        
        if weather_code == 3:

          return "fa-solid fa-cloud"

        if weather_code in [45, 48]:

           return "fa-solid fa-smog"

        if weather_code in [51, 53, 55]:

          return "fa-solid fa-cloud-rain"

        if weather_code in [61, 63, 65, 80]:

           return "fa-solid fa-cloud-showers-heavy"

        if weather_code in [95, 96, 99]:

          return "fa-solid fa-cloud-bolt"

        return "fa-solid fa-cloud"
    
    def generate_recommendations(
        self,
        current_weather,
        forecast):

        recommendations = []

        temperature = current_weather.get(
            "temperature",
            0
        )

        humidity = current_weather.get(
            "humidity",
            0
        )

        weather_code = current_weather.get(
            "weather_code",
            0
        )

        wind_speed = current_weather.get(
            "wind_speed",
            0
        )

        rain_percent = max(
            [
                day.get("rain_percent", 0)
                for day in forecast
            ],
            default=0
        )

        # Rain Conditions

        if rain_percent >= 70:

            recommendations.append(
                "Heavy rain is expected during your visit."
            )

            recommendations.append(
                "Carry an umbrella during your trip."
            )

            recommendations.append(
                "Outdoor activities may be affected by rainfall."
            )

        elif rain_percent >= 40:

            recommendations.append(
                "Moderate rainfall is possible."
            )

            recommendations.append(
                "Keep an umbrella handy while travelling."
            )

        # Thunderstorm

        if weather_code in [95, 96, 99]:

            recommendations.append(
                "Thunderstorms are expected in the forecast."
            )

            recommendations.append(
                "Avoid unnecessary outdoor travel during storm periods."
            )

            recommendations.append(
                "Consider indoor sightseeing activities."
            )

        # Hot Weather

        if temperature >= 35:

            recommendations.append(
                "Hot weather conditions are expected."
            )

            recommendations.append(
                "Keep yourself hydrated throughout the day."
            )

            recommendations.append(
                "Avoid direct sun exposure during afternoon hours."
            )

        # Cold Weather

        if temperature <= 10:

            recommendations.append(
                "Cold weather is expected."
            )

            recommendations.append(
                "Carry warm clothing for comfortable travel."
            )

        # Humidity

        if humidity >= 85:

            recommendations.append(
                "High humidity levels are expected."
            )

            recommendations.append(
                "Expect warm and sticky conditions outdoors."
            )

        # Pleasant Weather

        if (
            20 <= temperature <= 30
            and rain_percent < 40
        ):

            recommendations.append(
                "Weather conditions are favorable for travel."
            )

            recommendations.append(
                "Great time for sightseeing and outdoor exploration."
            )

        # Windy Weather

        if wind_speed >= 25:

            recommendations.append(
                "Strong winds are expected."
            )

            recommendations.append(
                "Secure loose belongings while outdoors."
            )

        if not recommendations:
            recommendations.append(
                "Weather conditions are stable for travel."
            )    

        return recommendations

