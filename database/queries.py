create_cars = """
    CREATE TABLE IF NOT EXISTS cars (
        id BIGSERIAL PRIMARY KEY,
        user_id INTEGER,
        restriction BOOLEAN default null,
        number_of_keys INTEGER,
        tire VARCHAR(255),
        drive_type VARCHAR(255),
        photo_ids TEXT[],
        document_ids TEXT[]
    );
"""

insert_car = """
    INSERT INTO cars (user_id) values ($1) RETURNING id
"""

insert_restriction = """
    UPDATE cars SET restriction = $2
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""
insert_number_of_keys = """
    UPDATE cars SET number_of_keys = $2
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

insert_tire = """
    UPDATE cars SET tire = $2
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

insert_drive_type = """
    UPDATE cars SET drive_type = $2
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

insert_document = """
    UPDATE cars
    SET document_ids = array_append(document_ids, $2),
    photo_ids = array_append(photo_ids, $3)
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

select_documents = """
    SELECT photo_ids, document_ids FROM cars
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""

select_summary = """
    SELECT restriction, number_of_keys, tire, drive_type FROM cars
    WHERE id = (SELECT id FROM cars WHERE user_id = $1 ORDER BY id DESC LIMIT 1)
"""
