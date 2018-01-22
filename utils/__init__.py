import json
from typing import List, Dict, Any, Callable, Union

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from asyncpg.protocol.protocol import Record

from settings import PG_POOL


def psql_to_python(psql_result: Record) -> List[Dict[str, Any]]:
    return [dict(i) for i in psql_result]


def python_to_json_response(python_input: Any) -> Response:
    return web.json_response(python_input, dumps=lambda x: json.dumps(x, default=str))


def bytes_to_string(input_bytes: bytes) -> str:
    return input_bytes.decode("utf-8")


def json_string_to_python(json_str: str) -> Any:
    return json.loads(json_str)


def generic_conversion_view_decorator_factory(converter_function: Callable[[Any], Any]) -> Callable[
    [Callable[[Request], Any]], Callable[[Request], Any]]:
    def decorator(view_function: Callable[[Request], Any]) -> Callable[[Request], Any]:
        async def inner(request: Request) -> Any:
            result: Any = await view_function(request)
            return converter_function(result)

        return inner

    return decorator


def handle_none_view_decorator(identity_type: Callable[..., Any]) -> Callable[
    [Callable[[Request], Any]], Callable[[Request], Any]]:
    def _handle_none_view_decorator(view_function: Callable[[Request], Any]) -> Callable[[Request], Any]:
        async def inner(request: Request) -> Any:
            result = await view_function(request)
            if result is None:
                return identity_type()
            else:
                return result

        return inner

    return _handle_none_view_decorator


async def execute_sql(request: Request, sql_string: str, *params: Union[str, int]) -> Record:
    async with request.app[PG_POOL].acquire() as connection:
        result: Record = await connection.fetch(sql_string, *params)
    return result


def concat_sequence(*args):
    for seq in args:
        yield from seq
