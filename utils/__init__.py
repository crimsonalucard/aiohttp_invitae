import json
from typing import List, Dict, Any

from aiohttp import web
from aiohttp.web_response import Response
from asyncpg.protocol.protocol import Record


def psql_to_python(psql_result: Record) -> List[Dict[str, Any]]:
    return [dict(i) for i in psql_result]


def python_to_json_response(python_input: Any) -> Response:
    return web.json_response(python_input, dumps=lambda x: json.dumps(x, default=str))


def bytes_to_string(input_bytes: bytes) -> str:
    return input_bytes.decode("utf-8")


def json_string_to_python(json_str: str) -> Any:
    return json.loads(json_str)