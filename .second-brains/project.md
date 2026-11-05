# Project overview

**PDIS-Net — Plastic Debris Image Segmentation.** Undergrad thesis, BINUS University.
Author/owner: William Theodorus Wijaya (GitHub `williamtheodoruswijaya`, HF `adamantix`).

## Task

Binary semantic segmentation of **floating plastic waste** in UAV (drone) photos of **Dal Lake** (Kashmir).
Input: RGB photo. Output: per-pixel mask, plastic (1) vs background (0). Downstream: coverage % →
cleanup-priority category (deployment).

## Dataset — FloPWD 2025 (Dal Lake Floating Plastic Waste Detection)

- 2002 RGB frames, **1280×720**, each with a hand-drawn binary mask (`imgN.jpg` ↔ `imgN_mask.png`).
- Two side CSVs: `Image_labels_Binary Classification Task.csv` (yes/no plastic) and
  `Mask_foreground_percentages_Regression Task.csv` (fg %).
- ~74% of photos are labelled "plastic present". Foreground is tiny on average → heavy class imbalance
  (handled via weighted CE + Dice).
- Frames come from **video** → many near-duplicates (neighbouring frames).
- Raw copy in `data/raw/` (never modified). The notebooks pull the original zip from Google Drive
  (`file_id = 114xnPVZtthHi4Bejzho33vGJSqb4-F8g`) via `gdown`.

## Split (the one every reported run uses)

- `train_test_split` ×2, `random_state=42`, `stratify=has_plastic`:
  test = 15% → **301**; val = 15/85 of the rest → **301**; train → **1400**.
- Persisted per photo in `data/clean/manifest.csv` (`split`, `status`, `category`, `fg_pct`, `biggest_blob_pct`).
- Near-duplicate leakage is a known property: **277 of 301 test photos have a neighbouring frame in train**
  (from `curriculum-learnings/leakage_check.py`). Must be acknowledged as a limitation in the thesis.
- ⚠️ `data/splits/` (1496/253/253, dHash-grouped) is a **different, older split that no reported run uses**. See gotchas.

## Label audit (`data/clean/`)

94 photos (4.7%) flagged as bad labels: `coarse_zone` 91 (img1199–1219, img1418–1487: one big zone drawn over
banks/fields) + `missing_mask` 3 (img96, img340, img772). Kept-but-noted: `rough_polygon` 30,
`yes_label_empty_mask` 5, `no_label_nonempty_mask` 4. Removed per split: train 65, val 18, test 11 →
clean set 1335/283/290. Audit overlay sheets in `data/clean/audit/`.

## Repo map

```
data/        raw FloPWD + clean manifest/zip + audit sheets (+ legacy data/splits/)
notebooks/   one folder per run: NN-arch-backbone-init/vX.ipynb ; templates v2 (train), v3/v4 (Optuna); .kaggles/
results/     per run/version: test_metrics.json, history.csv, split_*.csv, samples/curves/overlays png, optuna.db
model/       best.pth (LFS) + test_metrics.json ; build_index.py → model/README.md leaderboard ; add_mpa.py
xai/         Seg-Eigen-CAM notebooks + heatmaps for run 02 (v1, v4-final)
eda/         scripts: class_distribution, mask_coverage, boundary_complexity, image_statistics, class_cooccurrence, overlay
deployment/  server (FastAPI + Gradio, onion architecture, HF Space) ; web (Next.js client) ; upload/upload_weights.py
.archive/    pre-"3x3 grid restart" work: old U-Net/U-Net++/SegFormer/EoMT-DINOv3/CosNet notebooks + weights
```

Training environment: Google Colab T4 (Kaggle variants in `notebooks/.kaggles/`), outputs to
`Drive: THESIS/runs/<run_id>/<version>/`, then copied into `results/` + `model/`. ~1.8 h per 40-epoch run on T4.

## Timeline (from `.archive/model/history/` + git log)

| Date (2026) | Milestone |
|---|---|
| 04-11 | U-Net++ first try (IoU 0.56) |
| 05-01 | U-Net (IoU 0.67) |
| 05-12 | SegFormer-B3 (mIoU 0.81) |
| 05-13 | EoMT-DINOv3 ADE large (mIoU 0.7916) — archived |
| 05-24 | SegFormer raw (0.55) |
| 06-02 | CosNet from scratch (IoU 0.437) — archived |
| 09-22…24 | Grid restart with fixed split: run 01 raw 0.47, run 02 ImageNet 0.82, run 04 aerial 0.81 |
| ~10 | Runs 05–17, label cleaning, curriculum, Optuna v3/v4 |
| 10-23/24 | v4 Optuna (25 trials), per-image re-score |
| late 10 | v4-final 80 ep → **0.8320** (best) ; XAI on v4-final |
| ~11 | Deployment rewrite (onion arch FastAPI + Next.js) merged (PR #26) |
