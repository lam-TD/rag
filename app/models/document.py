import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, ForeignKey
from sqlalchemy import UUID as SQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.services.db.base_model import BaseModel


class Document(BaseModel):
    __tablename__ = "documents"
    id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True), default=uuid.uuid4, primary_key=True
    )
    collection_id: Mapped[uuid.UUID] = mapped_column(
        SQLUUID(as_uuid=True),
        nullable=False,
        foreign_key=ForeignKey("collections.id", ondelete="CASCADE"),
    )
    cmetadata: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC), onupdate=datetime.now(UTC)
    )
