create_cars = """
    CREATE TABLE IF NOT EXISTS cars (
        id SERIAL PRIMARY KEY,
        user_id INTEGER,
        restriction BOOLEAN default null,
        number_of_keys INTEGER,
        tire VARCHAR(255),
        drive_type VARCHAR(255),
        photo_ids INTEGER[]
    );
"""