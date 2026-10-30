from fastapi import APIRouter
from pydantic import BaseModel
from core.application.model_service import DEVICE, get_catalog

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    device: str
    models_available: int 

@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        device=DEVICE,
        models_available=len(get_catalog()),
    )