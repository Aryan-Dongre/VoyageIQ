from flask import current_app
import requests

class WeatherAPI:
    # All the data fetch related work present over here 
    def __init__(self):
        
        self.geo_url = ("https://geocoding-api.open-meteo.com/v1/search")

        self.weather_url = ( "https://api.open-meteo.com/v1/forecast")

    def get_coordinates(self, destination):    # conver the city with there coordinate for Open Metro

        params = {

            "name": destination,

            "count": 1,

            "format": "json"
        }

        try:

            response = requests.get(
                        self.geo_url,
                        params=params,
                        timeout=30 
            )

            response.raise_for_status()

            data = response.json()

            # print(data)

            results = data.get("results", [])

            if not results:

                return None
            
            city = results[0]

            return {

                "latitude": city.get("latitude"),
                "longitude": city.get("longitude"),
                "country" : city.get("country"),
                "city" : city.get("name")
            }
        
        except requests.RequestException as e:
                
                current_app.logger.error(
                      f"Geocoding API request failed: {e}"
                   )

                return None
    
    def get_weather(self,latitude,longitude ):
                        # it send the longitude and latitude and receive the data information
                params = {

                    "latitude": latitude,

                    "longitude": longitude,

                    "current": [
                        "temperature_2m",
                        "relative_humidity_2m",
                        "apparent_temperature",
                        "weather_code",
                        "wind_speed_10m",
                        "visibility"
                    ],

                    "daily": [
                        "weather_code",
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_probability_max"
                    ],

                    "forecast_days": 5
                }

                try:

                    response = requests.get(
                        self.weather_url,
                        params=params,
                        timeout=30
                    )

                    response.raise_for_status()

                    return response.json()

                except requests.RequestException as e:

                    current_app.logger.error(
                        f"Weather API request failed: {e}"
                    )

                    return None

    def search_weather(self, destination):

        # it marge both above function into it 

        coordinates = self.get_coordinates(destination)

        if not coordinates:

            return None
        
        weather_data=  self.get_weather(
             coordinates["latitude"],
             coordinates["longitude"]
        )

        if not weather_data:
             
            return None
        
        return self._extract_weather(
              weather_data,
              coordinates
        )
    
    def _extract_weather(self, weather_data, coordinates):
         
        current = weather_data.get(
                           "current",
                           {}
                        )

        daily = weather_data.get(
                 "daily",
                 {}
                )

        current_weather = {
             
              "destination": coordinates["city"],

                "country": coordinates["country"],

                "temperature": current.get(
                    "temperature_2m"
                ),

                "feels_like": current.get(
                    "apparent_temperature"
                ),

                "humidity": current.get(
                    "relative_humidity_2m"
                ),

                "wind_speed": current.get(
                    "wind_speed_10m"
                ),

                "visibility": current.get(
                              "visibility"   
                ),

                "weather_code": current.get(
                    "weather_code"
                )
        }

        forecast = []

        dates = daily.get("time", [])

        max_temps =  daily.get(
                      "temperature_2m_max",
                      []
                    )

        min_temps =  daily.get(
                     "temperature_2m_min",
                     []
                    )

        weather_codes = daily.get(
                            "weather_code",
                            []
                        )

        rain_probability =  daily.get(
                              "precipitation_probability_max",
                             []
                            ) 
        
        
        for i in range(len(dates)):
             forecast.append({
                    "forecast_date": dates[i],

                    "temp_max": max_temps[i],

                    "temp_min": min_temps[i],

                    "weather_code": weather_codes[i],

                    "rain_percent": rain_probability[i]
                })
             
        return {
              "current_weather": current_weather,

               "forecast": forecast
        }     
                     
         
         
         

          
