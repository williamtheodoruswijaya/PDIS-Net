# AGENTS.md — Exploratory Data Analysis for Semantic Segmentation

## Overview

This document defines the full scope, structure, task specifications, and output conventions
for conducting an Exploratory Data Analysis (EDA) on a semantic segmentation dataset.

**All EDA work lives entirely inside the `eda/` folder.**

Primary goals:
1. Visually verify how well segmentation masks align with raw images via overlay blending
2. Run standard segmentation-specific EDA analyses
3. Qualitatively assess mask detail and coverage using agent vision (no Python)
4. Produce simple, table-only markdown reports for every analysis

---

## Repository Structure (Reference)

```
├───data
│   ├───Raw_Images               ← Source raw images
│   └───Segmentation_Masks       ← Source segmentation masks
├───demo
│   └───...
├───eda                          ← ALL EDA work lives here (agent creates this)
├───model
│   ├───20260105 - Unet (IOU=0.67)
│   ├───20261104 - Unet++ (IOU=0.56)
│   ├───20261205 - Segformer (mIoU=0.81)
│   ├───20261305 - DinoV3 (mIoU=0.7916)
│   └───20262405 - Segformer RAW (mIoU=0.55)
├───notebooks
│   ├───dinov3
│   ├───segformer
│   └───u-net
└───results
    ├───dinov3
    └───segformer
        └───RAW
```

---

## EDA Folder Layout (Agent Must Create)

The agent MUST scaffold and populate the following structure:

```
eda/
├── overlay/
│   ├── images/                        # Blended overlay output images
│   └── results.md                     # Table-only markdown
├── class_distribution/
│   ├── images/                        # Bar/pie chart plots
│   └── results.md
├── mask_coverage/
│   ├── images/                        # Per-image coverage heatmaps
│   └── results.md
├── image_statistics/
│   ├── images/                        # Brightness/contrast histograms
│   └── results.md
├── boundary_complexity/
│   ├── images/                        # Edge/contour overlays
│   └── results.md
├── class_cooccurrence/
│   ├── images/                        # Co-occurrence matrix heatmap
│   └── results.md
├── mask_quality/
│   ├── assessment.md                  # Agent vision assessment (NO Python)
│   └── mask_improvement_guide.md      # Per-image improvement instructions
└── scripts/
    ├── overlay.py
    ├── class_distribution.py
    ├── mask_coverage.py
    ├── image_statistics.py
    ├── boundary_complexity.py
    └── class_cooccurrence.py
```

> Additional analysis outputs that do not fit existing categories go into a new
> subfolder under `eda/` (e.g., `eda/aspect_ratio/`, `eda/color_analysis/`).

---

## Task 1 — Mask Overlay Visualization (Priority Task)

### Objective

Visually confirm mask-image alignment by rendering each segmentation mask directly
**on top of** its corresponding raw image with a lowered opacity, so both the annotation
and the underlying scene are visible simultaneously.

---

### Script: `eda/scripts/overlay.py`

**Input paths (configurable at top of script):**

```python
RAW_DIR   = "data/Raw_Images"
MASK_DIR  = "data/Segmentation_Masks"
OUT_DIR   = "eda/overlay/images"
MD_OUT    = "eda/overlay/results.md"
ALPHA     = 0.45     # mask opacity: 0.0 = fully transparent, 1.0 = fully opaque
COLORMAP  = "tab20"  # matplotlib colormap applied to mask class labels
```

**Processing steps (per image pair):**

1. Iterate all files in `RAW_DIR`; match to mask in `MASK_DIR` by filename stem
   (case-insensitive, extension-agnostic — e.g., `img_001.jpg` ↔ `img_001.png`)
2. Log a warning and skip if no matching mask is found
3. Convert raw image → RGBA
4. Apply a colormap to the mask (map each integer class label to an RGB color via
   `matplotlib.cm.get_cmap(COLORMAP)`) → RGBA colored mask
5. Set mask layer alpha channel to `int(255 * ALPHA)` uniformly
6. Composite: `PIL.Image.alpha_composite(raw_rgba, mask_rgba)`
   — mask sits **on top**, raw image shows through beneath
7. Save composite to `eda/overlay/images/<stem>_overlay.png`

**Reference blending function:**

```python
from PIL import Image
import numpy as np
import matplotlib.cm as cm

def apply_colormap(mask_arr: np.ndarray, cmap_name: str = "tab20") -> np.ndarray:
    """Map integer class labels to RGBA uint8 array."""
    norm = mask_arr.astype(np.float32) / max(mask_arr.max(), 1)
    rgba = cm.get_cmap(cmap_name)(norm)          # (H, W, 4) float [0,1]
    return (rgba * 255).astype(np.uint8)

def overlay_mask_on_image(
    raw_img: Image.Image,
    mask_img: Image.Image,
    alpha: float = 0.45,
    cmap_name: str = "tab20",
) -> Image.Image:
    raw_rgba  = raw_img.convert("RGBA")
    mask_arr  = np.array(mask_img.convert("L"))
    mask_rgba = Image.fromarray(apply_colormap(mask_arr, cmap_name), mode="RGBA")
    mask_rgba = mask_rgba.resize(raw_rgba.size, Image.NEAREST)
    r, g, b, a = mask_rgba.split()
    a = a.point(lambda p: int(255 * alpha))
    mask_rgba = Image.merge("RGBA", (r, g, b, a))
    return Image.alpha_composite(raw_rgba, mask_rgba)
```

---

### Markdown Output: `eda/overlay/results.md`

The script MUST generate `results.md` containing **only** the table below.
No title, no description, no section headers — just the table.

```markdown
| Image | Raw Image | Mask | Overlay |
|-------|-----------|------|---------|
| `image_001` | ![](../../../data/Raw_Images/image_001.png) | ![](../../../data/Segmentation_Masks/image_001.png) | ![](images/image_001_overlay.png) |
| `image_002` | ![](../../../data/Raw_Images/image_002.png) | ![](../../../data/Segmentation_Masks/image_002.png) | ![](images/image_002_overlay.png) |
```

- **Column order is fixed:** Image name → Raw → Mask → Overlay
- All image paths must be **relative** to the markdown file location
- One row per image pair; rows sorted by filename

---

## Task 2 — Standard Semantic Segmentation EDA

Each sub-task has its own script under `eda/scripts/`, outputs visuals to its
`eda/<analysis>/images/` folder, and writes a table-only `results.md`.

---

### 2a. Class Distribution — `eda/scripts/class_distribution.py`

**Compute:**
- For every unique integer label across all masks: total pixel count and percentage
  share of the whole dataset
- Also compute per-image class pixel counts
- Save a horizontal bar chart to `eda/class_distribution/images/class_distribution.png`

**`results.md` table:**

| Class ID | Class Name | Total Pixels | % of Dataset | Appears In (images) |
|----------|------------|--------------|--------------|---------------------|
| 0 | Background | 12,345,678 | 52.1% | 120 |
| 1 | Object | 8,901,234 | 37.6% | 118 |

> If class names are unknown, use `Class_<ID>` as placeholder.

---

### 2b. Mask Coverage per Image — `eda/scripts/mask_coverage.py`

**Compute:**
- Per image: total pixels, non-background masked pixels, coverage percentage
- Flag images: `⚠ Low` if coverage < 5%, `⚠ High` if coverage > 90%
- Save a coverage distribution histogram to `eda/mask_coverage/images/coverage_hist.png`

**`results.md` table:**

| Image | W | H | Total Px | Masked Px | Coverage % | Flag |
|-------|---|---|----------|-----------|------------|------|
| image_001 | 1280 | 720 | 921,600 | 450,230 | 48.9% | — |
| image_002 | 1280 | 720 | 921,600 | 43,000 | 4.7% | ⚠ Low |

---

### 2c. Image Statistics — `eda/scripts/image_statistics.py`

**Compute:**
- Per raw image: mean, std, min, max pixel values per RGB channel
- Per mask: unique label count, dominant label (by pixel count)
- Save per-channel brightness histograms to `eda/image_statistics/images/`

**`results.md` table:**

| Image | R_mean | G_mean | B_mean | R_std | G_std | B_std | Unique Labels | Dominant Label |
|-------|--------|--------|--------|-------|-------|-------|---------------|----------------|
| image_001 | 112.3 | 98.7 | 85.2 | 42.1 | 38.4 | 35.9 | 3 | 1 |

---

### 2d. Boundary Complexity — `eda/scripts/boundary_complexity.py`

**Compute:**
- Per mask per class: extract contours via `cv2.findContours`
- Metrics: contour count, total perimeter (px), total area (px²)
- Complexity score = `perimeter² / (4π × area)` — near 1.0 is circle-like (simple),
  high values indicate irregular/complex boundaries
- Save contour overlay images to `eda/boundary_complexity/images/<stem>_contours.png`

**`results.md` table:**

| Image | Class ID | Contour Count | Total Perimeter (px) | Total Area (px²) | Complexity Score |
|-------|----------|---------------|----------------------|-----------------|------------------|
| image_001 | 1 | 3 | 1,240 | 45,000 | 2.71 |

---

### 2e. Class Co-occurrence — `eda/scripts/class_cooccurrence.py`

**Compute:**
- For each class-pair `(A, B)`, count images where both appear simultaneously
- Produce a symmetric co-occurrence count matrix
- Save heatmap to `eda/class_cooccurrence/images/cooccurrence_heatmap.png`

**`results.md` table:**

| Class A | Class B | Co-occurring Images | % of Total Images |
|---------|---------|---------------------|-------------------|
| 0 | 1 | 95 | 79.2% |
| 1 | 2 | 40 | 33.3% |

---

## Task 3 — Mask Quality Assessment (Agent Vision, No Python)

### Objective

The agent MUST visually inspect each image-mask pair and produce a qualitative
assessment of mask accuracy and detail level. This is entirely agent-driven —
**no Python script is written or run for this task.**

Output files:
- `eda/mask_quality/assessment.md`
- `eda/mask_quality/mask_improvement_guide.md`

---

### Assessment Criteria

For each pair, the agent evaluates:

| Criterion | What to look for |
|-----------|-----------------|
| **Boundary Sharpness** | Do mask edges follow object silhouette tightly, or are they jagged / over-smoothed? |
| **Coverage Completeness** | Does the mask fully enclose the target, or are there internal holes and missed regions? |
| **False Positives** | Are background areas incorrectly labeled as foreground? |
| **False Negatives** | Are foreground object areas missing from the mask? |
| **Fine Detail Capture** | Are thin structures (wires, limbs, edges) annotated, or only coarse shapes? |
| **Cross-image Consistency** | Are similar objects annotated with the same level of detail across the dataset? |

---

### Output: `eda/mask_quality/assessment.md`

Table-only. No prose, no section headers.

```markdown
| Image | Boundary Sharpness | Coverage | False Positives | False Negatives | Detail Level | Overall |
|-------|-------------------|----------|-----------------|-----------------|--------------|---------|
| image_001 | Sharp | Complete | None | Minor gap (top-left corner) | High | ✅ Good |
| image_002 | Rough edges | Partial (~80%) | Background patch bottom-right | Large missed region (center) | Low | ❌ Poor |
| image_003 | Adequate | Complete | None | None | Medium | ⚠ Acceptable |
```

**Rating definitions:**

| Rating | Meaning |
|--------|---------|
| ✅ Good | Mask is usable as-is for training |
| ⚠ Acceptable | Minor issues; may introduce slight noise but still trainable |
| ❌ Poor | Mask needs re-annotation before use in training |

---

### How to Create Masks in More Detail (Agent's Role)

For every image rated ⚠ Acceptable or ❌ Poor, the agent MUST write a specific,
actionable improvement instruction in `eda/mask_quality/mask_improvement_guide.md`.

**Agent guidelines for writing improvement instructions:**
- Reference spatial location (quadrant, corner, center, top/bottom edge)
- Describe the structural feature that is missed or wrong
- Suggest the exact annotation action (expand, retrace, add stroke, remove region)
- Estimate approximate size/extent of the fix in pixels where possible

```markdown
| Image | Issue | Location | Recommended Fix |
|-------|-------|----------|-----------------|
| image_002 | Mask boundary sits ~15px inside the true object silhouette | Right side, full height | Expand mask boundary outward by 12–18px, tracing the actual object edge |
| image_002 | Background patch (≈50×40px) incorrectly labeled as foreground | Bottom-right quadrant | Erase and relabel as background (class 0) |
| image_005 | Thin rod (≈3–4px wide) completely missing from mask | Center-left diagonal | Annotate with 4px brush stroke along the full rod length |
| image_009 | Hollow interior left transparent inside the mask | Centroid of main object | Flood-fill the interior region with the correct class label |
```

> Be specific. The goal is for a human annotator to act directly on these
> instructions without needing to re-examine the raw image themselves.

---

## Output Folder Map

| Analysis | Script | Images → | Markdown → |
|----------|--------|----------|-----------|
| Overlay | `eda/scripts/overlay.py` | `eda/overlay/images/` | `eda/overlay/results.md` |
| Class Distribution | `eda/scripts/class_distribution.py` | `eda/class_distribution/images/` | `eda/class_distribution/results.md` |
| Mask Coverage | `eda/scripts/mask_coverage.py` | `eda/mask_coverage/images/` | `eda/mask_coverage/results.md` |
| Image Statistics | `eda/scripts/image_statistics.py` | `eda/image_statistics/images/` | `eda/image_statistics/results.md` |
| Boundary Complexity | `eda/scripts/boundary_complexity.py` | `eda/boundary_complexity/images/` | `eda/boundary_complexity/results.md` |
| Class Co-occurrence | `eda/scripts/class_cooccurrence.py` | `eda/class_cooccurrence/images/` | `eda/class_cooccurrence/results.md` |
| Mask Quality | *(agent vision — no script)* | *(none)* | `eda/mask_quality/assessment.md` |
| Mask Improvement | *(agent vision — no script)* | *(none)* | `eda/mask_quality/mask_improvement_guide.md` |

---

## General Coding Guidelines

- **Language:** Python 3.10+
- **Required libraries:** `Pillow`, `numpy`, `matplotlib`, `opencv-python`, `pandas`
- Install with: `pip install pillow numpy matplotlib opencv-python pandas`
- **All paths** are relative to the repository root
- **All scripts** must be runnable from the repository root:
  ```bash
  python eda/scripts/overlay.py
  python eda/scripts/class_distribution.py
  # etc.
  ```
- Match raw images to masks by **filename stem** (case-insensitive, extension-agnostic)
- On missing pairs: log a warning (`WARNING: No mask found for <file>`) and skip
- **Markdown files contain ONLY tables.** No titles, no descriptions, no prose.
- Save all intermediate figures at a minimum of **150 DPI**
- Image links in markdown must use **relative paths** from the markdown file location

---

## Do's and Don'ts

| ✅ Do | ❌ Don't |
|------|---------|
| Keep all EDA output inside `eda/` | Write any EDA output outside `eda/` |
| Use relative paths in markdown image links | Use absolute or system-level paths |
| Match images ↔ masks by filename stem | Assume directory sort order matches |
| Write only tables in `.md` files | Add prose, titles, or section headers to `.md` |
| Use agent vision for Task 3 (mask quality) | Write or run Python for Task 3 |
| Create new `eda/<name>/` subfolders for extra analyses | Dump extra outputs into an existing folder |
| Flag ⚠ Low / ⚠ High coverage images explicitly | Silently skip anomalous entries |
| Use `tab20` colormap to distinguish classes in overlays | Use single-color binary overlays |
| Log all skipped files with reason | Silently discard unmatched pairs |
