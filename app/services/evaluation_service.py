from uuid import uuid4

from app.schemas.request_schema import EvaluationRequest
from app.services.report_service import generate_evaluation_report
from app.schemas.response_schema import EvaluationResponse, ErrorResponse
from app.schemas.report_schema import EvaluationSource
from app.services.metrics_service import preprocess_metrics
from app.utils.prompts import build_evaluation_prompt
from app.utils.logger import get_logger
from app.services.llm_service import generate_llm_evaluation, get_format_instructions

logger = get_logger(__name__)

async def evaluate_from_metrics(request: EvaluationRequest, evaluation_source: EvaluationSource = EvaluationSource.metrics ) -> EvaluationResponse:

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

        report = generate_evaluation_report(
        request=request,
        processed_metrics=processed_metrics,
        llm_output=llm_output,
        evaluation_source= evaluation_source,
        )

        logger.info("received llm response")

       # report_id = f"report_{uuid4().hex[:12]}"

        recommendations_text = " ".join(
        f"{index + 1}. {recommendation}"
        for index, recommendation in enumerate(report.content.recommendations)
         )

        summary = (
            f"{report.content.performance_summary} "
            f"Risk Assessment: {report.content.risk_assessment} "
            f"Recommendations: {recommendations_text}"
        )
      
        logger.info("Ready to return")
        
        return EvaluationResponse(
        message="Evaluation report generated successfully.",
        report_id=report.metadata.report_id,
        evaluation_source=evaluation_source,
        model_name=report.metadata.model_name,
        tasktype=report.metadata.tasktype,
        summary=summary,
        risk_level=llm_output.risk_level,
        deployment_readiness=report.content.deployment_readiness,
   
        )
           
        
    except:
        return ErrorResponse