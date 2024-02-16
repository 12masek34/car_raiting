import asyncpg
import config


class Db:
    def __init__(self):
        self.pool = None

    async def init_pool(self):
        self.pool = await asyncpg.create_pool(
                database=config.DATABASE,
                user=config.USER,
                host=config.HOST,
                password=config.PASSWORD,
            )


async def init_db():
    db = Db()
    await db.init_pool()
    async with db.pool.acquire() as con:
        async with con.transaction():
            await con.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER,
                    restriction BOOLEAN default null,
                    number_of_keys INTEGER,
                    tire VARCHAR(255),
                    drive_type VARCHAR(255),
                    photo_ids INTEGER[]
                );
            """)
    return db
