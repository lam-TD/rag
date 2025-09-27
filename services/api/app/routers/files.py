from typing import Annotated

from fastapi import APIRouter, File, Depends, UploadFile
from sqlmodel import Session, select

from app.models.files import Files, FileCreate

from app.core.database import get_session
from app.schemas.files import FileIn

router = APIRouter(tags=["Files"], prefix="/api/v1/files")


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
    filename = file.filename
    if filename is None:
        return {"error": "Filename is required."}

    file_data = FileCreate(name=filename, size=len(content), note=payload.note)
    file_record = Files.model_validate(file_data)
    db.add(file_record)
    db.commit()
    db.refresh(file_record)
    return {"file": file_record}
