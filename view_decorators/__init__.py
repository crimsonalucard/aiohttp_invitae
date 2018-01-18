from typing import Callable, Any, Dict, List
from aiohttp.web import Request
from asyncpg import Record

from utils import psql_to_python, python_to_json_response, bytes_to_string, json_string_to_python


def generic_conversion_view_decorator_factory(converter_function: Callable[[Any], Any]) -> Callable[
    [Callable[[Request], Any]], Callable[[Request], Any]]:
    def decorator(view_function: Callable[[Request], Any]) -> Callable[[Request], Any]:
        async def inner(request: Request) -> Any:
            result: Any = await view_function(request)
            return converter_function(result)

        return inner

    return decorator


def psql_python_view_decorator(view_function: Callable[[Request], Record]) -> Callable[[Request], List[Dict[str, Any]]]:
    return generic_conversion_view_decorator_factory(psql_to_python)(view_function)


def python_to_json_response_view_decorator(view_function: Callable[[Request], Any]) -> Callable[[Request], str]:
    return generic_conversion_view_decorator_factory(python_to_json_response)(view_function)


def bytes_to_string_view_decorator(view_function: Callable[[Request], bytes]) -> Callable[[Request], str]:
    return generic_conversion_view_decorator_factory(bytes_to_string)(view_function)


def json_string_to_python_view_decorator(view_function: Callable[[Request], str]) -> Callable[[Request], Any]:
    return generic_conversion_view_decorator_factory(json_string_to_python)(view_function)


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
