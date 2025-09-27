from re import T
from sqlmodel import Field, SQLModel


class FileModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False, unique=True)
    size: int = Field(nullable=False)
    absolute_path: str = Field(nullable=False)
    note: str | None = Field(nullable=True, default=None)
