from uuid import uuid4

from app.schemas.request_schema import EvaluationRequest
from app.schemas.response_schema import EvaluationResponse
from app.schemas.report_schema import EvaluationSource
from app.services.metrics_service import preprocess_metrics
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def evaluate_from_metrics(request: EvaluationRequest) -> EvaluationResponse:


    try :
        
       
        processed_metrics = preprocess_metrics(
        tasktype=request.tasktype,
        metrics=request.metrics,
        )
        
        logger.info("proccessed metrics")

        report_id = f"report_{uuid4().hex[:12]}"

        metric_count = len(processed_metrics["formatted_metrics"])
        missing_metrics = processed_metrics["missing_metrics"]
        metric_flags = processed_metrics["metric_flags"]

        if missing_metrics:
            missing_text = ", ".join(missing_metrics)
        else:
            missing_text = "None"

        flags_text = " ".join(metric_flags)

        logger.info("Ready to return")

        return EvaluationResponse(
            message="Evaluation metrics processed successfully.",
            report_id=report_id,
            evaluation_source=EvaluationSource.metrics,
            model_name=request.model_name,
            tasktype=request.tasktype,
            summary=(
                f"Processed {metric_count} metric(s) for {request.model_name}. "
                f"Missing optional metrics: {missing_text}. "
                f"Metric observations: {flags_text}"
            ),
            risk_level="Unknown",
            deployment_readiness="Not assessed yet",
        )
           
        
    except:
        return ErrorResponse