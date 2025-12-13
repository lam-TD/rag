from __future__ import annotations

from typing import Any, Protocol

from app.schemas.rag import EmbeddingResponse


class EmbeddingServiceProtocol(Protocol):
    async def embed_texts(
        self,
        texts: list[str],
        model: str,
        *,
        metadata: dict[str, Any] | None = None,
        encoding_format: str = "float",
    ) -> EmbeddingResponse:
        """Return embeddings for list of texts."""
