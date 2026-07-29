/* Creating all the tables*/

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    country VARCHAR(100),
    profile_picture TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE authentication (
    auth_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    session_token TEXT,
    last_login TIMESTAMP,
    token_expires_at TIMESTAMP,

	CONSTRAINT fk_auth_user
	FOREIGN KEY (user_id)
	REFERENCES users(user_id)
	ON DELETE CASCADE
	);

CREATE TABLE user_preferences (
    preference_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,

    preferred_airline VARCHAR(100),
    preferred_hotel_rating DECIMAL(2,1),

    budget_range VARCHAR(50),
    preferred_travel_class VARCHAR(50),
    preferred_weather VARCHAR(50),
    favorite_destination VARCHAR(100),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

	CONSTRAINT fk_pref_user
	FOREIGN KEY (user_id)
	REFERENCES users(user_id)
	ON DELETE CASCADE
	);

CREATE TABLE searches (
    search_id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,

    date_from DATE NOT NULL,
    date_to DATE,

    adults INTEGER DEFAULT 1,

    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_search_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
		);

	ALTER TABLE searches
	ALTER COLUMN user_id DROP NOT NULL;
	
	ALTER TABLE searches
	RENAME COLUMN date_from TO departure_date;
	
	ALTER TABLE searches
	RENAME COLUMN date_to TO return_date;
	
	ALTER TABLE searches
	ADD COLUMN travel_class VARCHAR(50);
	
	ALTER TABLE searches
	ADD COLUMN search_status VARCHAR(20);
	
	ALTER TABLE searches
	ADD COLUMN trip_type

	ALTER TABLE searches
    ADD COLUMN rooms INTEGER;

	ALTER TABLE searches
	ADD COLUMN search_type VARCHAR(20);
	
	ALTER TABLE searches
	ADD CONSTRAINT chk_search_type
	CHECK (
	    search_type IN (
	        'FLIGHT',
	        'HOTEL',
	        'WEATHER'
	    )
	);

	ALTER TABLE searches
   ALTER COLUMN origin DROP NOT NULL;

   ALTER TABLE searches
		ADD CONSTRAINT chk_origin_required_for_flight
		CHECK (
		    CASE
		        WHEN search_type = 'FLIGHT'
		        THEN origin IS NOT NULL
		        ELSE TRUE
		    END
		);

		ALTER TABLE searches
       ALTER COLUMN departure_date DROP NOT NULL;

	   ALTER TABLE searches
	   ADD CONSTRAINT chk_departure_required
	   CHECK(
              CASE
			       WHEN search_type IN ('FLIGHT', 'HOTEL')
				   THEN departure_date IS NOT NULL
				   ELSE TRUE
			  END   
	   );

	
	SELECT column_name, data_type
	FROM information_schema.columns
	WHERE table_name = 'searches';

CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,

    search_id INTEGER NOT NULL,

    airline VARCHAR(100),
    flight_number VARCHAR(50),

    departure_airport VARCHAR(100),
    departure_city VARCHAR(100),

    arrival_airport VARCHAR(100),
    arrival_city VARCHAR(100),

    stopover_airports TEXT,

    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,

    duration VARCHAR(50),

    stops INTEGER,

    cabin_class VARCHAR(50),

    price NUMERIC(10,2),

    currency VARCHAR(10),

    api_source VARCHAR(100),

    is_selected BOOLEAN DEFAULT FALSE,

    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_flight_search
        FOREIGN KEY (search_id)
        REFERENCES searches(search_id)
);

CREATE TABLE airports (
    airport_id SERIAL PRIMARY KEY,

    airport_code VARCHAR(10) UNIQUE NOT NULL,

    city_name VARCHAR(100),

    airport_name VARCHAR(200),

    country VARCHAR(100),

    latitude NUMERIC(10,6),

    longitude NUMERIC(10,6)
);



CREATE TABLE hotels (
    hotel_id SERIAL PRIMARY KEY,

    search_id INTEGER NOT NULL,

    hotel_name VARCHAR(255),

    location VARCHAR(255),

    amenities TEXT,

    star_rating DECIMAL(2,1),

    review_score DECIMAL(3,1),

    review_count INTEGER,

    room_type VARCHAR(100),

    price_per_night NUMERIC(10,2),

    currency VARCHAR(10),

    hotel_image TEXT,

    api_source VARCHAR(100),

    is_selected BOOLEAN DEFAULT FALSE,

    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_hotel_search
        FOREIGN KEY (search_id)
        REFERENCES searches(search_id)
);

CREATE TABLE weather_data (
    weather_id SERIAL PRIMARY KEY,

    search_id INTEGER NOT NULL,

    destination VARCHAR(100),

    forecast_date DATE,

    temp_min DECIMAL(5,2),
    temp_max DECIMAL(5,2),

    humidity INTEGER,

    weather_condition VARCHAR(100),

    rain_percent INTEGER,

    wind_speed DECIMAL(5,2),

    api_source VARCHAR(100),

    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_weather_search
        FOREIGN KEY (search_id)
        REFERENCES searches(search_id)
);

   ALTER TABLE weather_data
	ADD COLUMN current_temperature DECIMAL(5,2);
	
	ALTER TABLE weather_data
	ADD COLUMN feels_like_temperature DECIMAL(5,2);
	
	ALTER TABLE weather_data
	ADD COLUMN visibility DECIMAL(5,2);


CREATE TABLE search_filter_history (
    filter_id SERIAL PRIMARY KEY,

    search_id INTEGER NOT NULL,

    user_id INTEGER NOT NULL,

    filter_name VARCHAR(100),

    filter_value VARCHAR(255),

    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_filter_search
        FOREIGN KEY (search_id)
        REFERENCES searches(search_id),

    CONSTRAINT fk_filter_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE saved_trips (
    trip_id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,

    flight_id INTEGER,
    hotel_id INTEGER,

    trip_name VARCHAR(255),

    trip_score DECIMAL(3,1),

    estimated_budget NUMERIC(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_trip_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_trip_flight
        FOREIGN KEY (flight_id)
        REFERENCES flights(flight_id),

    CONSTRAINT fk_trip_hotel
        FOREIGN KEY (hotel_id)
        REFERENCES hotels(hotel_id)
);

/*Contact */
CREATE TABLE contact_messages (

    contact_id SERIAL PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(150) NOT NULL,

    category VARCHAR(50) NOT NULL,

    message TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

CREATE TABLE target_trips(
               target_trip_id SERIAL PRIMARY KEY,
			   user_id INTEGER NOT NULL,
			   origin VARCHAR(200) NOT NULL,
			   destination VARCHAR(200) NOT NULL,

			   travelers INTEGER NOT NULL DEFAULT 1
                 CHECK (travelers >= 1),
               travel_class VARCHAR(30) NOT NULL
                    CHECK (
				            travel_class IN (
				                'economy',
				                'premium_economy',
				                'business',
				                'first'
				            )
				        ),

			    start_month SMALLINT NOT NULL
			        CHECK (start_month BETWEEN 1 AND 12),
			
			    end_month SMALLINT NOT NULL
			        CHECK (end_month BETWEEN 1 AND 12),
			
			    travel_year INTEGER NOT NULL,

			    flight_min_price NUMERIC(10,2) NOT NULL
			        CHECK (flight_min_price >= 0),
			
			    flight_max_price NUMERIC(10,2) NOT NULL
			        CHECK (flight_max_price >= flight_min_price),
			
			    hotel_min_price NUMERIC(10,2) NOT NULL
			        CHECK (hotel_min_price >= 0),
			
			    hotel_max_price NUMERIC(10,2) NOT NULL
			        CHECK (hotel_max_price >= hotel_min_price),

			    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
			        CHECK (
			            status IN (
			                'ACTIVE',
			                'COMPLETED',
			                'ARCHIVED'
			            )
			        ),

			    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			
			    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			
			    CONSTRAINT fk_target_trip_user
			        FOREIGN KEY (user_id)
			        REFERENCES users(user_id)
			        ON DELETE CASCADE
);



                           