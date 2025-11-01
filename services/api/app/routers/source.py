from fastapi import APIRouter

router = APIRouter(tags=["Source"], prefix="/api/v1/source")

@router.get("")
def get_sources():
    return {"message": "List of sources"}

@router.post("")
def create_source(source: dict):
    return {"message": "Source created", "source": source}

@router.get("/{source_id}")
def get_source(source_id: int):
    return {"message": f"Details of source with id {source_id}"}

@router.put("/{source_id}")
def update_source(source_id: int, source: dict):
    return {"message": f"Source with id {source_id} updated", "source": source}

@router.delete("/{source_id}")
def delete_source(source_id: int):
    return {"message": f"Source with id {source_id} deleted"}