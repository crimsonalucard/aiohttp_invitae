from typing import Any

from aiohttp import web
from aiohttp.web_request import Request
from asyncpg.protocol.protocol import Record

from client import fetch
from settings import REDIS_CONNECTION, SESSION
from utils import generic_conversion_view_decorator_factory, python_to_json_response, psql_to_python, \
    handle_none_view_decorator, execute_sql, bytes_to_string, json_string_to_python

decorated_routes = web.RouteTableDef()

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


@decorated_routes.post('/redis/')
@generic_conversion_view_decorator_factory(python_to_json_response)
async def set_redis(request: Request) -> Any:
    post_params = await request.post()
    await request.app[REDIS_CONNECTION].execute('set', post_params.get('key'), post_params.get('value'))
    return {'message': 'successfully inserted key into redis'}


@decorated_routes.get('/redis/')
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(bytes_to_string)
@handle_none_view_decorator(bytes)
async def get_redis(request: Request) -> bytes:
    key = request.query.get('key')
    result: bytes = await request.app[REDIS_CONNECTION].execute('get', key)
    return result


@decorated_routes.get('/request/')
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(json_string_to_python)
@handle_none_view_decorator(str)
async def request_test(_: Request) -> str:
    root = 'https://jsonplaceholder.typicode.com/posts/1'
    result: str = await fetch(app[SESSION], root)
    return result


