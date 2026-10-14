from flask import current_app
import requests

class WeatherAPI:
    # All the data fetch related work present over here 
    def __init__(self):

         self.base_url = current_app.config["WEATHER_API_URL"]

    def search_weather(self, destination):

        params = {
              "destination": destination
         }

        try:
                response = requests.get(
                   f"{self.base_url}/api/weather",
                   params=params,
                   timeout=30
                )

                response.raise_for_status()
                return response.json()
         
        except requests.RequestException as e:
              current_app.logger.error(
                   f"Weather Function request failed: {e}"
              )
              return None

        except (ValueError, TypeError) as e:
             current_app.logger.error(
                  f"Invaild Weather Function response: {e}"
             )
             return None

        except Exception as e:
            current_app.logger.error(
                f"Error processing Weather Function response: {e}"
            )
            return None

                     
         
         
         

          
