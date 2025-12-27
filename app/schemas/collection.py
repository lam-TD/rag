from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CollectionItemReponse(BaseModel):
    id: uuid.UUID
    name: str
    embedding_model: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "extra": "forbid",
        "from_attributes": True,
    }


class CollectionCreateRequest(BaseModel):
    name: str
    embedding_model: str
    cmetadata: dict[str, Any] | None = Field(default=None)

    model_config = {
        "extra": "forbid",
        "from_attributes": True,
    }


class CollectionChatRequet(BaseModel):
    question: str = Field(max_length=1000)
    top_k: float = Field(default=0.7)


class CollectionChatReponse(CollectionChatRequet):
    answer: str
    context: list[Any]
