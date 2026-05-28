from fastapi import APIRouter
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

@router.get("/health")
async def health_check():
    logger.info("Health endpoint called")
    return {
        "status":"ok",
        "message":"Model evaluation is healthy"
    }