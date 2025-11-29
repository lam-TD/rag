from typing import Annotated
from pathlib import Path
import uuid
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.config.env import Env, get_env
from app.services.chunking.simple_chunker import SimpleChunker
from app.services.db.pgvector import get_db_session
from app.services.embeddings.jina_service import JinaEmbedding
from app.services.text_extractor.tika_extractor import TikaExtractor

router = APIRouter(tags=["Files"], prefix="/api/v1/files")

# UPLOAD_PATH = Path("/storage/uploads")
# UPLOAD_PATH.mkdir(parents=True, exist_ok=True)


@router.post("")
async def upload_file(
    file: Annotated[UploadFile, File],
    env: Annotated[Env, Depends(get_env)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    content = await file.read()
    document_id = uuid.uuid4()

    try:
        text_extractor = TikaExtractor(base_url="http://tika:9998")
        text = await text_extractor.extract(content)

        text_chunker = SimpleChunker(20, 4)
        chunks = text_chunker.chunk(
            text=text,
            base_metadata={"document_id": document_id, "filename": file.filename},
        )

        embedding_service = JinaEmbedding(
            base_url=env.embedding_base_url,
            api_key=env.embedding_api_key,
            default_model=env.embedding_default_model,
        )

        result = await embedding_service.embed_texts(text=[text])

        await db_session.execute(("Select 1"))
    except Exception as e:
        return HTTPException(status_code=500, detail=e)

    return {
        "doc_id": document_id,
        "chunk_count": len(chunks),
        "sample_chunk": result,
    }
