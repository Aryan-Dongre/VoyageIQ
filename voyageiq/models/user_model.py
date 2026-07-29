# In this file we are keeping the user related code
# like create a user, user by email etc
# in future we will add update the profile of user , country etc


from voyageiq.database.db import get_db_connection

class UserModel:   #Using oops concept Encapsulation + Abstraction

    @staticmethod  # using static method so we dont need to create obeject now
    def get_user_by_email(email):

        # use to identify the user by email if present 

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                    SELECT * FROM users
                           WHERE email = %s
                           """,(email,))
            return cursor.fetchone()
        
        except Exception as e:
            print(f"Error fetching user by email: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()


    @staticmethod
    def create_user(full_name, email, phone):

        print("Inside create user")
        print(full_name, email, phone)

        # to create a new user

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           INSERT INTO users
                           (full_name, email,phone)
                           VALUES(
                           %s,
                           %s,
                           %s)
                           RETURNING user_id
                           """, (full_name, email, phone))

            user_id = cursor.fetchone()["user_id"]
            print("Created user id:", user_id)

            conn.commit()

            return user_id

        except Exception as e:

            if conn:
                conn.rollback()

            print(f"Error to create user: {e}")
            return None
         
        finally:

            cursor.close()
            conn.close()            