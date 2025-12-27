from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from google import genai
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.env import Env, get_env
from app.models.embedding import Embedding
from app.repositories.collection_repository import ModelNotFound
from app.schemas.api_response import ApiResponse
from app.schemas.collection import (
    CollectionChatReponse,
    CollectionChatRequet,
    CollectionCreateRequest,
    CollectionItemReponse,
)
from app.schemas.embedding import EmbeddingItem
from app.services.ask import prompt_genenrator
from app.services.collection_service import CollectionService
from app.services.db.pgvector import get_db_session
from app.services.dependencies import get_collection_service
from app.services.embeddings.jina_service import JinaEmbedding

router = APIRouter(tags=["Collections"], prefix="/api/v1/collections")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[list[CollectionItemReponse]],
)
async def index(
    collection_service: Annotated[CollectionService, Depends(get_collection_service)],
) -> ApiResponse[list[CollectionItemReponse]]:
    collections = await collection_service.paginate()
    data = [CollectionItemReponse.model_validate(collection) for collection in collections]

    return ApiResponse().ok(
        data=data,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[CollectionItemReponse],
)
async def store(
    payload: Annotated[CollectionCreateRequest, Body(...)],
    collection_service: Annotated[CollectionService, Depends(get_collection_service)],
) -> ApiResponse[CollectionItemReponse]:
    collection = await collection_service.create(payload)

    return ApiResponse().ok(
        data=CollectionItemReponse.model_validate(collection),
    )


@router.post(
    "/{collection_id}/chat",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[CollectionChatReponse],
)
async def chat(
    env: Annotated[Env, Depends(get_env)],
    payload: Annotated[CollectionChatRequet, Body(...)],
    collection_service: Annotated[CollectionService, Depends(get_collection_service)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    collection_id: str = "default",
) -> ApiResponse[CollectionChatReponse]:
    try:
        collection = await collection_service.find_by_name(collection_id)
        embedding_service = JinaEmbedding(
            base_url=env.embedding_base_url,
            api_key=env.embedding_api_key,
            default_model=env.embedding_default_model,
        )

        embed_question = await embedding_service.embed_texts(text=[payload.question])

        if embed_question is None or embed_question.embeddings is None:
            raise HTTPException(status_code=500, detail="Embedding service error")

        embed_query = Embedding.embedding.cosine_distance(embed_question.embeddings[0]["embedding"])
        embed_select = (
            select(Embedding, embed_query.label("distance"))
            .where(Embedding.collection_id == collection.id)
            .order_by(embed_query)
            .limit(5)
        )

        embed_result = await db_session.execute(embed_select)
        embed_result = embed_result.all()
        context = []
        for chunk, distance in embed_result:
            chunk.similarity = 1 - distance
            context.append(EmbeddingItem.model_validate(chunk))

        messages, kept = prompt_genenrator.build(
            query=payload.question, hits=context, answer_lang="en"
        )
        system_msg = str(messages[0]["content"])
        user_msg = str(messages[1]["content"])

        client = genai.Client()
        answer = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_msg,
            config={
                "temperature": 0.8,
                "max_output_tokens": 1024,
                "top_p": 0.8,
                "top_k": 40,
                "system_instruction": system_msg,
            },
        )

        print(answer.parts[0].text)

    except ModelNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The {collection_id} is invalid",
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from None

    data = CollectionChatReponse(
        question=payload.question,
        top_k=payload.top_k,
        answer=answer.parts[0].text,
        context=kept,
    )
    return ApiResponse().ok(data=data)
