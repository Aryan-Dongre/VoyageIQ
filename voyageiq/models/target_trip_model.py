from voyageiq.database.db import get_db_connection

class TargetTripModel:

    @staticmethod
    def create_target_trip(target_trip_data):

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           INSERT INTO target_trips(
                            user_id,
                           origin,
                           destination,
                           travelers,
                           travel_class,
                           start_month,
                           end_month,
                           travel_year,
                           flight_min_price,
                           flight_max_price,
                           hotel_min_price,
                           hotel_max_price
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
                                    %s
                            ) RETURNING target_trip_id;
                            """, ( 
                                    target_trip_data["user_id"],
                                    target_trip_data["origin"],
                                    target_trip_data["destination"],
                                    target_trip_data["travelers"],
                                    target_trip_data["travel_class"],
                                    target_trip_data["start_month"],
                                    target_trip_data["end_month"],
                                    target_trip_data["travel_year"],
                                    target_trip_data["flight_min_price"],
                                    target_trip_data["flight_max_price"],
                                    target_trip_data["hotel_min_price"],
                                    target_trip_data["hotel_max_price"]
                   ))
            target_trip_id  = cursor.fetchone()["target_trip_id"]
            conn.commit()
            return target_trip_id
        
        except Exception as e:
            conn.rollback()
            raise e
        
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_user_target_trips(user_id):

        conn = get_db_connection()
        cursor= conn.cursor()

        try:
            cursor.execute("""
                         SELECT *
                           FROM target_trips
                           WHERE user_id = %s
                           ORDER BY created_at DESC
                           """, (user_id,))
            
            target_trips = cursor.fetchall()
            return target_trips

        except Exception as e:
            raise e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_target_trip_by_id(target_trip_id):

        conn = get_db_connection()
        cur = conn.cursor()

        try:

            query = """
                SELECT *
                FROM target_trips
                WHERE target_trip_id = %s
            """

            cur.execute(query, (target_trip_id,))

            target_trip = cur.fetchone()

            return target_trip

        except Exception as e:
            raise e

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def update_target_trip(target_trip_id, target_trip_data):

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           UPDATE target_trips
                           SET
                            origin = %s,
                            destination = %s,
                            travelers = %s,
                            travel_class = %s,
                            start_month = %s,
                            end_month = %s,
                            travel_year = %s,
                            flight_min_price = %s,
                            flight_max_price = %s,
                            hotel_min_price = %s,
                            hotel_max_price = %s,
                            updated_at = CURRENT_TIMESTAMP
                            WHERE target_trip_id = %s
                           """, (
                                    target_trip_data["origin"],
                                    target_trip_data["destination"],
                                    target_trip_data["travelers"],
                                    target_trip_data["travel_class"],
                                    target_trip_data["start_month"],
                                    target_trip_data["end_month"],
                                    target_trip_data["travel_year"],
                                    target_trip_data["flight_min_price"],
                                    target_trip_data["flight_max_price"],
                                    target_trip_data["hotel_min_price"],
                                    target_trip_data["hotel_max_price"],
                                    target_trip_id
                                ))
            conn.commit()
            return cursor.rowcount >0

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cursor.close()
            conn.close()                        

    @staticmethod
    def delete_target_trip(target_trip_id):

        conn = get_db_connection()
        cur = conn.cursor()

        try:

            query = """
                DELETE FROM target_trips
                WHERE target_trip_id = %s
            """

            cur.execute(query, (target_trip_id,))

            conn.commit()

            return cur.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e

        finally:
            cur.close()
            conn.close()        
