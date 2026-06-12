from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

class task_type(str, Enum):
    classification ="classification"
    regression = "regression"

class classificationMetrics(BaseModel):
    accuracy: Optional[float]=Field(None, le=1, ge=0, description="The accuracy of the classification model.")
    precision: Optional[float]=Field(None, le=1, ge=0,description="The precision of the classification model.")
    recall: Optional[float]=Field(None, le=1, ge=0, description="The recall of the classification model.")
    f1_score: Optional[float]=Field(None,le=1, ge=0, description="The F1 score of the classification model.")
    roc_auc: Optional[float]=Field(None,le=1, ge=0, description="The ROC AUC score of the classification model.")
    log_loss: Optional[float]=Field(None, le=1, ge=0,description="The log loss of the classification model.")

    @model_validator(mode="after")
    def validate_at_least_one_metric(self):
        metric_values = self.model_dump(exclude_none=True)

        if not metric_values:
            raise ValueError("At least one classification metric must be provided.")

        return self

class regressionMetrics(BaseModel):
    mae :Optional[float] = Field(None, ge=0, description= " Mean absolute error")
    mse :Optional[float] = Field(None, ge=0, description= " Mean squared error")
    rmse :Optional[float] = Field(None, ge=0, description= " Root mean absolute error")
    r2_score :Optional[float] = Field(None,  description= " r2 score")

    @model_validator(mode="after")
    def validate_at_least_one_metric(self):
        metric_values = self.model_dump(exclude_none=True)

        if not metric_values:
            raise ValueError("At least one classification metric must be provided.")

        return self

def validate_metrics_by_task(tasktype : task_type, metrics : dict):
    if tasktype == task_type.classification:
        return classificationMetrics.model_validate(metrics)

    if tasktype == task_type.regression:
        return regressionMetrics.model_validate(metrics)

    
    raise ValueError(f"Unsupported task type: {tasktype}")
       