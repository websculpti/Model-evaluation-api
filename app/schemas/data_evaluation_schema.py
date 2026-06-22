from pydantic import BaseModel

from app.schemas.metrics_schema import task_type


class DataEvaluationMetadata(BaseModel):
    tasktype: task_type
    target_column: str
    model_name: str