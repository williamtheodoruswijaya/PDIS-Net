from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from common import (
    ensure_output_dir,
    load_mask_array,
    load_raw_image,
    markdown_relpath,
    pair_image_files,
    setup_logging,
    warn_if_empty_mask,
    write_markdown_table,
)


RAW_DIR = "data/Raw_Images"
MASK_DIR = "data/Segmentation_Masks"
OUT_DIR = "eda/overlay/images"
MD_OUT = "eda/overlay/results.md"
ALPHA = 0.45
COLORMAP = "tab20"


def apply_colormap(mask_arr: np.ndarray, cmap_name: str = "tab20") -> np.ndarray:
    """Map integer class labels to an RGBA uint8 array."""
    norm = mask_arr.astype(np.float32) / max(float(mask_arr.max()), 1.0)
    rgba = plt.get_cmap(cmap_name)(norm)
    return (rgba * 255).astype(np.uint8)


def overlay_mask_on_image(
    raw_img: Image.Image,
    mask_img: Image.Image | np.ndarray,
    alpha: float = 0.45,
    cmap_name: str = "tab20",
) -> Image.Image:
    raw_rgba = raw_img.convert("RGBA")
    mask_arr = np.array(mask_img.convert("L")) if isinstance(mask_img, Image.Image) else mask_img
    mask_rgba = Image.fromarray(apply_colormap(mask_arr, cmap_name))
    mask_rgba = mask_rgba.resize(raw_rgba.size, Image.Resampling.NEAREST)
    r, g, b, _ = mask_rgba.split()
    a = Image.new("L", raw_rgba.size, int(255 * alpha))
    mask_rgba = Image.merge("RGBA", (r, g, b, a))
    return Image.alpha_composite(raw_rgba, mask_rgba)


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
        overlay = overlay_mask_on_image(raw_img, mask_arr, alpha=ALPHA, cmap_name=COLORMAP)
        overlay_path = out_dir / f"{pair.image_stem}_overlay.png"
        overlay.save(overlay_path)

        raw_link = markdown_relpath(pair.raw_path, MD_OUT)
        mask_link = markdown_relpath(pair.mask_path, MD_OUT)
        overlay_link = markdown_relpath(overlay_path, MD_OUT)
        rows.append(
            f"| `{pair.image_stem}` | ![]({raw_link}) | ![]({mask_link}) | ![]({overlay_link}) |"
        )

    write_markdown_table(
        MD_OUT,
        "| Image | Raw Image | Mask | Overlay |",
        "|-------|-----------|------|---------|",
        rows,
    )
    logging.info("Wrote %d overlay rows to %s", len(rows), MD_OUT)


if __name__ == "__main__":
    main()
