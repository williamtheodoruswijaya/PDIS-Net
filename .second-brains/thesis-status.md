# Thesis status + decisions log

Read with `README.md`. Updated 6 Nov 2026.

## Where the thesis lives

- **Team (group skripsi, BINUS, "Proposal Skripsi Non Kelas"):** Elena Nathanielle Budiman Angkawi (DS),
  Felicia Audrey Tanujaya (DS), William Theodorus Wijaya (CS). Title: *Segmentasi Semantik Sampah Plastik Terapung
  pada Citra Udara Berbasis Deep Learning*.
- **Source of truth = the team's Word file** (`THESIS v1`). We never edit Word directly.
- **Proposed changes live in the diff artifact:** https://claude.ai/artifact/VaPYGxN2tZDd9y7u4D41mD
  ("THESIS v1.pdf → proposed", anchors `#bab1` … `#bab5`, `#refs`). It also serves `pdf/thesis-v1-lengkap.pdf`
  (125 pages, latest full PDF) and `pdf/sidang-pdis-net.pdf` (20 slides). Private: teammates need it shared.
- **The user's local second brain** (`.second-brain/`, singular, gitignored) is on Drive:
  `THESIS/.second-brain.zip`. Key files there: `PLAN-thesis-v1-revisi-dan-bab4.md` (27 Oct master plan, partly
  stale), `REVISI-bab1-3-before-after.md` (5 Nov, 65 BEFORE/AFTER items for Bab 1–3 + 19 Daftar Pustaka fixes),
  `REVIEW-bab4-v1-accuracy.md`, `DRAFT-bab4-4.4-4.6-model.md`, `DRAFT-bab4-4.7-4.8-aplikasi.md`,
  `cam_grid.py` (makes Gambar 4.5, **not in the repo**).
- Old proposal PDF (v0, 81 pages, Bab 1–3 only) has outdated method details from the archived notebooks
  (30 epochs, patience 5, BCE, ElasticTransform/GridDistortion/GaussNoise/CoarseDropout, Streamlit).

## Writing rules (thesis text)

- Formal Indonesian in the user's voice: use the `write-like-me` skill. "peneliti", "Hal ini dilakukan supaya …",
  "yang bernama", plain words, no bullets in body text, decimal comma, English terms in italics.
- **No version or notebook names in the text** (v1/v3/v4): "Model awal / Hasil pencarian pertama / kedua / Model akhir".
- **No citations in Bab 4** (team decision, 4 Nov). Definitions and their citations go in Bab 2, method in Bab 3.
- **0,02 rule:** mIoU gaps under 0,02 are written "setara" (single seed).
- Accuracy → **mPA**. Loss = weighted CE (0,3) + Dice (0,7), not BCE.
- **From the Seg-Eigen-CAM section onward (6 Nov): no derived or script-only numbers.** That means no heatmap
  averages, no per-photo % computed outside the repo. Describe heatmaps qualitatively from Gambar 4.5. Numbers in
  earlier sections that come from `results/` / `model/` stay.
- **Never claim anything about areas outside the predicted mask** from the heatmap. The gradient is zero there, so
  the colour means nothing: usually blue, but on img1454 the water outside the prediction was the hottest part.
  E.g. NOT "perahu berwarna biru jadi tidak berpengaruh". Standard phrase in the thesis: "*heatmap* hanya
  menjelaskan bagian yang diprediksi sebagai plastik". Avoid "memiliki nilai di dalam area prediksi" (confusing).

## Decisions log

| Date | Decision |
|---|---|
| 6 Nov | 4.6 intro: definition of Seg-Eigen-CAM + method steps removed; points to 2.1.23 (theory, cited) and 3.6.3 (method). 3.6.3 now says the gradient is taken on the predicted plastic area |
| 6 Nov | **4.6.1 Uji Kesesuaian Heatmap (deletion test) removed** (team: too advanced). Also removed from 2.1.23, 3.6.3, Bab 5 and Daftar Pustaka (Petsiuk). 4.6.2 → 4.6.1 Hasil, 4.6.3 → 4.6.2 Keterbatasan |
| 6 Nov | Tabel 4.1 = William's laptop (Ryzen 7 8840HS, Radeon 780M integrated, ~377 MB dedicated, shared with RAM). "4 GB" sentence replaced: integrated GPU + no CUDA support → training on Colab/Kaggle T4 |
| 6 Nov | 4.6 heatmap averages (0,561/0,215/0,467/0,236), img1454 limitation and the 1×1-kernel sentence removed. New limitation sentence: heatmap faithfulness not tested quantitatively |

The deletion-test code still exists in the repo (`xai/02-segformer-mitb3-imagenet/v4/[fix]SEGEIGENCAM_pipeline_v4_final.ipynb`,
cell 6 `faithfulness`, results in `xai_summary.json`: 219 photos, 20,3% vs 65,0%, 204/219). It's fine as backup
material for sidang questions, just not in the text.

## Open items (from the local second brain)

- Team decisions Q1–Q5 in `REVISI-bab1-3-before-after.md` §7 (RM → 5 items, drop Focal Loss, near-duplicate
  limitation, UAT method, source of Gambar 1.2).
- 4.9 UAT / evaluasi aplikasi + its Bab 5 sentence still a placeholder.
- Bootstrap CIs come from the local note `EVAL-02-segformer-v4-hpo.md`, not a repo file (and Bab 4 dropped CIs on 5 Nov).
