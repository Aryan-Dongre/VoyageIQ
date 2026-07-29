from voyageiq.database.db import get_db_connection

def create_contact(contact_data):

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                        INSERT INTO contact_messages( 
                        full_name,
                       email,
                       category,
                        message
                       )
                       VALUES (
                       %s,
                       %s,
                       %s,
                       %s
                       ) RETURNING contact_id
                       """,(
                            contact_data["full_name"],
                            contact_data["email"],
                            contact_data["category"],
                            contact_data["message"]
                       ))
        contact = cursor.fetchone()

        conn.commit()

    finally:
        cursor.close()
        conn.close()    