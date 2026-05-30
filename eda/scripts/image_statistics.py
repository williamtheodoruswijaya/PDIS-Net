from __future__ import annotations

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import (
    ensure_output_dir,
    format_float,
    load_mask_array,
    load_raw_image,
    pair_image_files,
    setup_logging,
    warn_if_empty_mask,
    write_markdown_table,
)


RAW_DIR = "data/Raw_Images"
MASK_DIR = "data/Segmentation_Masks"
OUT_DIR = "eda/image_statistics/images"
MD_OUT = "eda/image_statistics/results.md"


def save_channel_histogram(histogram: np.ndarray, channel_name: str, color: str, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(np.arange(256), histogram, color=color, width=1.0)
    ax.set_xlabel(f"{channel_name} Pixel Value")
    ax.set_ylabel("Pixel Count")
    ax.set_xlim(0, 255)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    setup_logging()
    out_dir = ensure_output_dir(OUT_DIR)
    pairs = pair_image_files(RAW_DIR, MASK_DIR)

    channel_histograms = {
        "R": np.zeros(256, dtype=np.int64),
        "G": np.zeros(256, dtype=np.int64),
        "B": np.zeros(256, dtype=np.int64),
    }
    rows: list[str] = []

    for pair in pairs:
        raw_img = load_raw_image(pair.raw_path)
        if raw_img is None:
            continue

        raw_arr = np.array(raw_img)
        means = raw_arr.mean(axis=(0, 1))
        stds = raw_arr.std(axis=(0, 1))
        _mins = raw_arr.min(axis=(0, 1))
        _maxs = raw_arr.max(axis=(0, 1))

        for index, channel in enumerate(("R", "G", "B")):
            channel_histograms[channel] += np.bincount(
                raw_arr[:, :, index].ravel(),
                minlength=256,
            )

        mask_arr = load_mask_array(pair.mask_path, target_size=raw_img.size, image_name=pair.image_stem)
        if mask_arr is None:
            continue

        warn_if_empty_mask(mask_arr, pair.image_stem)
        labels, counts = np.unique(mask_arr, return_counts=True)
        dominant_label = int(labels[int(np.argmax(counts))]) if labels.size else ""

        rows.append(
            "| {image} | {r_mean} | {g_mean} | {b_mean} | {r_std} | {g_std} | {b_std} | {unique} | {dominant} |".format(
                image=pair.image_stem,
                r_mean=format_float(float(means[0])),
                g_mean=format_float(float(means[1])),
                b_mean=format_float(float(means[2])),
                r_std=format_float(float(stds[0])),
                g_std=format_float(float(stds[1])),
                b_std=format_float(float(stds[2])),
                unique=int(labels.size),
                dominant=dominant_label,
            )
        )

    save_channel_histogram(channel_histograms["R"], "Red", "#c84b4b", out_dir / "r_brightness_hist.png")
    save_channel_histogram(channel_histograms["G"], "Green", "#4b8f55", out_dir / "g_brightness_hist.png")
    save_channel_histogram(channel_histograms["B"], "Blue", "#4b6fb8", out_dir / "b_brightness_hist.png")

    write_markdown_table(
        MD_OUT,
        "| Image | R_mean | G_mean | B_mean | R_std | G_std | B_std | Unique Labels | Dominant Label |",
        "|-------|--------|--------|--------|-------|-------|-------|---------------|----------------|",
        rows,
    )
    logging.info("Wrote %d image statistic rows to %s", len(rows), MD_OUT)


if __name__ == "__main__":
    main()
