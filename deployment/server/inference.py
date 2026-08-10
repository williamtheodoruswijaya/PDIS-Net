import os
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from transformers import SegformerForSemanticSegmentation
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from huggingface_hub import snapshot_download

class Predictor:
    # note: these constants are based on the training notebook
    IMAGENET_MEAN = (0.485, 0.456, 0.406)
    IMAGENET_STD = (0.229, 0.224, 0.225)
    INPUT_SIZE = (512, 512)
    DEFAULT_THRESHOLD = 0.80
    DEFAULT_HF_REPO = "adamantix/pdisnet-weights"

    def __init__(self, weights_dir, device = None):
        self.weights_dir = Path(weights_dir)
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    # alternative constructor to load weights from HF
    @classmethod
    def from_env(cls):
        root = Path(snapshot_download(
            os.environ.get("PDISNET_HF_REPO", cls.DEFAULT_HF_REPO)))
        weights_dir = root / "segformer"
        return cls(weights_dir)

    # for check purposes (if model is loaded with the trained weights or not)
    @property
    def loaded(self) -> bool:
        return self.model is not None

    def load(self) -> "Predictor":
        model = SegformerForSemanticSegmentation.from_pretrained(self.weights_dir)
        self.model = model.to(self.device).eval() # type: ignore
        return self

def predict(self, image: Image.Image) -> np.ndarray:
        # Resize the image to match the input dimensions expected by the model
        height, width = self.INPUT_SIZE
        resized = image.convert("RGB").resize((width, height), Image.BILINEAR) # type: ignore

        # Scale pixels to 0.0-1.0 and apply standard ImageNet normalization
        x = torch.from_numpy(np.asarray(resized)).float().div_(255.0)
        x = (x - torch.tensor(self.IMAGENET_MEAN)) / torch.tensor(self.IMAGENET_STD)

        # Reorder dimensions to PyTorch format (Channels, Height, Width) and add a batch size of 1
        x = x.permute(2, 0, 1).unsqueeze(0).to(self.device)

        # Disable gradient tracking to save memory and speed up inference
        with torch.no_grad():
            logits = self.model(pixel_values=x).logits
            logits = F.interpolate(logits, size=(height, width),
                                    mode="bilinear", align_corners=False)
            
            # Convert raw outputs to probabilities and isolate the target class (plastic)
            probs = torch.softmax(logits, dim=1)[:, 1:2]
            
            # Scale the probability map back up to the original image's resolution
            probs = F.interpolate(probs, size=(image.height, image.width),
                                    mode="bilinear", align_corners=False)

        # Remove the batch and channel dimensions, returning a standard 2D NumPy array with values between 0.0 and 1.0
        return probs[0, 0].cpu().numpy()

'''
# for testing purposes
if __name__ == "__main__":
    p = Predictor.from_env().load()
    probs = p.predict(Image.open("./data/Raw_Images/img30.jpg"))
    print(probs.shape, probs.min(), probs.max())
'''

