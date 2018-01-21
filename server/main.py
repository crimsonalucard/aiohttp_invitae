#! /usr/bin/env python3

import asyncio
from aiohttp import web

# settings
from server.bootstrap import startup, cleanup
from server.cors import add_cors_to_all_routes
from server.views import decorated_routes
from server.routes import routes

# https://magic.io/blog/uvloop-blazing-fast-python-networking/
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app: web.Application = web.Application()
app.on_startup.append(startup)
app.on_cleanup.append(cleanup)
app.router.add_routes(decorated_routes)
app.router.add_routes(routes)
add_cors_to_all_routes(app)

if __name__ == "__main__":
    web.run_app(app, port=1337)
