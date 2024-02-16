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

    async def add_car(self, user_id: int) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_car, user_id)
        config.log.info(f" создана запись user_id={user_id}")

    async def add_restriction(self, user_id: int, resriction: bool) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_restriction, user_id, resriction)
        config.log.info(f" добавлено ограничение user_id={user_id} ограничение={resriction}")

    async def add_number_of_keys(self, user_id: int, number_of_keys: int | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_number_of_keys, user_id, number_of_keys)
        config.log.info(f" добавлено количество user_id={user_id} ключей={number_of_keys}")

    async def add_tire(self, user_id: int, tire: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_tire, user_id, tire)
        config.log.info(f" добавлена резина user_id={user_id} резина={tire}")

    async def add_drive_type(self, user_id: int, drive_type: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_drive_type, user_id, drive_type)
        config.log.info(f" добавлен привод user_id={user_id} привод={drive_type}")


async def init_db() -> Db:
    db = Db()
    await db.init_pool()

    async with db.pool.acquire() as con:
        async with con.transaction():
            await con.execute(queries.create_cars)

    return db
