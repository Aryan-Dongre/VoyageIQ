# In this file we are keeping the authentication code 

from voyageiq.database.db import get_db_connection

class AuthModel: 
    @staticmethod
    def get_auth_by_username(username):
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                    SELECT * FROM 
                    authentication
                    WHERE username = %s
                      """, (username,))
            return cursor.fetchone()
        
        except Exception as e:
            print(f"username data not found: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
            

    @staticmethod
    def create_auth_record(user_id, username,password_hash):
        
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                            INSERT INTO authentication
                                (user_id,username,password_hash )
                                VALUES(
                                %s,
                                %s,
                                %s)
                             RETURNING auth_id
                            """, (user_id, username,password_hash))
            
            auth_id = cursor.fetchone()["auth_id"]
            conn.commit()

            return auth_id
        
        except Exception as e:

            if conn:
                conn.rollback()

            print(f"Error to fetch the data: {e}")
            return None
    
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_login_user(identifier):

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                          SELECT
                           u.user_id,
                           u.full_name,
                           u.email,
                           a.username,
                           a.password_hash
                           FROM users u
                           INNER JOIN authentication a
                           ON u.user_id = a.user_id
                           WHERE u.email = %s
                            OR a.username = %s
                           """, (identifier,identifier))
            
            return cursor.fetchone()
        
        except Exception as e:

            print(f"Error fetching login user: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()



            
            