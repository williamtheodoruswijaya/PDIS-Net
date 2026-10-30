import json
from functools import lru_cache
import segmentation_models_pytorch as smp
import torch
from transformers import SegformerConfig, SegformerForSemanticSegmentation
from core.entities.trained_models import MODELS
from core.infrastructure.weights_store import weights_file

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@lru_cache(maxsize=None)
def get_catalog():
    catalog = {}

    for model_id, info in MODELS.items():
        metrics = json.loads(weights_file(info["folder"], "test_metrics.json").read_text())
        catalog[model_id] = {
            "id": model_id,
            "arch": info["arch"],
            "backbone": info["backbone"],
            "init": info["init"],
            "miou": metrics["miou"],
            "threshold": metrics["cfg"]["threshold"],
        }
    return catalog

def build_empty_model(arch, backbone):
    if arch == "segformer" and backbone.startswith("mit_"):
        config = SegformerConfig.from_pretrained(
            "nvidia/" + backbone.replace("_", "-"),
            id2label={0: "background", 1: "plastic"},
            label2id={"background": 0, "plastic": 1},
        )
        return SegformerForSemanticSegmentation(config)

    if arch == "unet":
        return smp.Unet(encoder_name=backbone, encoder_weights=None, classes=2)

    if arch == "deeplab":
        return smp.DeepLabV3Plus(encoder_name=backbone, encoder_weights=None, classes=2)

    return smp.Segformer(
        encoder_name=backbone,
        encoder_weights=None,
        classes=2,
        decoder_segmentation_channels=768,
    )

@lru_cache(maxsize=3) 
def get_model(model_id):
    info = MODELS[model_id]
    model = build_empty_model(info["arch"], info["backbone"])
    weights = torch.load(weights_file(info["folder"], "best.pth"), map_location="cpu", weights_only=True)
    model.load_state_dict(weights)
    return model.to(DEVICE).eval()