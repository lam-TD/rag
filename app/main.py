from typing import Annotated

from fastapi import Depends, FastAPI

from app.config.database import DatabaseConfig, get_db_config
from app.config.env import Env, get_env
from app.routers import collections, documents

env = get_env()

app = FastAPI(title=env.app_name)

app.include_router(documents.router)
app.include_router(collections.router)


@app.get("/")
def read_root(
    settings: Annotated[Env, Depends(get_env)],
    db_config: Annotated[DatabaseConfig, Depends(get_db_config)],
):
    return {"settings": settings, "db_config": db_config}
