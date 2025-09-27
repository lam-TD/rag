import hashlib
from typing import Annotated
from pathlib import Path
from fastapi import APIRouter, File, Depends, Path as PathParams, UploadFile
from sqlmodel import Session, select

from app.models.files import Files, FileCreate

from app.core.database import get_session
from app.schemas.files import FileIn

router = APIRouter(tags=["Files"], prefix="/api/v1/files")

UPLOAD_PATH = Path("/uploads")
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)


@router.get("")
async def read_files(db: Annotated[Session, Depends(get_session)]):

    files = db.exec(select(Files)).all()
    return {"files": files}


@router.post("")
async def upload_file(
    file: Annotated[UploadFile, File],
    db: Annotated[Session, Depends(get_session)],
    payload: Annotated[FileIn, Depends(FileIn.as_form)],
):
    content = await file.read()
    sha = hashlib.sha256(content).hexdigest()
    filename = file.filename

    if filename is None:
        return {"error": "Filename is required."}

    file_path = UPLOAD_PATH / filename
    with open(file_path, "wb") as f:
        f.write(content)

    file_data = FileCreate(
        name=filename,
        size=len(content),
        note=payload.note,
        sha256=sha,
        storage_path=str(file_path),
        mime_type=file.content_type or "application/octet-stream",
    )

    file_record = Files.model_validate(file_data)

    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    return {"file": file_record}


@router.post("/{file_id}/summary")
async def get_file_summary(
    file_id: Annotated[int, PathParams(description="The ID of the file to summarize")],
    db: Annotated[Session, Depends(get_session)],
):
    file = db.get(Files, file_id)
    if not file:
        return {"error": "File not found."}
    return {"summary": "This is a summary", "file": file}
