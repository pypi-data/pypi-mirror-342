import typing

from starlette import _exception_handler
from starlette._exception_handler import ExceptionHandlers, StatusHandlers, \
    _lookup_exception_handler
from starlette._utils import is_async_callable
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send, Message, HTTPExceptionHandler, WebSocketExceptionHandler
from starlette.websockets import WebSocket

RASHandler = typing.Callable[
    [BaseException, Request | WebSocket], typing.Coroutine[typing.Any, typing.Any, None]
]


def build_patch(ras_handler: RASHandler):
    def wrap_app_handling_exceptions_patch(app: ASGIApp, conn: Request | WebSocket) -> ASGIApp:
        exception_handlers: ExceptionHandlers
        status_handlers: StatusHandlers
        try:
            exception_handlers, status_handlers = conn.scope["starlette.exception_handlers"]
        except KeyError:
            exception_handlers, status_handlers = {}, {}

        async def wrapped_app(scope: Scope, receive: Receive, send: Send) -> None:
            response_started = False

            async def sender(message: Message) -> None:
                nonlocal response_started

                if message["type"] == "http.response.start":
                    response_started = True
                await send(message)

            try:
                await app(scope, receive, sender)
            except Exception as exc:
                nonlocal conn
                handler = None

                if isinstance(exc, HTTPException):
                    handler = status_handlers.get(exc.status_code)

                if handler is None:
                    handler = _lookup_exception_handler(exception_handlers, exc)

                if handler is None:
                    raise exc

                if response_started:
                    await ras_handler(exc, conn) # type: ignore[used-before-def]
                    return

                if scope["type"] == "http":
                    handler = typing.cast(HTTPExceptionHandler, handler)
                    conn = typing.cast(Request, conn)
                    if is_async_callable(handler):
                        response = await handler(conn, exc)
                    else:
                        response = await run_in_threadpool(handler, conn, exc)
                    await response(scope, receive, sender)
                elif scope["type"] == "websocket":
                    handler = typing.cast(WebSocketExceptionHandler, handler)
                    conn = typing.cast(WebSocket, conn)
                    if is_async_callable(handler):
                        await handler(conn, exc)
                    else:
                        await run_in_threadpool(handler, conn, exc)

        return wrapped_app
    return wrap_app_handling_exceptions_patch

def handle_starlette_ras(handler: RASHandler) -> None:
    _exception_handler.wrap_app_handling_exceptions = build_patch(handler)