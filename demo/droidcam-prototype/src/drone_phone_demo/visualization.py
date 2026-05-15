from __future__ import annotations

from typing import Optional

import cv2
import numpy as np


PLASTIC_COLOR_BGR = np.array([40, 40, 255], dtype=np.uint8)


def make_overlay(frame_bgr: np.ndarray, mask: np.ndarray, probability: np.ndarray) -> np.ndarray:
    overlay = frame_bgr.copy()
    heat = np.zeros_like(frame_bgr, dtype=np.uint8)
    heat[:, :] = PLASTIC_COLOR_BGR

    alpha = np.clip(probability, 0.0, 1.0) * 0.55
    alpha = np.where(mask > 0, np.maximum(alpha, 0.35), 0.0).astype(np.float32)
    alpha_3c = alpha[:, :, None]
    overlay = (frame_bgr.astype(np.float32) * (1.0 - alpha_3c)) + (heat.astype(np.float32) * alpha_3c)
    return np.clip(overlay, 0, 255).astype(np.uint8)


def draw_hud(
    frame_bgr: np.ndarray,
    plastic_percentage: float,
    model_name: str,
    threshold: float,
    latitude: Optional[float],
    longitude: Optional[float],
    timestamp: str,
) -> np.ndarray:
    output = frame_bgr.copy()
    lines = [
        f"Model: {model_name} | Plastic: {plastic_percentage:.2f}% | Threshold: {threshold:.2f}",
        f"Location: {format_coordinate(latitude)}, {format_coordinate(longitude)}",
        f"Time: {timestamp} | s: save | q: quit",
    ]

    x, y = 16, 28
    line_height = 28
    box_width = min(output.shape[1] - 24, 780)
    box_height = line_height * len(lines) + 18

    cv2.rectangle(output, (8, 8), (8 + box_width, 8 + box_height), (0, 0, 0), -1)
    cv2.rectangle(output, (8, 8), (8 + box_width, 8 + box_height), (255, 255, 255), 1)

    for index, line in enumerate(lines):
        cv2.putText(
            output,
            line,
            (x, y + index * line_height),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.68,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    return output


def format_coordinate(value: Optional[float]) -> str:
    if value is None:
        return "n/a"
    return f"{value:.6f}"

