import json
from typing import Any

from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel

from app.schemas.metrics_schema import task_type


evaluation_prompt = PromptTemplate.from_template(
    """
You are an ML evaluation assistant.

Evaluate the following machine learning model using the provided structured evaluation data.

Model Name:
{model_name}

Task Type:
{tasktype}

Processed Metrics:
{processed_metrics}

Experiment Metadata:
{experiment_metadata}

Return the evaluation using the required structured format.

Format Instructions:
{format_instructions}

Your task is to generate a structured model evaluation report.

Important rules:
- Do not assume metrics that are not present.
- Clearly mention missing important metrics.
- Base your judgment only on the provided metrics and metadata.
- Keep the explanation practical for ML deployment decisions.
""".strip()
)


def convert_to_serializable_dict(data: Any) -> dict[str, Any]:
    "  Convert Pydantic models or dictionaries into JSON-serializable dictionaries."
  


    if data is None:
        return {}

    if isinstance(data, BaseModel):
        return data.model_dump(exclude_none=True)

    if isinstance(data, dict):
        return data

    return {"value": str(data)}


def build_evaluation_prompt(
    model_name: str,
    tasktype: task_type,
    processed_metrics: dict[str, Any],
    experiment_metadata: Any | None = None,
    format_instructions:str ="",
) -> str:
   

    metadata_dict = convert_to_serializable_dict(experiment_metadata)

    prompt = evaluation_prompt.format(
        model_name=model_name,
        tasktype=tasktype.value,
        processed_metrics=json.dumps(processed_metrics, indent=2),
        experiment_metadata=json.dumps(metadata_dict, indent=2),
        format_instructions= format_instructions,
    )

    return prompt