from fastapi import APIRouter
router = APIRouter(tags=["Files"], prefix="/api/v1/files")

@router.get("")
async def read_files():
    return {"files": []}