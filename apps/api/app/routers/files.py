from typing import Annotated
from pathlib import Path
from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)


from app.services.text_extractor.tika_extractor import TikaExtractor

router = APIRouter(tags=["Files"], prefix="/api/v1/files")

UPLOAD_PATH = Path("/uploads")
UPLOAD_PATH.mkdir(parents=True, exist_ok=True)


@router.post("")
async def upload_file(
    file: Annotated[UploadFile, File],
):
    content = await file.read()

    try:
        tika_extractor = TikaExtractor(base_url="http://tika:9998")
        text = await tika_extractor.extract(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"file_content": text}
