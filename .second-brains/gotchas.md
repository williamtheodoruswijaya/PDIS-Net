# Gotchas — check these before a claim goes into the draft

## Inconsistencies in the repo

1. **Two different splits documented.** `data/README.md` describes `data/splits/` = 1496/253/253 via dHash
   near-duplicate grouping + `StratifiedGroupKFold` (`pipelines/split.ipynb`, which **doesn't exist** in the repo).
   Every reported run uses the **1400/301/301 stratified `train_test_split`** (seed 42) instead. Bab 3 must describe
   the 1400/301/301 one. `data/README.md` is stale.
2. **Near-duplicate leakage is real:** 277/301 test photos have a neighbouring video frame in train
   (`leakage_check.py`). Scores are likely optimistic vs truly unseen scenes → limitation in Bab 5.
   `CFG["dup_hamming"]=5` exists in every notebook but is **never used** by the split.
3. **Deployed checkpoint:** root `README.md` says the deployed model is "an earlier SegFormer MiT-B3 (0.811)", but
   `deployment/server/README.md` + `core/entities/trained_models.py` point to **v4-final (0.832)**. Confirm with the
   user which is live on the HF Space before writing Bab 4 deployment.
4. **Run 16 missing from `model/README.md` leaderboard** — its files are flat (`model/16-deeplab-resnet50-imagenet-v1/`)
   instead of `<run>/<version>/`, so `build_index.py` skips it. Score: 0.7533. Run 17 is listed (0.7816).
5. **Runs 16/17 named "deeplab"** but the code is `smp.DeepLabV3Plus` → call them DeepLabV3+ in the thesis.
   They also lack `mpa` (nan).
6. **v4 metric:** v4.ipynb saved a dataset-level (pooled) score 0.8116; the comparable per-image score is **0.7810**
   (`per_image_t05`). Never cite 0.8116 next to the others.
7. **clean-stage1 has two numbers:** `test_metrics.json` = 0.8162 on its 290 clean test photos; README cites
   0.8087 on the full 301 (re-score not saved as a file). v1 on the same 290 = 0.8250 (README only).
8. **Bootstrap CIs** (v4-final − v1 = +0.011 [+0.002, +0.019]; curriculum A/B CIs) are in READMEs only — the
   bootstrap script/output is not in the repo. Either regenerate (needs per-image scores for v1 — only v4-final has
   `per_image.csv`) or cite as reported.
9. **Curriculum run C** (baseline, seed 43) still **pending** → the seed-noise argument rests on A vs B only.
10. **Notebook naming:** `notebooks/03-unet-mitb3/` vs `results/03-unet-mitb3-imagenet/`; weights file is
    `UNET_MITB3 Model.pth` not `best.pth`; run 03 came from an older notebook (same CFG, different code).
11. `notebooks/README.md` example names (`07-segformer-mitb3-imagenet`, `01-unet-resnet50-imagenet`) are stale.

## Methodological caveats to state honestly

- **Early stopping confound in the grid.** Recipe = 40 ep, patience 8, no LR schedule. Many runs stopped early:
  01 raw (13 ep, best 5), 06 drone (17/9), 12 MiT-B0 (14/6), 15 DLV3+-R34 raw (13/5), 16 DLV3+-R50 (20/12),
  v4 (16/8). v1-80ep vs v1-80ep-poly shows the schedule matters (+0.025). So "X < Y" in the grid means
  "under this fixed budget", not "X is intrinsically worse".
- **v4-final's +0.011 over v1** mixes 3 changes (tuned hparams, 80 vs 40 epochs, PolyLR). v1-80ep-poly isolates
  the latter two: +0.005 of the gain. Still under the 0.02 "tie" bar.
- **v4-final best epoch = 80/80**, val still rising → not converged; also no early stop means "best" is chosen on val
  each epoch (fine, test never used for selection).
- **HPO budget:** trials of 12 epochs on 1 seed; v4 recorded 25 of 30 planned trials.
- **Single seed (42)** for every grid run; seed noise ≈ ±0.01.
- **Resize to 512×512 squashes 16:9** frames; tiny litter may vanish (relevant to worst cases).
- Domain-init checkpoints differ in more than domain (aerial: 1024 px/10 cm; drone: no model card; ADE/aerial/drone
  also transfer the decoder while ImageNet doesn't) — not a perfectly controlled comparison.
- DeepLabV3+ MiT-B3 (13) uses a modified stage-4 (stride→dilation), pretrained weights never saw that.
- MiT-B0 shrinks the decoder too (256 vs 768) → "whole-model size", as the SegFormer paper defines B0–B5.

## Environment

- Cloud container: no GPU, LFS weights not pulled → can't re-run eval/XAI here. Work from saved JSON/CSV/PNG.
- `.second-brain/` (singular) is gitignored = the user's local notes (e.g. `bad-annotations.md` referenced in
  `data/clean/README.md`) — **not available** in the cloud clone.
