from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.services.collection_service import CollectionService
from app.repositories.collection_repository import CollectionRepository
from app.services.db.pgvector import get_db_session

DbSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


def get_collection_repository(db_session: DbSessionDep):
    return CollectionRepository(db_session)


def get_collection_service(
    repository: Annotated[CollectionRepository, Depends(get_collection_repository)],
):
    return CollectionService(repository)
