import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine() -> Engine:
    return create_engine(DATABASE_URL, pool_pre_ping=True)
