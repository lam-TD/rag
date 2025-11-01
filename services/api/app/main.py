from fastapi import FastAPI
from .routers import files, source

app = FastAPI(title="My FastAPI Application")

app.include_router(files.router)
app.include_router(source.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
