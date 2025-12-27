import uuid
from typing import Any

from pydantic import BaseModel


class EmbeddingItem(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    collection_id: uuid.UUID
    content: str
    similarity: float
    cmetadata: dict[str, Any]

    model_config = {
        "extra": "forbid",
        "from_attributes": True,
    }
