from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class FileRecord(BaseModel):
    id: int
    name: str
    size: int
    note: Optional[str] = None
    sha256: Optional[str] = None
    storage_path: Optional[str] = None
    mime_type: Optional[str] = None


class FilesResponse(BaseModel):
    files: List[FileRecord]


class UploadResponse(BaseModel):
    file: FileRecord


class SummaryResponse(BaseModel):
    summary: List[str]


class APIErrorPayload(BaseModel):
    error: Optional[str] = None
    detail: Optional[Any] = None

