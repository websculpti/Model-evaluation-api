from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field

from app.schemas.metrics_schema import task_type


class EvaluationSource(str, Enum):
    metrics = "metrics"
    data = "data"


class RiskLevel(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"
    critical = "Critical"
    unknown = "Unknown"


class ReportMetadata(BaseModel):
    report_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_name: str
    tasktype: task_type
    evaluation_source: EvaluationSource
    dataset_name: Optional[str] = None


class ReportContent(BaseModel):
    performance_summary: str
    risk_assessment: str
    deployment_readiness: str
    recommendations: list[str] = Field(default_factory=list)
    metric_flags: list[str] = Field(default_factory=list)
    llm_raw_output: Optional[str] = None


class EvaluationReport(BaseModel):
    metadata: ReportMetadata
    content: ReportContent
    metrics: dict[str, Any]
    experiment_metadata: Optional[dict[str, Any]] = None