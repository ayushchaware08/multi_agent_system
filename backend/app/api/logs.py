from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.logging_utils import tail_logs

router = APIRouter()

@router.get("/")
def get_logs(limit: int = 100):
    logs = tail_logs(limit=limit)
    return JSONResponse(content={"logs": logs})
