from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI

from app.config.env import Env, get_env


def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    env = get_env()
    app.state.env = env
    if env.app_name:
        app.title = env.app_name
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model

    yield

    ml_models.clear()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root(
    settings: Annotated[Env, Depends(get_env)],
):
    return {"settings": app.state.env}


@app.get("/test")
def test(
    commons: Annotated[dict, Depends(common_parameters)],
):
    return {"commons": commons}
