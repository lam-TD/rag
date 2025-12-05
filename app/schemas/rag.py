from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    input: list[str] = Field(..., min_items=1)
    model: str = Field(..., description="Embedding model name, e.g. 'jina-embeddings-v3'")
    encoding_format: Literal["float", "none"] = "float"
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmbeddingItem(BaseModel):
    index: int
    embedding_id: Optional[str] = None
    embedding: Optional[list[float]] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class EmbeddingUsage(BaseModel):
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class EmbeddingResponse(BaseModel):
    model: str
    dimension: int
    data: list[EmbeddingItem]
    usage: Optional[EmbeddingUsage] = None
    trace_id: Optional[str] = None