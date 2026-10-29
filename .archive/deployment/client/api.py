import base64
import io
import time
import numpy as np
import requests
from PIL import Image

class ApiClient:
    COLD_START_RETRIES = 6
    COLD_START_WAIT_S = 10
    PREDICT_TIMEOUT_S = 180

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')

    def health(self):
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=5)
            return resp.json() if resp.ok else None
        except requests.RequestException:
            return None

    def predict(self, image_bytes):
        last_error = None
        for _ in range(self.COLD_START_RETRIES):
            try:
                resp = requests.post(
                    f"{self.base_url}/predict",
                    files={"file": ("image", image_bytes)},
                    timeout=self.PREDICT_TIMEOUT_S
                )
            except requests.RequestException as e:
                last_error = str(e)
                time.sleep(self.COLD_START_WAIT_S)
                continue

            if resp.status_code in (502, 503):
                last_error = f"HTTP {resp.status_code} - Space is waking up"
                time.sleep(self.COLD_START_WAIT_S)
                continue

            if not resp.ok:
                detail = resp.json().get("detail", resp.text) if resp.text else resp.reason
                raise RuntimeError(f"Backend error {resp.status_code}: {detail}")

            payload = resp.json()
            prob_png = base64.b64decode(payload["prob_png_b64"])
            return {
                "probs": np.asarray(Image.open(io.BytesIO(prob_png)),
                                    dtype=np.float32) / 255.0,
                "inference_ms": payload["inference_ms"],
                "default_threshold": payload["default_threshold"],
            }
        raise RuntimeError(f"Backend unreachable after "
                            f"{self.COLD_START_RETRIES} attempts: {last_error}")