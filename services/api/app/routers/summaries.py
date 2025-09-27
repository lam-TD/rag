from fastapi import APIRouter

router = APIRouter(tags=["Summaries"], prefix="/api/v1/summaries")


@router.get("/{file_id}")
async def create_summary():
    return {"summary": "This is a summary"}
