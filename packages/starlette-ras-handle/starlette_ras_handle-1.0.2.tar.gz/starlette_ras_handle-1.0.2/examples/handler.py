from starlette.requests import Request
from starlette.websockets import WebSocket


async def print_handler(exc: Exception, request: Request | WebSocket) -> None:
    print("Caught", exc)