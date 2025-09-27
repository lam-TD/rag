from fastapi import FastAPI
from .routers import files

app = FastAPI(title="My FastAPI Application")

app.include_router(files.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
