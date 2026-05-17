from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


class DetectionWriter:
    def __init__(self, output_root: Path, model_name: str, camera_source: str) -> None:
        self.output_root = output_root
        self.model_name = model_name
        self.camera_source = camera_source
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_dir = output_root / self.run_id
        self.images_dir = self.run_dir / "images"
        self.masks_dir = self.run_dir / "masks"
        self.overlays_dir = self.run_dir / "overlays"
        self.csv_path = self.run_dir / "detections.csv"
        self.jsonl_path = self.run_dir / "detections.jsonl"
        self.latest_json_path = output_root / "latest_detection.json"

        for directory in [self.images_dir, self.masks_dir, self.overlays_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        self._ensure_csv_header()

    def write(
        self,
        frame_index: int,
        timestamp: str,
        frame_bgr: np.ndarray,
        mask: np.ndarray,
        overlay_bgr: np.ndarray,
        plastic_percentage: float,
        threshold: float,
        latitude: Optional[float],
        longitude: Optional[float],
        altitude_m: Optional[float],
        telemetry_source: str,
        inference_ms: float,
    ) -> dict:
        stem = f"frame_{frame_index:06d}"
        image_path = self.images_dir / f"{stem}.jpg"
        mask_path = self.masks_dir / f"{stem}_mask.png"
        overlay_path = self.overlays_dir / f"{stem}_overlay.jpg"

        cv2.imwrite(str(image_path), frame_bgr)
        cv2.imwrite(str(mask_path), (mask * 255).astype(np.uint8))
        cv2.imwrite(str(overlay_path), overlay_bgr)

        record = {
            "run_id": self.run_id,
            "frame_index": frame_index,
            "timestamp": timestamp,
            "model": self.model_name,
            "plastic_percentage": round(float(plastic_percentage), 4),
            "latitude": latitude,
            "longitude": longitude,
            "altitude_m": altitude_m,
            "telemetry_source": telemetry_source,
            "threshold": round(float(threshold), 4),
            "inference_ms": round(float(inference_ms), 2),
            "camera_source": self.camera_source,
            "image_path": image_path.relative_to(self.output_root).as_posix(),
            "mask_path": mask_path.relative_to(self.output_root).as_posix(),
            "overlay_path": overlay_path.relative_to(self.output_root).as_posix(),
        }

        self._append_csv(record)
        self._append_jsonl(record)
        self.latest_json_path.parent.mkdir(parents=True, exist_ok=True)
        self.latest_json_path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(
            f"Saved {stem}: plastic={record['plastic_percentage']:.2f}% "
            f"lat={latitude} lon={longitude}"
        )
        return record

    def _ensure_csv_header(self) -> None:
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        with self.csv_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

    def _append_csv(self, record: dict) -> None:
        with self.csv_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow({field: record.get(field) for field in FIELDNAMES})

    def _append_jsonl(self, record: dict) -> None:
        with self.jsonl_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")


FIELDNAMES = [
    "run_id",
    "frame_index",
    "timestamp",
    "model",
    "plastic_percentage",
    "latitude",
    "longitude",
    "altitude_m",
    "telemetry_source",
    "threshold",
    "inference_ms",
    "camera_source",
    "image_path",
    "mask_path",
    "overlay_path",
]

