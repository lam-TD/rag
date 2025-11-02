import chunk
from typing import Annotated
from fastapi import APIRouter, Depends, File, Path, Path
from sqlmodel import Session

from app.core.database import get_session
from app.core.document_loader import split_document
from app.models.files import Files

router = APIRouter(tags=["Summaries"], prefix="/api/v1/summaries")


@router.get("/{file_id}")
async def create_summary(
    file_id: Annotated[str, Path], db: Annotated[Session, Depends(get_session)]
) -> dict:
    file = db.get(Files, file_id)
    if not file:
        return {"error": "File not found"}

    chunks = split_document(str(file.storage_path))
    return {"summary": chunks}
