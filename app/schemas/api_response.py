from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ApiMeta(BaseModel):
    request_id: str
    timestamp: datetime


class ApiError(BaseModel):
    code: str
    message: str
    details: dict[str, Any] | None = None


class Pagination(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=200)
    total: int = Field(ge=0)
    has_next: bool


class ApiResponse[T](BaseModel):
    success: bool = False
    data: T | None = None
    error: ApiError | None = None
    pagination: Pagination | None = None

    model_config = {
        "extra": "forbid",
    }

    @classmethod
    def ok(cls, *, data: T, pagination: Pagination | None = None) -> ApiResponse[T]:
        return cls(
            success=True,
            data=data,
            error=None,
            pagination=pagination,
        )

    @classmethod
    def fail(
        cls,
        *,
        code: str,
        message: str,
        request_id: str,
        details: dict[str, Any] | None = None,
    ) -> ApiResponse[None]:
        return cls(
            success=False,
            data=None,
            error=ApiError(code=code, message=message, details=details),
        )
