from fastapi import APIRouter
from pydantic import BaseModel
from core.application.model_service import get_catalog

router = APIRouter()

class ModelInfo(BaseModel):
    id: str
    arch: str
    backbone: str
    init: str
    miou: float
    threshold: float

@router.get("/models", response_model=list[ModelInfo])
def list_models():
    catalog = list(get_catalog().values())

    return catalog