from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import Iterator

from starlette.requests import Request
from starlette.types import ASGIApp, Scope, Receive, Send


# Context object used to store information bound to the current execution flow.
# For now, it only contains tenant_id, but it can later be extended with
# trace_id, request_id, etc. if needed.
#
# frozen=True:
#   - makes the object immutable after creation
#   - prevents tenant_id from being changed during processing
#
# slots=True:
#   - only allows declared fields
#   - prevents accidental extra attributes from being added
#   - slightly more memory efficient
@dataclass(frozen=True, slots=True)
class RequestContext:
    tenant_id: str | None = None


# ContextVar stores context per current async execution flow.
# Each request gets its own context and does not share it with other requests.
#
# default=RequestContext():
#   - when running outside a request or before context is set,
#     get_current_context() still returns a valid object
_request_context: ContextVar[RequestContext] = ContextVar(
    "request_context",
    default=RequestContext(),
)


def get_current_context() -> RequestContext:
    """
    Return the current execution context.

    This is typically used in services, repositories, logging filters, etc.
    to read tenant_id without passing it manually through many layers.
    """
    return _request_context.get()


@contextmanager
def use_request_context(ctx: RequestContext) -> Iterator[RequestContext]:
    """
    Temporarily set RequestContext for the current execution flow.

    How it works:
    1. Set the new context into ContextVar
    2. Run the code inside the `with` block
    3. Always restore the previous context afterward,
       even if an exception occurs inside the block

    This prevents context from "leaking" into another request or job.
    """
    token: Token = _request_context.set(ctx)
    try:
        yield ctx
    finally:
        _request_context.reset(token)


class RequestContextMiddleware:
    """
    Middleware that creates RequestContext for each HTTP request.

    Purpose:
    - read tenant_id from the request header
    - store tenant_id in ContextVar
    - allow downstream layers to access it via get_current_context()
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Apply this middleware only to HTTP requests.
        # Skip websocket and lifespan events.
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Create a Request object from ASGI scope for easier header access.
        request = Request(scope)

        # Read tenant_id from the request header.
        #
        # Note:
        # - headers must be accessed via request.headers.get(...)
        # - do not use Request(...).get(...), because that is not header access
        tenant_id = request.headers.get("x-tenant-id")

        # Normalize the input:
        # - keep None as None
        # - convert whitespace-only strings into None
        tenant_id = tenant_id.strip() if tenant_id else None
        tenant_id = tenant_id or None

        # Build context for the current request
        ctx = RequestContext(tenant_id=tenant_id)

        # Bind the context to the current execution flow for the whole request lifecycle.
        # Any code running below this middleware can read the context.
        with use_request_context(ctx):
            await self.app(scope, receive, send)