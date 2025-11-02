from sqlmodel import Field, SQLModel


class FileBase(SQLModel):
    name: str = Field(index=True)
    size: int
    note: str | None = None
    sha256: str | None = None
    storage_path: str | None = None
    mime_type: str | None = None


class Files(FileBase, table=True):
    id: int = Field(default=None, primary_key=True)


class FileCreate(FileBase):
    pass
