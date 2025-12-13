from __future__ import annotations

import json
from typing import Any, Optional

from fastapi import Form, HTTPException
from pydantic import BaseModel, Field


DEFAULT_COLLECTION_NAME = "default"
DEFAULT_EMBEDDING_MODEL = "jina-embeddings-v3"


class EmbeddingRequest(BaseModel):
    model: Optional[str] = Field(
        DEFAULT_EMBEDDING_MODEL,
        description="Embedding model name, e.g. 'jina-embeddings-v3'",
        examples=[DEFAULT_EMBEDDING_MODEL],
    )
    metadata: dict[str, Any] | None = Field(
        default=None,
        description="Metadata dạng JSON (key/value) gắn kèm cho toàn bộ batch",
    )

    @classmethod
    def as_form(
        cls,
        model: Optional[str] = Form(DEFAULT_EMBEDDING_MODEL),
        metadata: Optional[str] = Form(
            "{}",
            description="Metadata dạng JSON (key/value) gắn kèm cho toàn bộ batch",
        ),
    ):
        parsed_metadata: dict[str, Any] | None = None
        if metadata:
            try:
                parsed_metadata = json.loads(metadata)
                if not isinstance(parsed_metadata, dict):
                    raise ValueError("metadata must be a JSON object")
            except (json.JSONDecodeError, ValueError):
                raise HTTPException(
                    status_code=422,
                    detail="metadata must be a valid JSON object",
                )

        return cls(model=model, metadata=parsed_metadata)


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
