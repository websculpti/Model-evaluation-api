from enum import Enum
from typing import Optional
from pydantic import BaseModel

from app.schemas.metrics_schema import task_type
from app.schemas.report_schema import EvaluationSource


class ResponseStatus(str, Enum):
    success = "success"
    error = "error"


class EvaluationResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.success
    message: str
    report_id: str
    evaluation_source: EvaluationSource
    model_name: str
    tasktype: task_type
    summary: str
    risk_level: Optional[str] = None
    deployment_readiness: Optional[str] = None


class ErrorResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.error
    message: str
    detail: Optional[str] = None