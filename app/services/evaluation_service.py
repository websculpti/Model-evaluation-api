from uuid import uuid4

from app.schemas.request_schema import EvaluationRequest
from app.schemas.response_schema import EvaluationResponse
from app.schemas.report_schema import EvaluationSource
from app.services.metrics_service import preprocess_metrics
from app.utils.prompts import build_evaluation_prompt
from app.utils.logger import get_logger
from app.services.llm_service import generate_llm_evaluation, get_format_instructions

logger = get_logger(__name__)

async def evaluate_from_metrics(request: EvaluationRequest) -> EvaluationResponse:


    try :
        
       
        processed_metrics = preprocess_metrics(
        tasktype=request.tasktype,
        metrics=request.metrics,
        )
        
        logger.info("proccessed metrics")

        format_instructions = get_format_instructions()

        logger.info("format instruction in evaluation service")

        prompt = build_evaluation_prompt(
            model_name=request.model_name,
            tasktype=request.tasktype,
            processed_metrics=processed_metrics,
            experiment_metadata=request.experiment_metadata,
            format_instructions= format_instructions


        )

        logger.info("received prompt")

        llm_output = await generate_llm_evaluation(prompt)

        logger.info("received llm response")

        report_id = f"report_{uuid4().hex[:12]}"

        recommendations_text = " ".join(
        f"{index + 1}. {recommendation}"
        for index, recommendation in enumerate(llm_output.recommendations)
         )

        summary = (
            f"{llm_output.performance_summary} "
            f"Risk Assessment: {llm_output.risk_assessment} "
            f"Recommendations: {recommendations_text}"
        )
      

        return EvaluationResponse(
        message="Structured LLM evaluation completed successfully.",
        report_id=report_id,
        evaluation_source=EvaluationSource.metrics,
        model_name=request.model_name,
        tasktype=request.tasktype,
        summary=summary,
        risk_level=llm_output.risk_level,
        deployment_readiness=llm_output.deployment_readiness,
        )
           
        
    except:
        return ErrorResponse