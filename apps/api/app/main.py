from typing import Annotated
from fastapi import Depends, FastAPI

from app.config.database import DatabaseConfig, get_db_config
from .routers import files, source
from .config.env import Env, get_env

env = get_env()

app = FastAPI(title=env.app_name)

app.include_router(files.router)
app.include_router(source.router)


@app.get("/")
def read_root(settings: Annotated[Env, Depends(get_env)], db_config: Annotated[DatabaseConfig, Depends(get_db_config)]):
    return {"settings": settings, "db_config": db_config}
