"""Model layer: weight loading and inference. HTTP lives in app.py.

DESIGN NOTE: a class because Predictor must remember the loaded model and
the torch device. Load once at startup, reuse for every request.
"""

import os
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import SegformerForSemanticSegmentation
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class Predictor:
    """Loads the checkpoint once, then runs inference on demand.

    Use:
        predictor = Predictor.from_env().load()
        probs = predictor.predict(image)
    """

    # facts copied from the training notebook — model must be used with the
    # exact same numbers it was trained with, so don't change these
    IMAGENET_MEAN = (0.485, 0.456, 0.406)
    IMAGENET_STD = (0.229, 0.224, 0.225)
    INPUT_SIZE = (512, 512)        # (H, W) — must match the training notebook
    DEFAULT_THRESHOLD = 0.80       # calculated on the validation set, not a preference
    DEFAULT_HF_REPO = "adamantix/pdisnet-weights"

    def __init__(self, weights_dir: str | Path, device: str | None = None):
        # only remember where the weights are — load() does the heavy work
        self.weights_dir = Path(weights_dir)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    @classmethod
    def from_env(cls) -> "Predictor":
        """Alternative constructor: local folder via env var, else download from HF Hub."""
        weights_dir = os.environ.get("PDISNET_SEGFORMER_DIR")
        if not weights_dir:
            from huggingface_hub import snapshot_download

            root = Path(snapshot_download(
                os.environ.get("PDISNET_HF_REPO", cls.DEFAULT_HF_REPO)))
            weights_dir = root / "segformer"
        return cls(weights_dir)

    @property
    def loaded(self) -> bool:
        # True once load() has been called
        return self.model is not None

    def load(self) -> "Predictor":
        """Load the checkpoint into memory. Returns self so calls can chain."""
        model = SegformerForSemanticSegmentation.from_pretrained(self.weights_dir)
        # eval() = no training randomness; move to "cuda" or "cpu"
        self.model = model.to(self.device).eval()
        return self

    def predict(self, image: Image.Image) -> np.ndarray:
        """Run the model on a PIL image, return a prob map at original size."""
        # 1. resize to the only size the model knows
        height, width = self.INPUT_SIZE
        resized = image.convert("RGB").resize((width, height), Image.BILINEAR)

        # 2. same normalization as training: 0-255 → 0-1, then ImageNet shift
        x = torch.from_numpy(np.asarray(resized)).float().div_(255.0)
        x = (x - torch.tensor(self.IMAGENET_MEAN)) / torch.tensor(self.IMAGENET_STD)

        # 3. (H, W, C) → (C, H, W), plus a batch dimension of 1
        x = x.permute(2, 0, 1).unsqueeze(0).to(self.device)

        # 4. no_grad = inference only, skip training bookkeeping
        with torch.no_grad():
            logits = self.model(pixel_values=x).logits
            logits = F.interpolate(logits, size=(height, width),
                                   mode="bilinear", align_corners=False)
            # 5. softmax → probabilities; channel 1 = plastic
            probs = torch.softmax(logits, dim=1)[:, 1:2]
            # 6. stretch probabilities (not a yes/no mask) back to original size
            probs = F.interpolate(probs, size=(image.height, image.width),
                                  mode="bilinear", align_corners=False)

        return probs[0, 0].cpu().numpy()

'''
# for testing purposes
if __name__ == "__main__":
    p = Predictor.from_env().load()
    probs = p.predict(Image.open("./data/Raw_Images/img30.jpg"))
    print(probs.shape, probs.min(), probs.max())
'''

