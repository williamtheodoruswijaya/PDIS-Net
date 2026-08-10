import base64
import io
import time
from contextlib import asynccontextmanager
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from PIL import Image
from inference import Predictor

MAX_UPLOAD_BYTES = 10 * 1024 * 1024     # 10 MB
MAX_IMAGE_SIDE = 4096                   # 4096 pixels

# cold start (always load the model on startup to avoid latency on first request)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # load model weights from HF and store the predictor in the app
    predictor = Predictor.from_env().load()
    app.state.predictor = predictor
    yield # before yield = code to be ran on startup

app = FastAPI(title="PDIS-Net Inference API", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(
    request: Request,
    file: UploadFile = File(...)
):
    predictor = request.app.state.predictor

    data = file.file.read(MAX_UPLOAD_BYTES + 1)

    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Image too large")
    try:
        image = Image.open(io.BytesIO(data))
        image.load()
    except Exception:
        raise HTTPException(400, "Invalid image file")
    if max(image.size) > MAX_IMAGE_SIDE:
        raise HTTPException(413, "Image Side too large")

    start = time.perf_counter()
    probs = predictor.predict(image)
    inference_ms = round((time.perf_counter() - start) * 1000)

    prob_img = Image.fromarray((probs * 255).round().astype(np.uint8), mode="L")
    buffer = io.BytesIO()
    prob_img.save(buffer, format="PNG")

    return {
        "default_threshold": Predictor.DEFAULT_THRESHOLD,
        "inference_ms": inference_ms,
        "width": image.width,
        "height": image.height,
        "prob_png_b64": base64.b64encode(buffer.getvalue()).decode()
    }