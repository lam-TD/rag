from __future__ import annotations

from typing import Any, Protocol, TypedDict


class ChunkDict(TypedDict, total=False):
    """
    Cấu trúc dữ liệu cho một chunk văn bản.
    - Bắt buộc: text, doc_id, page
    - Tuỳ chọn: embedding, metadata
    """

    text: str
    doc_id: str
    page: int
    embedding: list[float]
    metadata: dict[str, Any]


class Repository(Protocol):
    """Giao diện lưu trữ (ví dụ: bulk insert vào DB)."""

    def bulk_insert(self, rows: list[ChunkDict]) -> None:
        """Ghi hàng loạt các chunk (có thể kèm embedding) vào kho lưu trữ."""
        ...
