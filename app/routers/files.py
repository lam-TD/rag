from typing import Annotated, Any
from pathlib import Path
from uuid import uuid4
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, text
from app.config.env import Env, get_env
from app.services.chunking.simple_chunker import SimpleChunker
from app.services.db.pgvector import get_db_session
from app.services.embeddings.jina_service import JinaEmbedding
from app.services.text_extractor.tika_extractor import TikaExtractor
from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID

router = APIRouter(tags=["Files"], prefix="/api/v1/files")

# UPLOAD_PATH = Path("/storage/uploads")
# UPLOAD_PATH.mkdir(parents=True, exist_ok=True)


class Base(DeclarativeBase):
    pass


class Embeddings(Base):
    __tablename__ = "embeddings"

    # Define your table columns here
    id: Mapped[uuid4] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,  # tự generate uuid ở app
        index=True,
    )
    document_id = Column(String, index=True)
    embedding = Column(Vector(1024))
    content = Column(String)
    token_count = Column(Integer)
    chunk_metadata = mapped_column(JSON)


@router.post("")
async def upload_file(
    file: Annotated[UploadFile, File],
    env: Annotated[Env, Depends(get_env)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    content = await file.read()
    document_id = uuid4()

    try:
        text_extractor = TikaExtractor(base_url="http://tika:9998")
        text_result = await text_extractor.extract(content)

        text_chunker = SimpleChunker(500, 100)

        chunks = text_chunker.chunk(
            text=text_result,
            base_metadata={"document_id": document_id, "filename": file.filename},
        )

        embedding_service = JinaEmbedding(
            base_url=env.embedding_base_url,
            api_key=env.embedding_api_key,
            default_model=env.embedding_default_model,
        )

        embedding_result = None
        vector_literal = []

        result = await embedding_service.embed_texts(text=chunks)

        if result is None or result.embeddings is None:
            raise HTTPException(status_code=500, detail="Embedding service error")

        embedding_result = result

        for chunk, embed in zip(chunks, embedding_result.embeddings):
            vector_literal = embed["embedding"]

            # vector_literal = "[" + ",".join(str(v) for v in vector_literal) + "]"

            item = Embeddings(
                document_id=str(document_id),
                embedding=vector_literal,
                content=chunk,
                token_count=0,
                chunk_metadata="{}",
            )
            db_session.add(item)
            continue

            await db_session.execute(
                text(
                    """
                        INSERT INTO embeddings (
                            document_id,
                            embedding,
                            content,
                            token_count,
                            metadata,
                            chunk_metadata
                        )
                        VALUES (
                            :document_id,
                            :embedding::vector,
                            :content,
                            :token_count,
                            :metadata::jsonb,
                            :chunk_metadata::jsonb
                        )
                    """
                ),
                {
                    "document_id": document_id,
                    "embedding": vector_literal,
                    "content": chunk,
                    "token_count": 0,
                    "metadata": {},
                    "chunk_metadata": {},
                },
            )

        await db_session.commit()

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    return {
        "doc_id": document_id,
        "chunk_count": len(chunks),
        "sample_chunk": result,
    }
