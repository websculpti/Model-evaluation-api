from fastapi import APIRouter, HTTPException

from app.schemas.request_schema import EvaluationRequest
from app.schemas.response_schema import EvaluationResponse
from app.services.evaluation_service import evaluate_from_metrics 
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/Evaluate")
async def  evaluate_model(request: EvaluationRequest) -> EvaluationResponse:
    try:
        logger.info(f"Evaluation completed")
        return await evaluate_from_metrics(request) 

    except Exception as e:
        logger.error(f"Error occured during evaluation")
        raise HTTPException(status_code=500, detail="Error occured suring evaluation")

   