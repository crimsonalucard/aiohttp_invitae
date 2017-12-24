import json

from aiohttp import web


def psql_python_view_decorator(handler):
    async def inner(request):
        result = await handler(request)
        return [dict(i) for i in result]

    return inner


def python_to_json_response_view_decorator(handler):
    async def inner(request):
        result = await handler(request)
        return web.json_response(result, dumps=lambda x: json.dumps(x, default=str))

    return inner


def bytes_to_string_view_decorator(handler):
    async def inner(request):
        result = await handler(request)
        return result.decode("utf-8")

    return inner


def json_string_to_python_view_decorator(handler):
    async def inner(request):
        result = await handler(request)
        return json.loads(result)

    return inner
