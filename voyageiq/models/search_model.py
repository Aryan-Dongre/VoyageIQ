from voyageiq.database.db import get_db_connection


def create_search(search_data):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                        INSERT INTO searches(
                            origin,
                            destination,
                            departure_date,
                            return_date,
                            adults,
                            travel_class,
                            search_status,
                            trip_type,
                            rooms,
                            search_type
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
                              %s   
                            )
                       RETURNING search_id
                        """, (
                             search_data["origin"],
                            search_data["destination"],
                            search_data["departure_date"],
                            search_data["return_date"],
                            search_data["adults"],
                            search_data["travel_class"],
                            "SUCCESS",
                            search_data["trip_type"],
                            search_data["rooms"],
                            search_data["search_type"]
                        ))
        search_id  =cursor.fetchone()["search_id"]

        conn.commit()
        return search_id
    
    finally:
        cursor.close()
        conn.close()
        