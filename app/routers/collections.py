from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends, status

from app.schemas.api_response import ApiResponse
from app.schemas.collection import CollectionCreateRequest, CollectionItemReponse
from app.services.dependencies import get_collection_service
from app.services.collection_service import CollectionService


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
    data = [
        CollectionItemReponse.model_validate(collection) for collection in collections
    ]

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
