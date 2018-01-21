from aiohttp import web
from typing import List
from server.views import handle

routes: List[web.RouteDef] = [
    web.get('/', handle),
    web.get('/{name}', handle),
    web.get('/postgres/', handle)
]
