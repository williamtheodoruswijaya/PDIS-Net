from __future__ import annotations

import logging
import math
from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from common import (
    BACKGROUND_LABEL,
    ensure_output_dir,
    format_float,
    format_int,
    load_mask_array,
    load_raw_image,
    pair_image_files,
    setup_logging,
    warn_if_empty_mask,
    write_markdown_table,
)


RAW_DIR = "data/Raw_Images"
MASK_DIR = "data/Segmentation_Masks"
OUT_DIR = "eda/boundary_complexity/images"
MD_OUT = "eda/boundary_complexity/results.md"
COLORMAP = "tab20"


def contour_color(class_id: int) -> tuple[int, int, int]:
    rgba = plt.get_cmap(COLORMAP)((class_id % 20) / 19 if class_id else 0)
    return tuple(int(channel * 255) for channel in rgba[:3])


def save_contour_overlay(raw_img: Image.Image, contours_by_class: dict[int, list[np.ndarray]], out_path: Path) -> None:
    overlay = np.array(raw_img.convert("RGB")).copy()
    for class_id, contours in contours_by_class.items():
        cv2.drawContours(overlay, contours, contourIdx=-1, color=contour_color(class_id), thickness=2)
    Image.fromarray(overlay).save(out_path)


def main() -> None:
    setup_logging()
    out_dir = ensure_output_dir(OUT_DIR)
    pairs = pair_image_files(RAW_DIR, MASK_DIR)

    rows: list[str] = []
    for pair in pairs:
        raw_img = load_raw_image(pair.raw_path)
        if raw_img is None:
            continue

        mask_arr = load_mask_array(pair.mask_path, target_size=raw_img.size, image_name=pair.image_stem)
        if mask_arr is None:
            continue

        warn_if_empty_mask(mask_arr, pair.image_stem)
        contours_by_class: dict[int, list[np.ndarray]] = {}
        for class_id in sorted(int(label) for label in np.unique(mask_arr) if int(label) != BACKGROUND_LABEL):
            binary = np.where(mask_arr == class_id, 255, 0).astype(np.uint8)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                logging.warning("No contours found for %s class %s", pair.image_stem, class_id)
                continue

            total_perimeter = float(sum(cv2.arcLength(contour, True) for contour in contours))
            total_area = float(sum(cv2.contourArea(contour) for contour in contours))
            complexity = (
                (total_perimeter**2) / (4 * math.pi * total_area)
                if total_area > 0
                else 0.0
            )
            contours_by_class[class_id] = contours
            rows.append(
                "| {image} | {class_id} | {count} | {perimeter} | {area} | {complexity} |".format(
                    image=pair.image_stem,
                    class_id=class_id,
                    count=format_int(len(contours)),
                    perimeter=format_int(round(total_perimeter)),
                    area=format_int(round(total_area)),
                    complexity=format_float(complexity, digits=2),
                )
            )

        save_contour_overlay(raw_img, contours_by_class, out_dir / f"{pair.image_stem}_contours.png")

    write_markdown_table(
        MD_OUT,
        "| Image | Class ID | Contour Count | Total Perimeter (px) | Total Area (px²) | Complexity Score |",
        "|-------|----------|---------------|----------------------|-----------------|------------------|",
        rows,
    )
    logging.info("Wrote %d boundary complexity rows to %s", len(rows), MD_OUT)


if __name__ == "__main__":
    main()
