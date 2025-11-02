from fastapi import Form
from pydantic import BaseModel, Field


class FileIn(BaseModel):
    note: str | None = Field(default=None, description="Optional note about the file")

    @classmethod
    def as_form(
        cls,
        note: str | None = Form(
            default=None, description="Optional note about the file"
        ),
    ):
        return cls(note=note)


class FileOut(BaseModel):
    id: int
    name: str
    size: int
    note: str | None = None
