from __future__ import annotations

import logging
from collections import Counter
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import (
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
OUT_DIR = "eda/class_cooccurrence/images"
MD_OUT = "eda/class_cooccurrence/results.md"


def save_heatmap(classes: list[int], matrix: np.ndarray, out_path: Path) -> None:
    if not classes:
        return

    size = max(6, 0.4 * len(classes))
    fig, ax = plt.subplots(figsize=(size, size))
    im = ax.imshow(matrix, cmap="viridis")
    ax.set_xticks(np.arange(len(classes)))
    ax.set_yticks(np.arange(len(classes)))
    ax.set_xticklabels(classes, rotation=90)
    ax.set_yticklabels(classes)
    ax.set_xlabel("Class B")
    ax.set_ylabel("Class A")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Images")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    setup_logging()
    out_dir = ensure_output_dir(OUT_DIR)
    pairs = pair_image_files(RAW_DIR, MASK_DIR)

    class_presence: Counter[int] = Counter()
    pair_counts: Counter[tuple[int, int]] = Counter()
    total_images = 0
    all_classes: set[int] = set()

    for pair in pairs:
        raw_img = load_raw_image(pair.raw_path)
        target_size = raw_img.size if raw_img is not None else None
        mask_arr = load_mask_array(pair.mask_path, target_size=target_size, image_name=pair.image_stem)
        if mask_arr is None:
            continue

        total_images += 1
        warn_if_empty_mask(mask_arr, pair.image_stem)
        classes = sorted(int(label) for label in np.unique(mask_arr))
        all_classes.update(classes)
        for class_id in classes:
            class_presence[class_id] += 1
        for class_a, class_b in combinations(classes, 2):
            pair_counts[(class_a, class_b)] += 1

    classes = sorted(all_classes)
    matrix = np.zeros((len(classes), len(classes)), dtype=np.int64)
    index_by_class = {class_id: idx for idx, class_id in enumerate(classes)}
    for class_id, count in class_presence.items():
        idx = index_by_class[class_id]
        matrix[idx, idx] = count
    for (class_a, class_b), count in pair_counts.items():
        idx_a = index_by_class[class_a]
        idx_b = index_by_class[class_b]
        matrix[idx_a, idx_b] = count
        matrix[idx_b, idx_a] = count

    save_heatmap(classes, matrix, out_dir / "cooccurrence_heatmap.png")

    rows = []
    for class_a, class_b in sorted(pair_counts):
        count = pair_counts[(class_a, class_b)]
        percentage = (count / total_images) * 100 if total_images else 0.0
        rows.append(
            "| {class_a} | {class_b} | {count} | {percent} |".format(
                class_a=class_a,
                class_b=class_b,
                count=format_int(count),
                percent=format_percent(percentage),
            )
        )

    write_markdown_table(
        MD_OUT,
        "| Class A | Class B | Co-occurring Images | % of Total Images |",
        "|---------|---------|---------------------|-------------------|",
        rows,
    )
    logging.info("Wrote %d co-occurrence rows to %s", len(rows), MD_OUT)


if __name__ == "__main__":
    main()
