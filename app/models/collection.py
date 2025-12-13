from datetime import datetime, timezone
from typing import Any
import uuid
from sqlalchemy import JSON, UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column
from app.services.db.base_model import BaseModel


class Collection(BaseModel):
    __tablename__ = "collections"
    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        unique=True, index=True, max_length=255, nullable=False
    )
    embedding_model: Mapped[str] = mapped_column(max_length=255, nullable=False)
    embedding_dimension: Mapped[int] = mapped_column(default=1024, nullable=False)
    distance_metric: Mapped[str] = mapped_column(
        default="cosine", max_length=50, nullable=False
    )
    cmetadata: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )
