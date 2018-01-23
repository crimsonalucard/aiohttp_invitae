from typing import Any

from aiohttp import web
from aiohttp.web_request import Request
from asyncpg.protocol.protocol import Record

from utils import generic_conversion_view_decorator_factory, python_to_json_response, psql_to_python, \
    handle_none_view_decorator, execute_sql
from server.cache import cache_json

decorated_routes = web.RouteTableDef()


@cache_json
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(psql_to_python)
@handle_none_view_decorator(list)
async def search_for_gene(request: Request) -> Record:
    gene: str = request.query.get('gene', '').upper()
    # limit: int = int(request.query.get('limit', '10'))
    # offset: int = int(request.query.get('offset', '0'))
    # sql_string: str = "SELECT * FROM variants WHERE gene = $1 LIMIT $2 OFFSET $3;"
    # remove offsets from gene search because no time to implement front end pagination.
    sql_string: str = "SELECT * FROM variants WHERE gene = $1"
    if len(gene) > 0:
        result: Record = await execute_sql(request, sql_string, gene)
    else:
        result = None
    return result


@cache_json
@generic_conversion_view_decorator_factory(python_to_json_response)
@generic_conversion_view_decorator_factory(psql_to_python)
@handle_none_view_decorator(list)
async def word_suggestion(request: Request) -> Record:
    word: str = request.query.get('word', '').upper()
    limit: int = int(request.query.get('limit', '10'))
    offset: int = int(request.query.get('offset', '0'))
    sql_string: str = "SELECT DISTINCT gene AS suggestion FROM variants WHERE gene LIKE $1||'%' LIMIT $2 OFFSET $3"
    if len(word) > 0:
        result: Record = await execute_sql(request, sql_string, word, limit, offset)
    else:
        result = None
    return result
