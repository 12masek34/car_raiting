import asyncpg
import config
from database import queries


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
            await con.execute(queries.create_cars)

    return db
