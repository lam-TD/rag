from __future__ import annotations
from datetime import datetime
from typing import Any
import uuid
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
