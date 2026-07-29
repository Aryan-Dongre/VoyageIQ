from voyageiq.database.db import get_db_connection

class ProfileModel:

    @staticmethod
    def get_user_profile(user_id):

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                      SELECT 
                        u.user_id,   
                        u.full_name,
                        u.email,
                        a.username,
                        u.phone,
                        u.country,
                        u.profile_picture,
                        u.created_at
                        FROM users u

                        INNER JOIN authentication a
                        ON u.user_id = a.user_id
                        WHERE u.user_id = %s         
                     """,(user_id,))
            user_profile = cursor.fetchone()

            return user_profile
        
        except Exception as e:
            print(f"Error to load user profile: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def update_user_profile(user_id, full_name, phone, country, profile_picture):

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           UPDATE users
                           SET 
                           full_name = %s,
                           phone = %s,
                           country = %s,
                           profile_picture = %s,
                           updated_at = CURRENT_TIMESTAMP

                           WHERE user_id = %s
                           """, (full_name, phone, country, profile_picture, user_id))
            
            conn.commit()
            return True
        
        except Exception as e:
            print(f"Error to update the profile details: {e}")
            conn.rollback()
            return None
        
        
        finally:
            cursor.close()
            conn.close()
