#! /usr/bin/env python3

import aiohttp
import asyncio
import aiohttp_cors
from aiohttp import web

#utils
from utils import psql_to_python, python_to_json_response, bytes_to_string, json_string_to_python

# types
from aiohttp.web import Request
from asyncpg import Record
from typing import Any

# IO
import asyncpg
import aioredis

# https://magic.io/blog/uvloop-blazing-fast-python-networking/
import uvloop

from view_decorators import psql_python_view_decorator, python_to_json_response_view_decorator, \
    bytes_to_string_view_decorator, json_string_to_python_view_decorator, handle_none_view_decorator, generic_conversion_view_decorator_factory

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


# client code

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    # with async_timeout.timeout(10):
    async with session.get(url) as response:
        return await response.text()


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://python.org')
        print(html)


# uncomment to run main()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())


# server code

# CONSTANTS
PG_CONNECTION_STRING: str = 'postgresql://postgres@localhost/postgres'
PG_POOL: str = 'pg_pool'
REDIS_CONNECTION_STRING: str = 'redis://localhost'
REDIS_CONNECTION: str = 'redis_connection'
SESSION: str = 'session'


# server startup
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


# server cleanup
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


routes = web.RouteTableDef()


async def execute_sql(request: Request, sql_string: str, *params: str) -> Record:
    async with request.app[PG_POOL].acquire() as connection:
        result: Record = await connection.fetch(sql_string, *params)
    return result


# server code
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(psql_to_python)
@handle_none_view_decorator(list)
async def handle(request: Request) -> Record:
    # name = request.match_info.get('name', "Anonymous")
    # text = "Hello, " + name
    # return web.Response(text=text)
    name = request.query.get('name', '*')
    result: Record = await execute_sql(request, 'SELECT * FROM users WHERE name = $1;', name)
    # return web.json_response(result, dumps=date_enabled_json_dumps)
    return result


@routes.post('/redis/')
@generic_conversion_view_decorator_factory(python_to_json_response)
async def set_redis(request: Request) -> Any:
    post_params = await request.post()
    await request.app[REDIS_CONNECTION].execute('set', post_params.get('key'), post_params.get('value'))
    return {'message': 'successfully inserted key into redis'}


@routes.get('/redis/')
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(bytes_to_string)
@handle_none_view_decorator(bytes)
async def get_redis(request: Request) -> bytes:
    key = request.query.get('key')
    result: bytes = await request.app[REDIS_CONNECTION].execute('get', key)
    return result


@routes.get('/request/')
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(json_string_to_python)
@handle_none_view_decorator(str)
async def request_test(_: Request) -> str:
    root = 'https://jsonplaceholder.typicode.com/posts/1'
    result: str = await fetch(app[SESSION], root)
    return result


app = web.Application()

app.on_startup.append(startup)
app.on_cleanup.append(cleanup)
app.router.add_routes(routes)
app.router.add_get('/', handle)
app.router.add_get('/{name}', handle)
app.router.add_get('/postgres/', handle)

# Configure CORS on all routes.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
    )
})
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app, port=1337)
