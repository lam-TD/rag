from __future__ import annotations

from typing import Any, Optional

import httpx
from pydantic import BaseModel

from app.schemas.rag import EmbeddingItem, EmbeddingResponse, EmbeddingUsage
from app.services.embedding_protocols import EmbeddingServiceProtocol


class LocalEmbeddingClientConfig(BaseModel):
    base_url: str
    api_key: str = ""
    timeout_seconds: float = 30.0


class LocalEmbeddingService(EmbeddingServiceProtocol):
    """EmbeddingService cho server local (tự build hoặc open-source)."""

    def __init__(self, config: LocalEmbeddingClientConfig) -> None:
        self._config = config

    async def embed_texts(
        self,
        texts: list[str],
        model: str,
        *,
        metadata: Optional[dict[str, Any]] = None,
        encoding_format: str = "float",
    ) -> EmbeddingResponse:
        # Tùy bạn định nghĩa API local, đây là ví dụ generic
        payload = {
            "texts": texts,
            "model": model,
            "metadata": metadata or {},
            "encoding_format": encoding_format,
        }

        async with httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout_seconds,
        ) as client:
            response = await client.post("/embeddings", json=payload)
            response.raise_for_status()
            raw = response.json()

        vectors = raw.get("embeddings", [])
        items: list[EmbeddingItem] = []

        for index, vector in enumerate(vectors):
            items.append(
                EmbeddingItem(
                    index=index,
                    embedding=vector,
                    embedding_id=None,
                    metadata=metadata or {},
                )
            )

        dimension = 0
        if items and items[0].embedding is not None:
            dimension = len(items[0].embedding)

        usage = EmbeddingUsage(
            prompt_tokens=None,
            total_tokens=None,
        )

        return EmbeddingResponse(
            model=model,
            dimension=dimension,
            data=items,
            usage=usage,
            trace_id=None,
        )
