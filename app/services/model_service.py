import tempfile
from pathlib import Path
from typing import Any

import joblib
from fastapi import UploadFile


SUPPORTED_MODEL_EXTENSIONS = {".pkl", ".joblib"}


def validate_model_file_extension(filename: str) -> None:
    """
    Validate uploaded model file extension.

    This is synchronous because it only checks the file name.
    """

    file_extension = Path(filename).suffix.lower()

    if file_extension not in SUPPORTED_MODEL_EXTENSIONS:
        raise ValueError(
            "Unsupported model file type. Please upload a .pkl or .joblib file."
        )


async def save_uploaded_model_temporarily(model_file: UploadFile) -> Path:
    """
    Save uploaded model file to a temporary path.

    This is async because UploadFile.read() is an async file operation.
    """

    validate_model_file_extension(model_file.filename)

    file_extension = Path(model_file.filename).suffix.lower()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension,
    ) as temp_file:
        file_content = await model_file.read()
        temp_file.write(file_content)

        return Path(temp_file.name)


def load_model_from_path(model_path: Path) -> Any:
    """
    Load model from a temporary file path.

    This is synchronous because joblib.load() is a blocking local file operation.
    """

    model = joblib.load(model_path)

    return model


def validate_model_has_predict(model: Any) -> None:
    """
    Check whether loaded model has a predict method.
    """

    if not hasattr(model, "predict"):
        raise ValueError("Loaded model is invalid because it does not have a predict() method.")


async def load_uploaded_model(model_file: UploadFile) -> Any:
    """
    Main function used by /evaluate-from-data.

    It saves the uploaded file temporarily, loads the model, validates it,
    and returns the loaded model object.
    """

    temp_model_path = await save_uploaded_model_temporarily(model_file)

    try:
        model = load_model_from_path(temp_model_path)
        validate_model_has_predict(model)

        return model

    finally:
        temp_model_path.unlink(missing_ok=True)