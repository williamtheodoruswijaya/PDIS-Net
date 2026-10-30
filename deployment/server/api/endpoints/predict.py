import base64
import io
import time
import numpy as np
from fastapi import APIRouter, File, Form, UploadFile
from PIL import Image
from api.endpoints.predict_request import Prediction, validate_model_id, validate_photo
from core.application.segmentation_service import segment
from core.domain.constants import DEFAULT_MODEL_ID
from core.entities.trained_models import MODELS

router = APIRouter()
DEFAULT = MODELS[DEFAULT_MODEL_ID]

@router.post("/predict", response_model=Prediction)
def predict(
    file: UploadFile = File(...),
    arch: str = Form(DEFAULT["arch"]),
    backbone: str = Form(DEFAULT["backbone"]),
    init: str = Form(DEFAULT["init"]),
):
    model_id = validate_model_id(arch, backbone, init)
    image = validate_photo(file)

    start = time.perf_counter()
    result = segment(model_id, image)
    inference_ms = round((time.perf_counter() - start) * 1000)

    return {
        "model": model_id,
        "threshold": result["threshold"],
        "inference_ms": inference_ms,
        "width": image.width,
        "height": image.height,
        "coverage_pct": result["coverage_pct"],
        "level": result["level"],
        "recommendation": result["recommendation"],
        "mask_png_b64": mask_to_png_base64(result["mask"]),
    }

def mask_to_png_base64(mask):
    black_and_white = Image.fromarray(
        mask.astype(np.uint8) * 255,
        mode="L"
    )
    buffer = io.BytesIO()
    black_and_white.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()