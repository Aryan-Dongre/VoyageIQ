import pandas as pd

from voyageiq.database.db import get_db_connection
from voyageiq import create_app

app = create_app()

def import_airports():

    df = pd.read_csv("database/airports.csv")

    # Keep the required columns

    df = df [[
                "iata_code",
                "name",
                "municipality",
                "iso_country",
                "latitude_deg",
                "longitude_deg"
            ]]
    
    # Remove row without airport code
    df = df.dropna(subset=["iata_code"])

    with app.app_context():

        conn = get_db_connection()

        
        cursor = conn.cursor()

        try:
            for _, row in df.iterrows():
                cursor.execute("""
                                INSERT INTO airports (
                        airport_code,
                        city_name,
                        airport_name,
                        country,
                        latitude,
                        longitude
                            )
                            VALUES (
                                %s,
                                %s,
                                %s,
                                %s,
                                %s,
                                %s
                            )  
                            ON CONFLICT (airport_code) DO NOTHING
                            """, (
                                    row["iata_code"],
                                    row["municipality"],
                                    row["name"],
                                    row["iso_country"],
                                    row["latitude_deg"],
                                    row["longitude_deg"]
                            ))
                
            conn.commit()

            print(f"{len(df)} airports imported successfully.")

        finally:
            cursor.close()
            conn.close()        

if __name__ == "__main__":
    import_airports()        