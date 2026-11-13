# Project overview

- **PDIS-Net** = Plastic Debris Image Segmentation. BINUS undergrad thesis (Data Science + Computer Science team).
- Thesis title: "Segmentasi Semantik Sampah Plastik Terapung pada Citra Udara Berbasis Deep Learning".
- Task: binary semantic segmentation (plastic vs background) on drone photos of Dal Lake.
- Dataset: FloPWD 2025, 2.002 photos 1280×720 + hand-drawn masks (`data/raw/`).

## Repo layout
- `notebooks/<NN>-<arch>-<backbone>-<init>/vX.ipynb` one folder per run. Templates: `notebooks/v2.ipynb` (normal),
  `v3.ipynb` / `v4.ipynb` (Optuna). Kaggle copies in `notebooks/.kaggles/`.
- `results/<run>/<version>/` test_metrics.json, history.csv, split_*.csv, samples.png.
- `model/<run>/<version>/best.pth` (Git LFS) + `model/README.md` leaderboard (`python model/build_index.py`).
- `xai/02-segformer-mitb3-imagenet/v4/` Seg-Eigen-CAM pipeline + summary.
- `eda/scripts/` generic EDA scripts (paths point at `data/Raw_Images`, not `data/raw/...`, so they need path edits).
- `data/clean/` curriculum stage 1: 94 bad-label photos set aside, `manifest.csv` = per-photo split for all 2.002.
- `deployment/server` FastAPI (+ Gradio /ui), onion architecture, weights from HF `adamantix/pdisnet-weights`.
  `deployment/web` Next.js front end. The old Streamlit client is in `.archive/deployment/client`.
- `.archive/` everything from before the 3x3 grid restart (DINOv3, COSNet, old U-Net/SegFormer).

## Runs (comparison grid, all same split, 40 epochs, test = 301 photos)
- Best: `02-segformer-mitb3-imagenet` v1 0.8210 mIoU; after Optuna `v4-final` 0.8320 (80 epochs, no early stop).
- Pretraining matters most: SegFormer MiT-B3 from scratch 0.4725 vs ImageNet 0.8210.
- Aerial 0.8140, ADE20K 0.8077, drone 0.7809: none beat plain ImageNet.
- MiT-B5 0.8087, MiT-B0 0.7552. DeepLabV3+ MiT-B3 0.8092, U-Net MiT-B3 0.7918.
- Seed noise about ±0.01 mIoU, so gaps < 0.02 are treated as ties.
- Full table: `model/README.md`.
