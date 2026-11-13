"""Recompute the plastic-coverage numbers quoted in thesis Bab 4.2.1.

Run from the repo root:  python .second-brains/scripts/plastic_coverage_stats.py
Expected: mean all 5.4560, median non-empty 2.4406 (n = 1478), empty masks 524.
"""
from pathlib import Path

import numpy as np
from PIL import Image

MASK_DIR = Path("data/raw/Segmentation_Masks")

cov = []
for f in sorted(MASK_DIR.glob("*.png")):
    mask = np.array(Image.open(f).convert("L")) > 127  # same threshold as the notebooks
    cov.append(mask.mean() * 100)                       # % of the 1280x720 frame that is plastic

cov = np.array(cov)
plastic = cov[cov > 0]

print(f"images                     : {len(cov)}")
print(f"empty masks                : {(cov == 0).sum()}")
print(f"mean coverage, all images  : {cov.mean():.4f}%")
print(f"median coverage, all       : {np.median(cov):.4f}%")
print(f"images with plastic        : {len(plastic)}")
print(f"mean coverage, with plastic: {plastic.mean():.4f}%")
print(f"median, with plastic       : {np.median(plastic):.4f}%")
print(f"background : plastic pixels: {(100 - cov.mean()) / cov.mean():.2f} : 1")
