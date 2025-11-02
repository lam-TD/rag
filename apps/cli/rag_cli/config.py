import os
from typing import Optional

from pydantic import BaseModel, field_validator

DEFAULT_BASE_URL = "http://localhost:8001"
DEFAULT_TIMEOUT = 15.0
ENV_BASE_URL = "RAG_API_BASE_URL"


class CLISettings(BaseModel):
    base_url: str = DEFAULT_BASE_URL
    timeout: float = DEFAULT_TIMEOUT

    @field_validator("base_url", mode="before")
    @classmethod
    def _normalise_base_url(cls, value: str) -> str:
        if not value:
            return DEFAULT_BASE_URL
        return value.rstrip("/")


def get_settings(
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
) -> CLISettings:
    """Return CLI settings resolved from CLI arguments, env vars, and defaults."""

    resolved_base_url = base_url or os.getenv(ENV_BASE_URL) or DEFAULT_BASE_URL
    resolved_timeout = timeout or DEFAULT_TIMEOUT

    return CLISettings(base_url=resolved_base_url, timeout=resolved_timeout)
