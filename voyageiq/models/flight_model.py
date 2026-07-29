from voyageiq.database.db import get_db_connection

# flight related function

def create_flight(search_id, flight_data):

    # Insert the data into the flight table comes from API

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                       INSERT INTO flights(
                       search_id,
                        airline,
                        flight_number,
                        departure_airport,
                        departure_city,
                        arrival_airport,
                        arrival_city,
                        stopover_airports,
                        departure_time,
                        arrival_time,
                        duration_minutes,
                        cabin_class,
                        price,
                        currency,
                        api_source
                       )
                       VALUES (
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
                            %s,
                            %s,
                            %s
                       )
                       """, (
                            search_id,
                            flight_data["airline"],
                            flight_data["flight_number"],
                            flight_data["departure_airport"],
                            flight_data["departure_city"],
                            flight_data["arrival_airport"],
                            flight_data["arrival_city"],
                            flight_data["stopover_airports"],
                            flight_data["departure_time"],
                            flight_data["arrival_time"],
                            flight_data["duration_minutes"],
                            flight_data["cabin_class"],
                            flight_data["price"],
                            flight_data["currency"],
                            flight_data["api_source"]
                       ))
        conn.commit()

    finally:
        cursor.close()
        conn.close()    
       