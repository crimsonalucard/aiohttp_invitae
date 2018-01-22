from aiohttp.web import Request, Response
from typing import Callable, Any, Coroutine
from settings import REDIS_CONNECTION, CACHE_EXPIRE_TIME


def cache_json(view_func: Callable[[Request], Coroutine[Any, Any, Response]]) -> Callable[
    [Request], Coroutine[Any, Any, Response]]:
    async def inner(request: Request) -> Response:
        key: str = request.path_qs
        key_exists: int = await request.app[REDIS_CONNECTION].execute('EXISTS', key)
        key_exists = True if key_exists == 1 else False
        if key_exists:
            cached_results: bytes = await request.app[REDIS_CONNECTION].execute('GET', key)
            response: Response = Response(body=cached_results, content_type='application/json')
        else:
            response: Response = await view_func(request)
            await request.app[REDIS_CONNECTION].execute('SET', key, response.body)
            await request.app[REDIS_CONNECTION].execute('EXPIRE', key, CACHE_EXPIRE_TIME)
        return response

    return inner
