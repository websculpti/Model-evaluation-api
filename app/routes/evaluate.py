from fastapi import APIRouter, HTTPException, File, Form, UploadFile
import pandas as pd

from app.schemas.request_schema import EvaluationRequest
from app.schemas.response_schema import EvaluationResponse
from app.services.evaluation_service import evaluate_from_metrics 
from app.schemas.data_evaluation_schema import DataEvaluationMetadata
from app.services.model_service import load_uploaded_model
from app.schemas.report_schema import EvaluationSource
from app.services.prediction_service import run_prediction_and_metric_calculation
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/Evaluate")
async def  evaluate_model(request: EvaluationRequest) -> EvaluationResponse:
    try:
        logger.info(f"Evaluation completed")
        return await evaluate_from_metrics(request) 

    except Exception as e:
        logger.error(f"Error occured during evaluation")
        raise HTTPException(status_code=500, detail="Error occured suring evaluation")


@router.post("/evaluate-from-data")
async def evaluate_from_data(
    model_file: UploadFile = File(...),
    test_dataset_file: UploadFile = File(...),
    metadata: str= Form(...,json_schema_extra={
        "example":{
            "tasktype":"regression",
            "target_column":"Price",
            "model_name":"Linear Regression"
        }
    }
    )
):  
    metadata_obj = DataEvaluationMetadata.model_validate_json(metadata)

    metadata_dict = metadata_obj.model_dump()

    logger.info("metadata loaded")

    try:
        model = await load_uploaded_model(model_file)
        logger.info("model done")
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Model loading failed: {str(exc)}",
        )
    
    # x_test,y_Test generation
    target_column = metadata_dict["target_column"]
    data=pd.read_csv(test_dataset_file.file)
    if target_column not in data.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Target column '{target_column}' not found in dataset."
        )

    logger.info("separating y and x test")
    y_test=data[target_column]
    x_test=data.drop(columns=[target_column])

    try:


        prediction_Result=run_prediction_and_metric_calculation(model,x_test,y_test,metadata_dict["tasktype"])

        logger.info("prediction result")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction and metric calculation failed: {str(e)}",
        )
    metrics_text = ", ".join(
        f"{metric_name}: {metric_value:.4f}"
        for metric_name, metric_value in prediction_Result.metrics.items()
    )

    logger.info("returning response")

    return EvaluationResponse(
        message="Uploaded model loaded successfully.",
        report_id="not_generated_yet",
        evaluation_source=EvaluationSource.data,
        model_name=metadata_dict['model_name'],
        tasktype=metadata_dict['tasktype'],
        summary=(
            f"Generated {prediction_Result.prediction_count} prediction(s) using "
            f"model file '{model_file.filename}' and dataset file '{test_dataset_file.filename}'. "
            f"Calculated metrics: {metrics_text}. "
            "LLM evaluation will be connected in the next phase."
        ),
        risk_level="Not assessed yet",
        deployment_readiness="Not assessed yet",
    )
  
   
