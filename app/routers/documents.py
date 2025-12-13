from typing import Annotated, Any, Dict, List, Tuple
from uuid import uuid4
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.env import Env, get_env
from app.models.document import Document
from app.models.embedding import Embedding
from app.schemas.rag import EmbeddingRequest
from app.services.ask.message import build_messages_for_rag
from app.services.chunking.simple_chunker import SimpleChunker
from app.services.collection_service import CollectionService
from app.services.db.pgvector import get_db_session
from app.services.dependencies import get_collection_service
from app.services.embeddings.jina_service import JinaEmbedding
from app.services.text_extractor.tika_extractor import TikaExtractor
from google import genai

router = APIRouter(tags=["Documents"], prefix="/api/v1/collections")


@router.post("/{collection_id}/documents")
async def upload_file(
    collection_id: str,
    file: Annotated[UploadFile, File],
    env: Annotated[Env, Depends(get_env)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    payload: Annotated[EmbeddingRequest, Depends(EmbeddingRequest.as_form)],
    collection_service: Annotated[CollectionService, Depends(get_collection_service)],
):
    content = await file.read()
    document_id = uuid4()

    try:
        collection_model = await collection_service.find_or_fail(collection_id)

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

        vector_literal = []

        result = await embedding_service.embed_texts(text=chunks)

        if result is None or result.embeddings is None:
            raise HTTPException(status_code=500, detail="Embedding service error")

        document_model = Document(
            collection_id=collection_id,
            cmetadata={"filename": file.filename, "total_tokens": result.total_tokens},
        )
        db_session.add(document_model)
        await db_session.commit()
        await db_session.refresh(document_model)

        embedding_result = result

        for chunk, embed in zip(chunks, embedding_result.embeddings):
            vector_literal = embed["embedding"]

            item = Embedding(
                embedding=vector_literal,
                content=chunk,
                token_count=0,
                cmetadata={},
                collection_id=str(collection_model.id),
                document_id=str(document_model.id),
            )
            db_session.add(item)

        await db_session.commit()

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    return {
        "doc_id": document_model.id,
        "chunk_count": len(chunks),
        "sample_chunk": result,
    }


@router.post("/retrieve")
async def get_file_embeddings(
    question: Annotated[str, Any],
    env: Annotated[Env, Depends(get_env)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    embedding_service = JinaEmbedding(
        base_url=env.embedding_base_url,
        api_key=env.embedding_api_key,
        default_model=env.embedding_default_model,
    )

    embedding_question = await embedding_service.embed_texts(text=[question])

    if embedding_question is None or embedding_question.embeddings is None:
        raise HTTPException(status_code=500, detail="Embedding service error")

    query = Embeddings.embedding.cosine_distance(
        embedding_question.embeddings[0]["embedding"]
    )

    try:
        result = await db_session.execute(
            select(Embeddings, query.label("distance")).order_by(query).limit(5)
        )
        rows = result.all()

        results = []
        for chunk, distance in rows:
            results.append(
                {
                    "id": str(chunk.id),
                    "doc_id": chunk.document_id,
                    "text": chunk.content,
                    "distance": float(distance),
                    "similarity": float(1 - distance),
                    "chunk_metadata": chunk.chunk_metadata,
                }
            )

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

    messages, used_hits = build_messages_for_rag(question, results)

    system, user = to_system_and_user(messages)

    client = genai.Client()
    answer = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user,
        config={
            "temperature": 0.8,
            "max_output_tokens": 1024,
            "top_p": 0.8,
            "top_k": 40,
        },
    )

    return {
        "question": question,
        "answer": answer.text,
    }


def to_system_and_user(messages: List[Dict[str, str]]) -> Tuple[str, str]:
    system = ""
    user_parts = []
    for m in messages:
        role = m.get("role")
        if role == "system":
            system = m.get("content", "")
        elif role == "user":
            user_parts.append(m.get("content", ""))
    return system, "\n\n".join(p for p in user_parts if p).strip() or "..."


@router.post("/ask")
async def ask_file_question(
    question: Annotated[str, Any],
    env: Annotated[Env, Depends(get_env)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
):
    from app.services.ask.message import build_messages_for_rag

    messages, used_hits = build_messages_for_rag(question, [])

    return {
        "question": messages,
        "used_hits": used_hits,
        # "used_chunks": used_chunks,
    }
