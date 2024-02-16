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

insert_car = """
    INSERT INTO cars (user_id) values ($1)
"""

insert_restriction = """
UPDATE cars SET restriction = $2
WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""