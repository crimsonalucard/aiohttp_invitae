import aiohttp
import aioredis
import asyncpg
from aiohttp import web

from settings import SESSION, PG_CONNECTION_STRING, PG_POOL, REDIS_CONNECTION_STRING, REDIS_CONNECTION

#IO
async def startup(app: web.Application) -> None:
    await connect_pg(app)
    await connect_redis(app)
    create_session(app)


def create_session(app: web.Application) -> aiohttp.ClientSession:
    app[SESSION] = aiohttp.ClientSession(loop=app.loop)
    return app[SESSION]


async def connect_pg(app: web.Application) -> None:
    pg_pool = await asyncpg.create_pool(PG_CONNECTION_STRING, loop=app.loop)
    app[PG_POOL] = pg_pool


async def connect_redis(app: web.Application) -> None:
    redis_connection = await aioredis.create_pool(REDIS_CONNECTION_STRING, loop=app.loop)
    app[REDIS_CONNECTION] = redis_connection


async def cleanup(app: web.Application) -> None:
    await close_pg(app)
    await close_redis(app)
    await close_session(app)


async def close_pg(app: web.Application) -> None:
    await app['pg_connections'].close()


async def close_redis(app: web.Application) -> None:
    app[REDIS_CONNECTION].close()
    await app[REDIS_CONNECTION].wait_closed()


async def close_session(app: web.Application) -> None:
    await app[SESSION].close()