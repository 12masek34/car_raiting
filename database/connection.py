import asyncpg

import config
from database import (
    queries,
)


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

    async def insert_car(self, user_id: int) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_car, user_id)
        config.log.info(f" создана запись user_id={user_id}")

    async def add_restriction(self, user_id: int, resriction: bool) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_restriction, user_id, resriction)
        config.log.info(f" добавлено ограничение user_id={user_id} ограничение={resriction}")


async def init_db() -> Db:
    db = Db()
    await db.init_pool()

    async with db.pool.acquire() as con:
        async with con.transaction():
            await con.execute(queries.create_cars)

    return db
