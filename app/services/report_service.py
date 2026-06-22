from app.schemas.request_schema import EvaluationRequest
from app.schemas.response_schema import EvaluationResponse, LLMEvaluationOutput 
from app.schemas.report_schema import  EvaluationReport,  EvaluationSource,  ReportContent, ReportMetadata
from typing import Any
from app.utils.logger import get_logger
from uuid import uuid4

from pydantic import BaseModel

logger = get_logger(__name__)

def generate_report_id() -> str:

    return f"report_{uuid4().hex[:12]}"


def convert_to_dict(data: Any) -> dict[str, Any]:

    logger.info("converting to dict")

    if data is None:
        return {}

    if isinstance(data, BaseModel):
        return data.model_dump(exclude_none=True)

    if isinstance(data, dict):
        return data

    return {"value": str(data)}


def extract_dataset_name(experiment_metadata: Any | None) -> str | None:

    logger.info("extracting name")

    metadata_dict = convert_to_dict(experiment_metadata)

    dataset_name = metadata_dict.get("dataset_name")

    if dataset_name:
        return str(dataset_name)

    return None


def generate_evaluation_report(
    request: EvaluationRequest,
    processed_metrics: dict[str, Any],
    llm_output: LLMEvaluationOutput,
    evaluation_source: EvaluationSource = EvaluationSource.metrics,
) -> EvaluationReport:

    logger.info("generating report")

    report_id = generate_report_id()

    metadata = ReportMetadata(
        report_id=report_id,
        model_name=request.model_name,
        tasktype=request.tasktype,
        evaluation_source=evaluation_source,
        dataset_name=extract_dataset_name(request.experiment_metadata),
    )

    logger.info("metadata")

    content = ReportContent(
        performance_summary=llm_output.performance_summary,
        risk_assessment=llm_output.risk_assessment,
        deployment_readiness=llm_output.deployment_readiness,
        recommendations=llm_output.recommendations,
        metric_flags=processed_metrics.get("metric_flags", []),     
        llm_raw_output=None,
    )

    logger.info("content")

    report = EvaluationReport(
        metadata=metadata,
        content=content,
        metrics={
            "raw_metrics": request.metrics,
            "processed_metrics": processed_metrics,
        },
       
        experiment_metadata=convert_to_dict(request.experiment_metadata),
    )

    logger.info("report")

    return report
   
   
    

