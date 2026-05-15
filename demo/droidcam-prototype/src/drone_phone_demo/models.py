from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
import torch


DEMO_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = next(
    (candidate for candidate in DEMO_ROOT.parents if (candidate / "model").exists()),
    DEMO_ROOT.parent,
)

LABEL2ID = {"background": 0, "plastic": 1}
ID2LABEL = {0: "background", 1: "plastic"}


@dataclass(frozen=True)
class SegmentationResult:
    probability: np.ndarray
    mask: np.ndarray
    plastic_percentage: float
    inference_ms: float


class BaseSegmenter:
    def __init__(self, model_path: Path, device: str, threshold: float) -> None:
        self.model_path = model_path
        self.device = resolve_device(device)
        self.threshold = threshold

    def predict(self, frame_bgr: np.ndarray) -> SegmentationResult:
        raise NotImplementedError


class SegformerSegmenter(BaseSegmenter):
    def __init__(self, model_path: Path, device: str, threshold: float) -> None:
        super().__init__(model_path, device, threshold)
        from transformers import SegformerForSemanticSegmentation, SegformerImageProcessor

        self.processor = SegformerImageProcessor.from_pretrained(model_path)
        self.model = SegformerForSemanticSegmentation.from_pretrained(
            model_path,
            num_labels=2,
            id2label=ID2LABEL,
            label2id=LABEL2ID,
            ignore_mismatched_sizes=True,
        )
        self.model.to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def predict(self, frame_bgr: np.ndarray) -> SegmentationResult:
        start = time.perf_counter()
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        inputs = self.processor(images=frame_rgb, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        outputs = self.model(**inputs)
        logits = torch.nn.functional.interpolate(
            outputs.logits,
            size=frame_bgr.shape[:2],
            mode="bilinear",
            align_corners=False,
        )
        probs = torch.softmax(logits, dim=1)[0, 1].detach().cpu().numpy()
        return build_result(probs, self.threshold, start)


class Dinov3Segmenter(BaseSegmenter):
    def __init__(self, model_path: Path, device: str, threshold: float) -> None:
        super().__init__(model_path, device, threshold)
        try:
            from transformers import AutoImageProcessor, EomtDinov3ForUniversalSegmentation
        except ImportError as exc:
            raise RuntimeError(
                "DINOv3/EoMT is not supported by the installed Transformers package. "
                "Use --model segformer for this machine, or install a Transformers version "
                "that provides EomtDinov3ForUniversalSegmentation."
            ) from exc

        self.processor = AutoImageProcessor.from_pretrained(model_path)
        self.model = EomtDinov3ForUniversalSegmentation.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()

    @torch.inference_mode()
    def predict(self, frame_bgr: np.ndarray) -> SegmentationResult:
        start = time.perf_counter()
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        inputs = self.processor(images=frame_rgb, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        outputs = self.model(**inputs)
        class_logits = outputs.class_queries_logits
        mask_logits = outputs.masks_queries_logits

        class_probs = torch.softmax(class_logits, dim=-1)
        mask_probs = torch.sigmoid(mask_logits)
        semantic_probs = torch.einsum("bqc,bqhw->bchw", class_probs, mask_probs)
        semantic_probs = semantic_probs / semantic_probs.sum(dim=1, keepdim=True).clamp_min(1e-6)
        semantic_probs = torch.nn.functional.interpolate(
            semantic_probs,
            size=frame_bgr.shape[:2],
            mode="bilinear",
            align_corners=False,
        )
        probs = semantic_probs[0, 1].detach().cpu().numpy()
        return build_result(probs, self.threshold, start)


def build_result(probability: np.ndarray, threshold: float, start_time: float) -> SegmentationResult:
    probability = np.clip(probability.astype(np.float32), 0.0, 1.0)
    mask = (probability > threshold).astype(np.uint8)
    plastic_percentage = float(mask.mean() * 100.0)
    inference_ms = (time.perf_counter() - start_time) * 1000.0
    return SegmentationResult(
        probability=probability,
        mask=mask,
        plastic_percentage=plastic_percentage,
        inference_ms=inference_ms,
    )


def load_segmenter(
    model_name: str,
    model_path: Optional[Path],
    device: str,
    threshold: Optional[float],
) -> BaseSegmenter:
    resolved_path = resolve_model_path(model_name, model_path)
    resolved_threshold = threshold if threshold is not None else default_threshold(model_name, resolved_path)

    if model_name == "segformer":
        return SegformerSegmenter(resolved_path, device=device, threshold=resolved_threshold)
    if model_name == "dinov3":
        return Dinov3Segmenter(resolved_path, device=device, threshold=resolved_threshold)

    raise ValueError(f"Unsupported model: {model_name}")


def resolve_device(device: str) -> torch.device:
    if device == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available.")
    return torch.device(device)


def resolve_model_path(model_name: str, explicit_path: Optional[Path]) -> Path:
    candidates: list[Path] = []
    if explicit_path is not None:
        candidates.append(explicit_path)

    if model_name == "segformer":
        candidates.extend(
            [
                DEMO_ROOT / "models" / "segformer",
                REPO_ROOT / "model" / "20261205 - Segformer (mIoU=0.81)",
            ]
        )
    elif model_name == "dinov3":
        candidates.extend(
            [
                DEMO_ROOT / "models" / "dinov3",
                REPO_ROOT / "model" / "20261305 - DinoV3 (mIoU=0.7916)",
            ]
        )

    for candidate in candidates:
        if candidate.exists() and (candidate / "config.json").exists():
            return candidate.resolve()

    pretty = "\n".join(str(candidate) for candidate in candidates)
    raise FileNotFoundError(f"Could not find model folder for {model_name}. Checked:\n{pretty}")


def default_threshold(model_name: str, model_path: Path) -> float:
    if model_name == "dinov3":
        metadata_path = model_path / "training_metadata.json"
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                return float(metadata.get("best_threshold", 0.9))
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                return 0.9
        return 0.9
    if model_name == "segformer":
        return 0.8
    return 0.5
