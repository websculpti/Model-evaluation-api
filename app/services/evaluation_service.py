from uuid import uuid4

from app.schemas.request_schema import EvaluationRequest
from app.schemas.response_schema import EvaluationResponse
from app.schemas.report_schema import EvaluationSource
from app.services.metrics_service import preprocess_metrics
from app.utils.prompts import build_evaluation_prompt
from app.utils.logger import get_logger
from app.services.llm_service import generate_llm_evaluation

logger = get_logger(__name__)

async def evaluate_from_metrics(request: EvaluationRequest) -> EvaluationResponse:


    try :
        
       
        processed_metrics = preprocess_metrics(
        tasktype=request.tasktype,
        metrics=request.metrics,
        )
        
        logger.info("proccessed metrics")

        prompt = build_evaluation_prompt(
            model_name=request.model_name,
            tasktype=request.tasktype,
            processed_metrics=processed_metrics,
            experiment_metadata=request.experiment_metadata


        )

        logger.info("received prompt")

        llm_output = await generate_llm_evaluation(prompt)

        logger.info("received llm response")

        report_id = f"report_{uuid4().hex[:12]}"

        return EvaluationResponse(
            message="Evaluation metrics processed successfully.",
            report_id=report_id,
            evaluation_source=EvaluationSource.metrics,
            model_name=request.model_name,
            tasktype=request.tasktype,
            summary= llm_output,
            risk_level="Unknown",
            deployment_readiness="Not assessed yet"
        )
           
        
    except:
        return ErrorResponse