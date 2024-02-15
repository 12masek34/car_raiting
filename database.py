from asyncio import AbstractEventLoop, get_event_loop
import asyncpg
import config



class Db:
    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop
        self.pool = self.loop.run_until_complete(
            asyncpg.create_pool(
                database=config.DATABASE,
                user=config.USER,
                host=config.HOST,
                password=config.PASSWORD,
            )
        )


loop = get_event_loop()
db = Db(loop)
