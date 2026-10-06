import json
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
import segmentation_models_pytorch as smp
from transformers import SegformerForSemanticSegmentation, SegformerConfig

ROOT = Path(__file__).parent.parent
RAW = ROOT / "data" / "raw"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

RUNS = {
    "01-segformer-mitb3-raw": "nvidia/mit-b3",
    "02-segformer-mitb3-imagenet": "nvidia/mit-b3",
    "03-unet-mitb3-imagenet": "mit_b3",
    "04-segformer-mitb3-aerial": "restor/tcd-segformer-mit-b3",
    "05-segformer-mitb3-ade": "nvidia/segformer-b3-finetuned-ade-512-512",
    "06-segformer-mitb3-drone": "pablojrios/segformer-b3-finetuned-drones",
    "07-segformer-mitb5-imagenet": "nvidia/mit-b5",
    "08-unet-resnet34-raw": "resnet34",
}


def build(src):
    if "/" in src:
        return SegformerForSemanticSegmentation(SegformerConfig.from_pretrained(src, num_labels=2))
    return smp.Unet(src, encoder_weights=None, classes=2)


@torch.no_grad()
def score(model, names, size):
    fg_iou, bg_iou, fg_acc, bg_acc = [], [], [], []
    for n in names:
        img = cv2.resize(cv2.cvtColor(cv2.imread(str(RAW / "Raw_Images" / n)), cv2.COLOR_BGR2RGB), (size, size))
        gt = (cv2.imread(str(RAW / "Segmentation_Masks" / n.replace(".jpg", "_mask.png")), cv2.IMREAD_GRAYSCALE) > 127).astype(np.uint8)
        t = torch.from_numpy(cv2.resize(gt, (size, size), interpolation=cv2.INTER_NEAREST)).float().to(DEVICE)
        x = torch.from_numpy(((img / 255.0 - MEAN) / STD).transpose(2, 0, 1)).float()[None].to(DEVICE)

        out = model(x)
        logits = F.interpolate(out.logits, size=x.shape[-2:], mode="bilinear", align_corners=False) if hasattr(out, "logits") else out
        p = (torch.softmax(logits, 1)[0, 1] > 0.5).float()

        eps = 1e-7
        tp, fp = (p * t).sum(), (p * (1 - t)).sum()
        fn, tn = ((1 - p) * t).sum(), ((1 - p) * (1 - t)).sum()
        fg_iou.append((tp + eps) / (tp + fp + fn + eps))
        bg_iou.append((tn + eps) / (tn + fp + fn + eps))
        fg_acc.append((tp + eps) / (tp + fn + eps))
        bg_acc.append((tn + eps) / (tn + fp + eps))

    mean = lambda v: float(torch.stack(v).mean())
    return (mean(fg_iou) + mean(bg_iou)) / 2, mean(bg_acc), (mean(fg_acc) + mean(bg_acc)) / 2


for run, src in RUNS.items():
    files = [ROOT / "model" / run / "v1" / "test_metrics.json", ROOT / "results" / run / "v1" / "test_metrics.json"]
    m = json.loads(files[0].read_text())

    model = build(src)
    weights = next((ROOT / "model" / run / "v1").glob("*.pth"))
    model.load_state_dict(torch.load(weights, map_location="cpu", weights_only=True))
    model.to(DEVICE).eval()

    names = pd.read_csv(ROOT / "results" / run / "v1" / "split_test.csv")["image_name"]
    miou, bg_acc, mpa = score(model, names, m["cfg"]["img_size"])

    ok = abs(miou - m["miou"]) < 1e-3
    print(f"{run:30s} stored mIoU {m['miou']:.4f} | re-scored {miou:.4f} | mPA {mpa:.4f} | {'written' if ok else 'MISMATCH, skipped'}")
    if ok:
        for f in files:
            d = json.loads(f.read_text())
            d["background_acc"], d["mpa"] = bg_acc, mpa
            f.write_text(json.dumps(d, indent=2))
