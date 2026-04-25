from typing import Any

from fastapi import FastAPI, middleware
from injector import Injector
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    pass


class Container(Injector):
    pass


class Application:
    config: Config
    container: Container
    instance: ApplicationBuilder

    def __init__(self) -> None:
        pass

    @staticmethod
    def configure():
        return ApplicationBuilder(Application())


def handle_exceptions():
    return []


class ApplicationBuilder():
    middlewares: list[Any]

    def __init__(self, app: Application) -> None:
        self._app = app

    def schedule(self):
        return self

    def withMiddleware(self, callback):
        callable(self.middlewares)
        return self

    def withExceptions(self, callback):
        return self

    def withRouting(self, routes: list[Any]):
        return self
    
    def create(self):

        app = FastAPI(
            lifespan=
        )

        app.add_middleware()
        app.add_exception_handler()
        return self

Application.configure().withMiddleware([]).withExceptions(handle_exceptions).schedule()
