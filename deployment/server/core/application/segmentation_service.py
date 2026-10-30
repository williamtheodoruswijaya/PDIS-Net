import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from core.application.coverage_service import RECOMMENDATIONS, coverage_level
from core.application.model_service import DEVICE, get_catalog, get_model
from core.domain.constants import IMAGENET_MEAN, IMAGENET_STD, INPUT_SIZE

def segment(model_id, image):
    threshold = get_catalog()[model_id]["threshold"]
    probs = predict_probabilities(get_model(model_id), image)
    mask = probs > threshold
    coverage_pct = round(float(mask.mean()) * 100, 2)
    level = coverage_level(coverage_pct)

    return {
        "mask": mask,
        "threshold": threshold,
        "coverage_pct": coverage_pct,
        "level": level,
        "recommendation": RECOMMENDATIONS[level],
    }

def photo_to_tensor(image):
    resized = image.convert("RGB").resize((INPUT_SIZE, INPUT_SIZE), Image.BILINEAR)
    pixels = torch.from_numpy(np.array(resized)).float() / 255.0
    pixels = (pixels - torch.tensor(IMAGENET_MEAN)) / torch.tensor(IMAGENET_STD)
    return pixels.permute(2, 0, 1).unsqueeze(0)  # (H, W, C) -> (1, C, H, W)


@torch.no_grad()
def predict_probabilities(model, image):
    output = model(photo_to_tensor(image).to(DEVICE))

    logits = output.logits if hasattr(output, "logits") else output

    logits = F.interpolate(logits, size=(image.height, image.width), mode="bilinear", align_corners=False)
    plastic = torch.softmax(logits, dim=1)[0, 1]  # channel 1 = plastic, channel 0 = background
    return plastic.cpu().numpy()