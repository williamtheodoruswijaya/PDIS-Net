from contextlib import asynccontextmanager
import gradio as gr
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import health, list_models, predict
from api.gradio_preview import demo
from core.application.model_service import get_catalog, get_model
from core.domain.constants import DEFAULT_MODEL_ID
from core.domain.options import OPTIONS

@asynccontextmanager
async def lifespan(app):
    get_catalog()
    get_model(DEFAULT_MODEL_ID)
    yield

app = FastAPI(title="PDIS-Net API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=OPTIONS.frontend_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(list_models.router)
app.include_router(predict.router)

app = gr.mount_gradio_app(app, demo, path="/ui", ssr_mode=False)