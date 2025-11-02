from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Any, Dict, Optional, Type, TypeVar

import httpx

from .models import APIErrorPayload, FilesResponse, SummaryResponse, UploadResponse

T = TypeVar("T")


class RagAPIError(RuntimeError):
    """Raised when the API returns a non-successful response."""

    def __init__(self, message: str, status_code: Optional[int] = None, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class RagAPIClient:
    def __init__(self, base_url: str, timeout: float = 15.0):
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "RagAPIClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def list_files(self) -> FilesResponse:
        response = self._client.get("/api/v1/files")
        return self._parse_response(response, FilesResponse)

    def upload_file(self, file_path: Path, note: Optional[str] = None) -> UploadResponse:
        if not file_path.exists():
            raise FileNotFoundError(f"No such file: {file_path}")

        mime_type, _ = mimetypes.guess_type(str(file_path))
        data: Dict[str, Optional[str]] = {}
        if note is not None:
            data["note"] = note

        with file_path.open("rb") as buffer:
            files = {"file": (file_path.name, buffer, mime_type or "application/octet-stream")}
            response = self._client.post("/api/v1/files", data=data, files=files)

        return self._parse_response(response, UploadResponse)

    def summarise_file(self, file_id: int) -> SummaryResponse:
        response = self._client.post(f"/api/v1/files/{file_id}/summary")
        return self._parse_response(response, SummaryResponse)

    def _parse_response(self, response: httpx.Response, model: Type[T]) -> T:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            payload = None
            try:
                payload = APIErrorPayload.model_validate(exc.response.json())
            except Exception:  # noqa: BLE001
                payload = None
            message = payload.error if isinstance(payload, APIErrorPayload) and payload.error else str(exc)
            raise RagAPIError(message, status_code=exc.response.status_code, payload=payload) from exc

        data = response.json()
        return model.model_validate(data)

