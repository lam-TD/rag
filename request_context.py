from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass, replace
from typing import Iterator, Optional


@dataclass(frozen=True, slots=True)
class RequestContext:
    trace_id: str
    tenant_id: Optional[str] = None
    request_id: Optional[str] = None
    user_id: Optional[str] = None


# Nguồn sự thật chính cho toàn bộ request context
_request_context: ContextVar[RequestContext | None] = ContextVar(
    "request_context",
    default=None,
)


def get_current_context() -> RequestContext | None:
    return _request_context.get()


def require_current_context() -> RequestContext:
    ctx = _request_context.get()
    if ctx is None:
        raise RuntimeError("RequestContext is not available in the current execution context.")
    return ctx


@contextmanager
def use_request_context(ctx: RequestContext) -> Iterator[RequestContext]:
    """
    Đặt context mới trong phạm vi `with`, sau đó reset lại an toàn.
    Hợp với Python 3.12+.
    """
    token: Token = _request_context.set(ctx)
    try:
        yield ctx
    finally:
        _request_context.reset(token)


@contextmanager
def override_request_context(**changes) -> Iterator[RequestContext]:
    """
    Cập nhật tạm thời một phần context hiện tại.
    Ví dụ: thêm user_id sau khi auth xong.
    """
    current = require_current_context()
    updated = replace(current, **changes)
    token: Token = _request_context.set(updated)
    try:
        yield updated
    finally:
        _request_context.reset(token)
        
from __future__ import annotations

import uuid
from typing import Callable, Awaitable

from starlette.types import ASGIApp, Scope, Receive, Send, Message

from .request_context import RequestContext, use_request_context


class RequestContextMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = {
            k.decode("latin-1").lower(): v.decode("latin-1")
            for k, v in scope.get("headers", [])
        }

        trace_id = headers.get("x-trace-id") or str(uuid.uuid4())
        tenant_id = headers.get("x-tenant-id")
        request_id = headers.get("x-request-id") or trace_id

        ctx = RequestContext(
            trace_id=trace_id,
            tenant_id=tenant_id,
            request_id=request_id,
        )

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                raw_headers = list(message.get("headers", []))
                raw_headers.append((b"x-trace-id", trace_id.encode("latin-1")))
                message["headers"] = raw_headers
            await send(message)

        with use_request_context(ctx):
            await self.app(scope, receive, send_wrapper)