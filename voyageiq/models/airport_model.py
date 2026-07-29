from voyageiq.database.db import get_db_connection

def  search_airports(keyword):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                        SELECT
                       airport_code,
                       city_name,
                       airport_name
                       
                       FROM airports
                       WHERE city_name ILIKE %s
                       OR airport_code ILIKE %s
                       OR airport_name ILIKE %s
                       LIMIT 10;
                       """, (f"%{keyword}%",
                             f"%{keyword}%",
                             f"%{keyword}%"))
        
        airports = cursor.fetchall()
        return airports
    
    finally:
        cursor.close()
        conn.close()
      