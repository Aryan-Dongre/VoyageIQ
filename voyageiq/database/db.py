import psycopg2
from flask import current_app
from psycopg2.extras import RealDictCursor

def get_db_connection():

    try:
        connection = psycopg2.connect(
            host=current_app.config["DB_HOST"],
            database=current_app.config["DB_NAME"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            port=current_app.config["DB_PORT"],
            sslmode='require',   # Add this line for azure database connection
            cursor_factory=RealDictCursor
        )
        return connection
        
    
    except Exception as e:
        print("DB connection fail", e)
        return None