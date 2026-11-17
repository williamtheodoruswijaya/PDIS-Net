# Thesis status + decisions log

Read with `README.md`. Updated 6 Nov 2026.

## Where the thesis lives

- **Team (group skripsi, BINUS, "Proposal Skripsi Non Kelas"):** Elena Nathanielle Budiman Angkawi (DS),
  Felicia Audrey Tanujaya (DS), William Theodorus Wijaya (CS). Title: *Segmentasi Semantik Sampah Plastik Terapung
  pada Citra Udara Berbasis Deep Learning*.
- **Source of truth = the team's Word file** (`THESIS v1`). We never edit Word directly.
- **Proposed changes live in the diff artifact:** https://claude.ai/artifact/VaPYGxN2tZDd9y7u4D41mD
  (since 12 Nov rebuilt by another session as "THESIS live (SharePoint 12 Nov).pdf → proposed", with fold/hint
  sections; anchors `#bab1` … `#bab5`, `#refs`). **Other sessions publish to it too: always build on the latest
  version** (a stale publish is refused and hands over the live source to merge). It also serves `pdf/thesis-v1-lengkap.pdf`
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
- **Don't name the 12 label–mask mismatches** (8 "yes"/empty, 4 "no"/plastic) in the thesis (team, 12 Nov).
  Details stay in `data/clean/README.md` for sidang questions.

## Voice sample (user's own rewrite, 12 Nov — "nanti style wordingnya seperti ini")

> Mask pada dataset tidak semuanya bernilai 0 dan 255, sebagian kecil piksel memiliki nilai yang berada tepat di
> antara 0 dan 255. Hal ini dikarenakan data mask yang di anotasi secara manual dari sumber dataset kita. Oleh karena
> itu, mask diubah menjadi biner dengan threshold 127. Piksel dengan nilai di atas 127 diberi nilai 1 sebagai plastik,
> sedangkan piksel lainnya diberi nilai 0 yang merupakan label untuk latar belakang. Hal ini dilakukan supaya seluruh
> mask hanya berisi nilai 0 dan 1. Selain itu, label "yes" dan "no" pada dataset diubah menjadi kolom has_plastic,
> yang menunjukkan apakah sebuah citra mengandung plastik atau tidak. Kolom ini kemudian digunakan hanya untuk
> stratifikasi pada saat pembagian data, sedangkan model utama tetap dilatih menggunakan mask sebagai ground truth.

Observed in this sample (follow these; confirm before turning them into hard rules): explain the cause in its own
sentence ("Hal ini dikarenakan …"), then the step ("Oleh karena itu, …"), then the purpose ("Hal ini dilakukan
supaya …"); "tidak semuanya" over "tidak seluruhnya"; "yang merupakan …"; "kemudian", "pada saat", "tetap" as
connectors; one step per sentence. Watch for: "kita" (informal, use "peneliti"/"pembuat *dataset*") and "di anotasi"
→ "dianotasi".

## Decisions log

| Date | Decision |
|---|---|
| 6 Nov | 4.6 intro: definition of Seg-Eigen-CAM + method steps removed; points to 2.1.23 (theory, cited) and 3.6.3 (method). 3.6.3 now says the gradient is taken on the predicted plastic area |
| 6 Nov | **4.6.1 Uji Kesesuaian Heatmap (deletion test) removed** (team: too advanced). Also removed from 2.1.23, 3.6.3, Bab 5 and Daftar Pustaka (Petsiuk). 4.6.2 → 4.6.1 Hasil, 4.6.3 → 4.6.2 Keterbatasan |
| 6 Nov | Tabel 4.1 = RTX 3050 laptop (Intel Core i5-11400H 6c/12t, RTX 3050 Laptop GPU 4 GB, 16 GB RAM; OS still to confirm). Original "4 GB tidak mencukupi" sentence kept (true for this PC; model_summary: ~1,6 GB fwd/bwd per 512×512 image). The AMD laptop (Ryzen 7 8840HS + Radeon 780M) is no longer listed |
| 17 Nov | **4.4.2 rewritten without early stopping (user's call).** Tabel 4.13 (0,7810) and the 0,8005 row go; the comparison is model awal 0,8210 (40 ep, LR tetap) vs hyperparameter awal + Poly 80 ep 0,8258 vs model akhir 0,8320. All gaps < 0,02 → write "setara"; no "scheduler naik besar" claim. Final model's precision 0,7816 < model awal 0,7847, so don't say "precision lebih tinggi" vs model awal. Gambar 4.3 → only the scheduler run (`results/02-.../v1-80ep-poly/curves.png`). Stability backup: val mIoU moves ~0,001/epoch in the last 10 epochs with Poly vs ~0,008 with constant LR (history.csv) |
| after 16 Nov | Diff v38, 4.4 on the newest Word. Team kept **Tabel 4.13** (0,8210 → 0,7810) and its own wording; bridge sentence + "Model akhir" paragraph + LR rationale are typed in. Left in 4.4: Y-01 (4.4.2 opening is a broken sentence, and Tabel 4.13 is never explained → one sentence about early stopping at epoch ke-16) and X-07 (duplicate "Tahap optimasi hanya dilakukan" paragraph). Tables are NOT renumbered (4.13 stays). M-04 and R-01 typed in. Sidang prep: why 0,8005 < 0,8210 with the same settings (early stopping fires at a different epoch because validation jumps); why not a small LR from the start (slow learning; smallest-encoder-LR trials scored lowest) |
| 16 Nov | **4.4 simplified (team call), diff v37, base = Word 16 Nov.** 4.4.1 no longer narrates the early-stopped retrain (0,7810): Tabel 4.13 and that paragraph are removed, the searched hyperparameter goes straight into the 80-epoch run with the Learning Rate Scheduler (4.4.2). One search only in the text (25 trial). Later tables renumber (4.14→4.13 …). LR highlight wording agreed as safe: "model tetap dapat dilatih dengan learning rate yang besar di awal, tetapi membutuhkan learning rate yang kecil di akhir" — NOT "membutuhkan LR besar di awal" (Tabel 4.12: best decoder LR 3,38e-5 is ~9× below nilai awal; both scheduler-comparison runs start at the same LR). Backup fact: 5 trials with encoder LR < 5e-6 scored 0,7554–0,7909 vs 0,7844–0,8136 for the other 14. The 0,7810 run stays in the public repo (model/README.md, v4). Another session maintains the diff too (S4-xx, H-xx hunks; BACKUP-4.4-trimmed.md) |
| 13 Nov | **Team rule: keep it simple.** In the diff, only flag real errors (wrong number, contradiction with what was run or with another chapter). No wording/detail suggestions unless asked. Diff v28: Bab 4 trimmed to F-04 ("15 trial" → 14, "v1" ×2) and S-01 (4.7/4.8 titles swapped); 4.9 still placeholder, Bab 5 missing. Bab 4 numbers, Gambar 4.2 and the val-mIoU claim re-verified against the repo. Bab 1–3 still carry the old-experiment leftovers (see diff hunks A-, B2-, B3-, T-) |
| 13 Nov | Diff artifact v27 synced to the team's Word (THESIS_v1.docx uploaded 13 Nov) for Bab 4.2–4.4. Typed in already: 4.3 raw-encoder LR reason, 4.3.2 "lokalitas", 4.3.3 two-groups reason, 4.2.3 normalisation reason. Proposed: 4.4.1 pruner example (trial 14: 0,7648 < median 0,7682) + what the 4 hyperparameters do, "15 trial" → 14, no "v1", "pada setiap epoch-nya" fix, Tabel 4.13 row 3, 4.4.2 LR finding (no "needs high LR at start"), pos_weight theory in 2.1.21.1 (Xie & Tu 2015; PyTorch docs to check) |
| 6 Nov | 4.6 heatmap averages (0,561/0,215/0,467/0,236), img1454 limitation and the 1×1-kernel sentence removed. New limitation sentence: heatmap faithfulness not tested quantitatively |

The deletion-test code still exists in the repo (`xai/02-segformer-mitb3-imagenet/v4/[fix]SEGEIGENCAM_pipeline_v4_final.ipynb`,
cell 6 `faithfulness`, results in `xai_summary.json`: 219 photos, 20,3% vs 65,0%, 204/219). It's fine as backup
material for sidang questions, just not in the text.

## Open items (from the local second brain)

- Team decisions Q1–Q5 in `REVISI-bab1-3-before-after.md` §7 (RM → 5 items, drop Focal Loss, near-duplicate
  limitation, UAT method, source of Gambar 1.2).
- 4.9 UAT / evaluasi aplikasi + its Bab 5 sentence still a placeholder.
- Bootstrap CIs come from the local note `EVAL-02-segformer-v4-hpo.md`, not a repo file (and Bab 4 dropped CIs on 5 Nov).
