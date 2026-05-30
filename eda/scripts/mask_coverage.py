from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import (
    BACKGROUND_LABEL,
    ensure_output_dir,
    format_int,
    format_percent,
    load_mask_array,
    load_raw_image,
    pair_image_files,
    setup_logging,
    warn_if_empty_mask,
    write_markdown_table,
)


RAW_DIR = "data/Raw_Images"
MASK_DIR = "data/Segmentation_Masks"
OUT_DIR = "eda/mask_coverage/images"
MD_OUT = "eda/mask_coverage/results.md"
LOW_FLAG = "\u26a0 Low"
HIGH_FLAG = "\u26a0 High"
NO_FLAG = "\u2014"


def save_coverage_histogram(coverages: list[float], out_path: Path) -> None:
    if not coverages:
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(coverages, bins=30, color="#4b8f8c", edgecolor="#1f3534")
    ax.axvline(5, color="#c84747", linestyle="--", linewidth=1, label="Low threshold")
    ax.axvline(90, color="#c89b2f", linestyle="--", linewidth=1, label="High threshold")
    ax.set_xlabel("Coverage %")
    ax.set_ylabel("Image Count")
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def coverage_flag(coverage: float) -> str:
    if coverage < 5.0:
        return LOW_FLAG
    if coverage > 90.0:
        return HIGH_FLAG
    return NO_FLAG


def main() -> None:
    setup_logging()
    out_dir = ensure_output_dir(OUT_DIR)
    pairs = pair_image_files(RAW_DIR, MASK_DIR)

    rows: list[str] = []
    coverages: list[float] = []
    for pair in pairs:
        raw_img = load_raw_image(pair.raw_path)
        if raw_img is None:
            continue

        mask_arr = load_mask_array(pair.mask_path, target_size=raw_img.size, image_name=pair.image_stem)
        if mask_arr is None:
            continue

        warn_if_empty_mask(mask_arr, pair.image_stem)
        width, height = raw_img.size
        total_pixels = int(mask_arr.size)
        masked_pixels = int(np.count_nonzero(mask_arr != BACKGROUND_LABEL))
        coverage = (masked_pixels / total_pixels) * 100 if total_pixels else 0.0
        coverages.append(coverage)
        rows.append(
            "| {image} | {width} | {height} | {total} | {masked} | {coverage} | {flag} |".format(
                image=pair.image_stem,
                width=width,
                height=height,
                total=format_int(total_pixels),
                masked=format_int(masked_pixels),
                coverage=format_percent(coverage),
                flag=coverage_flag(coverage),
            )
        )

    save_coverage_histogram(coverages, out_dir / "coverage_hist.png")

    write_markdown_table(
        MD_OUT,
        "| Image | W | H | Total Px | Masked Px | Coverage % | Flag |",
        "|-------|---|---|----------|-----------|------------|------|",
        rows,
    )
    logging.info("Wrote %d coverage rows to %s", len(rows), MD_OUT)


if __name__ == "__main__":
    main()
