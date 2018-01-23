from aiohttp.web import Request, Response
from typing import Callable, Any, Coroutine, Awaitable
from settings import REDIS_CONNECTION, CACHE_EXPIRE_TIME


def cache_json(view_func: Callable[[Request], Response]) -> Callable[
    [Request], Response]:
    async def inner(request: Request) -> Response:
        key: str = request.path_qs
        key_exists: int = await request.app[REDIS_CONNECTION].execute('EXISTS', key)
        key_exists = True if key_exists == 1 else False
        if key_exists:
            cached_results: bytes = await request.app[REDIS_CONNECTION].execute('GET', key)
            response: Response = Response(body=cached_results, content_type='application/json')
        else:
            #mypy throws an error here if I add a type to response. Otherwise pycharm throws an error
            #for consistency sake I'm going with mypy
            response = await view_func(request)
            await request.app[REDIS_CONNECTION].execute('SET', key, response.body)
            await request.app[REDIS_CONNECTION].execute('EXPIRE', key, CACHE_EXPIRE_TIME)
        return response

    return inner #pycharm returns a type error here but mypy doesn't.. going with mypy
