import io
from colorama import init
from fastapi import HTTPException, UploadFile
from PIL import Image
from pydantic import BaseModel
from core.application.model_service import get_catalog

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_SIDE = 4096

class Prediction(BaseModel):
    model: str
    threshold: float
    inference_ms: int
    width: int
    height: int
    coverage_pct: float
    level: str
    recommendation: str
    mask_png_b64: str 

def validate_model_id(arch, backbone, init):
    model_id = f"{arch}-{backbone}-{init}"

    if model_id not in get_catalog():
        raise HTTPException(400, f"No trained model for {arch} + {backbone} + {init}. See GET /models.")
    return model_id

def validate_photo(upload: UploadFile) -> Image.Image:
    data = upload.file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Image too large (max 10 MB)")

    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except Exception:
        raise HTTPException(400, "Not a valid image file")

    if max(image.size) > MAX_IMAGE_SIDE:
        raise HTTPException(413, "Image side too large (max 4096 px)")

    return image