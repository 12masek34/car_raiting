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

    async def add_document(self, user_id: int, document_id: str | None, photo_id: str | None) -> None:
        async with self.pool.acquire() as con:
            async with con.transaction():
                await con.execute(queries.insert_document, user_id, document_id, photo_id)
        config.log.info(f" добавлен документ user_id={user_id} document_id={document_id} photo_id={photo_id}")

    async def get_documents(self, user_id: int) -> tuple[set, set]:
        pics = set()
        docs = set()
        async with self.pool.acquire() as con:
            async with con.transaction():
                pics_and_docs = await con.fetch(queries.select_documents, user_id)

                if pics_and_docs:
                    pics.update(pics_and_docs[0][0])
                    docs.update(pics_and_docs[0][1])

                    if None in pics:
                        pics.remove(None)

                    if None in docs:
                        docs.remove(None)

        config.log.info(f" Для пользователя user_id={user_id} получено {len(docs)} документов и {len(pics)} фото")

        return pics, docs

    async def get_summary(self, user_id: int):
        async with self.pool.acquire() as con:
            async with con.transaction():
                summary = await con.fetchrow(queries.select_summary, user_id)
                config.log.info(f" Для пользователя user_id={user_id} получено {summary}")

                return summary


async def init_db() -> Db:
    db = Db()
    await db.init_pool()

    async with db.pool.acquire() as con:
        async with con.transaction():
            await con.execute(queries.create_cars)

    return db
