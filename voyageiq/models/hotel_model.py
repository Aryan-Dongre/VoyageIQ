from voyageiq.database.db import get_db_connection

def create_hotel(search_id, hotel_data):

    conn  = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                       INSERT INTO hotels(
                              search_id,
                                hotel_name,
                                location,
                                amenities,
                                star_rating,
                                review_score,
                                review_count,
                                room_type,
                                price_per_night,
                                currency,
                                hotel_image,
                                api_source
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
                                %s)
                       """, (
                           search_id,
                           hotel_data["hotel_name"],
                            hotel_data["location"],
                            hotel_data["amenities"],
                            hotel_data["star_rating"],
                            hotel_data["review_score"],
                            hotel_data["review_count"],
                            hotel_data["room_type"],
                            hotel_data["price_per_night"],
                            hotel_data["currency"],
                            hotel_data["hotel_image"],
                            hotel_data["api_source"]
                       ))
        
        conn.commit()
        
    finally:
        cursor.close()
        conn.close()    