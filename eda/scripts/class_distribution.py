from __future__ import annotations

import logging
from collections import Counter, defaultdict
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
OUT_DIR = "eda/class_distribution/images"
MD_OUT = "eda/class_distribution/results.md"
CLASS_NAMES = {BACKGROUND_LABEL: "Background"}


def class_name(class_id: int) -> str:
    return CLASS_NAMES.get(class_id, f"Class_{class_id}")


def save_distribution_chart(class_counts: Counter[int], total_pixels: int, out_path: Path) -> None:
    if not class_counts or total_pixels == 0:
        return

    class_ids = sorted(class_counts)
    labels = [f"{class_id} - {class_name(class_id)}" for class_id in class_ids]
    percentages = [(class_counts[class_id] / total_pixels) * 100 for class_id in class_ids]

    height = max(4, 0.35 * len(class_ids))
    fig, ax = plt.subplots(figsize=(10, height))
    ax.barh(labels, percentages, color="#4878a8")
    ax.set_xlabel("% of Dataset")
    ax.set_ylabel("Class")
    ax.grid(axis="x", alpha=0.25)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    setup_logging()
    out_dir = ensure_output_dir(OUT_DIR)
    pairs = pair_image_files(RAW_DIR, MASK_DIR)

    class_counts: Counter[int] = Counter()
    appears_in: defaultdict[int, int] = defaultdict(int)
    total_pixels = 0

    for pair in pairs:
        raw_img = load_raw_image(pair.raw_path)
        target_size = raw_img.size if raw_img is not None else None
        mask_arr = load_mask_array(pair.mask_path, target_size=target_size, image_name=pair.image_stem)
        if mask_arr is None:
            continue

        warn_if_empty_mask(mask_arr, pair.image_stem)
        labels, counts = np.unique(mask_arr, return_counts=True)
        total_pixels += int(mask_arr.size)
        per_image_counts = dict(zip((int(label) for label in labels), (int(count) for count in counts)))
        for class_id, count in per_image_counts.items():
            class_counts[class_id] += count
            appears_in[class_id] += 1

    save_distribution_chart(class_counts, total_pixels, out_dir / "class_distribution.png")

    rows = []
    for class_id in sorted(class_counts):
        percentage = (class_counts[class_id] / total_pixels) * 100 if total_pixels else 0.0
        rows.append(
            "| {class_id} | {name} | {pixels} | {percent} | {appears} |".format(
                class_id=class_id,
                name=class_name(class_id),
                pixels=format_int(class_counts[class_id]),
                percent=format_percent(percentage),
                appears=format_int(appears_in[class_id]),
            )
        )

    write_markdown_table(
        MD_OUT,
        "| Class ID | Class Name | Total Pixels | % of Dataset | Appears In (images) |",
        "|----------|------------|--------------|--------------|---------------------|",
        rows,
    )
    logging.info("Wrote %d class rows to %s", len(rows), MD_OUT)


if __name__ == "__main__":
    main()
