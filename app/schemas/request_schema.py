from typing import Any, Optional
from pydantic import BaseModel, Field, model_validator
from app.schemas.metrics_schema import task_type, validate_metrics_by_task


class ExperimentMetadata(BaseModel):
    dataset_name: Optional[str] = None
    dataset_size: Optional[int] = Field(default=None, ge=1)
    feature_count: Optional[int] = Field(default=None, ge=1)
    target_column: Optional[str] = None
    framework: Optional[str] = None
   
class EvaluationRequest(BaseModel):
    tasktype: task_type
    model_name: str = Field(..., min_length=1)
    metrics: dict[str, Any]
    experiment_metadata: Optional[ExperimentMetadata] = None

    @model_validator(mode="after")
    def validate_metrics_match_task_type(self):

        validate_metrics_by_task(
            tasktype=self.tasktype,
            metrics=self.metrics,
        )

        return self


class DataEvaluationMetadata(BaseModel):
    model_name: str = Field(..., min_length=1)
    framework: str = Field(default="sklearn")
    dataset_name: Optional[str] = None
    target_column: Optional[str] = None
   