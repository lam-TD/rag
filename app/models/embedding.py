from typing import Any
import uuid
from sqlalchemy import JSON, UUID as SQLUUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.services.db.base_model import BaseModel
from pgvector.sqlalchemy import Vector


class Embedding(BaseModel):
    __tablename__ = "embeddings"
    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    collection_id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
        foreign_key=ForeignKey("collections.id", ondelete="CASCADE"),
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
        foreign_key=ForeignKey("documents.id", ondelete="CASCADE"),
    )
    content: Mapped[str] = mapped_column(nullable=False)
    token_count: Mapped[int] = mapped_column(nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector)
    cmetadata: Mapped[dict[str, Any]] = mapped_column(JSON)
