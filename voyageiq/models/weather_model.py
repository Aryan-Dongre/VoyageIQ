from voyageiq.database.db import get_db_connection

def create_weather(search_id, weather_data):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:

        current_weather = weather_data["current_weather"]

        forecast = weather_data["forecast"]

        for day in forecast:

            cursor.execute("""
                            INSERT INTO weather_data(

                                    search_id,

                                    destination,

                                    forecast_date,

                                    temp_min,

                                    temp_max,

                                    humidity,

                                    weather_condition,

                                    rain_percent,

                                    wind_speed,

                                    api_source,

                                    current_temperature,

                                    feels_like_temperature,

                                    visibility

                                )

                                VALUES(

                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s,
                                    %s

                                ) """, (
                                    search_id,
                                    current_weather["destination"],
                                    day["forecast_date"],
                                    day["temp_min"],
                                    day["temp_max"],
                                    current_weather["humidity"],
                                    current_weather["weather_condition"],
                                    day["rain_percent"],
                                    current_weather["wind_speed"],
                                    "OPEN_METRO",
                                    current_weather["temperature"],
                                    current_weather["feels_like"],
                                    current_weather["visibility"]

                                ))
            
            conn.commit()
    finally:
        cursor.close()
        conn.close()    