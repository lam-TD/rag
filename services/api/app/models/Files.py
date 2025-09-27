from sqlmodel import SQLModel, Field


class File(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str