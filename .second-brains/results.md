# Results (Bab 4 material)

All: per-image mIoU, threshold 0.5, same 301 test photos (unless noted). Source: `results/<run>/<ver>/test_metrics.json`
(v4 uses its `per_image_t05` block). Runs 16/17 live flat at `results/<run>-v1/`.

## Full leaderboard

| # | Run | Ver | mIoU | fg IoU | Dice | mPA |
|---|---|---|---|---|---|---|
| 02 | SegFormer MiT-B3 ImageNet | **v4-final** | **0.8320** | 0.6926 | 0.7839 | 0.9138 |
| 02 | 〃 | v1-80ep-poly | 0.8258 | 0.6828 | 0.7798 | 0.9124 |
| 02 | 〃 | v1 (baseline) | 0.8210 | 0.6746 | 0.7720 | 0.8975 |
| 02 | 〃 | v3 (Optuna 12) | 0.8177 | 0.6670 | 0.7620 | 0.9095 |
| 02 | 〃 | curriculum A s42 | 0.8169 | 0.6653 | 0.7611 | 0.8974 |
| 02 | 〃 | clean-stage1 (n=290) | 0.8162 | 0.6540 | 0.7524 | 0.9086 |
| 04 | SegFormer MiT-B3 aerial | v1 | 0.8140 | 0.6595 | 0.7588 | 0.9022 |
| 13 | DeepLabV3+ MiT-B3 ImageNet | v2 | 0.8092 | 0.6495 | 0.7470 | 0.8908 |
| 07 | SegFormer MiT-B5 ImageNet | v1 | 0.8087 | 0.6501 | 0.7483 | 0.8886 |
| 05 | SegFormer MiT-B3 ADE20K | v1 | 0.8077 | 0.6499 | 0.7469 | 0.9006 |
| 02 | 〃 | curriculum B s43 | 0.8048 | 0.6428 | 0.7401 | 0.8853 |
| 02 | 〃 | v1-80ep (no sched) | 0.8005 | 0.6367 | 0.7354 | 0.9082 |
| 03 | U-Net MiT-B3 ImageNet | v1 | 0.7918 | 0.6128 | 0.7125 | 0.8666 |
| 17 | DeepLabV3+ ResNet101 ImageNet | v1 | 0.7816 | 0.6002 | 0.6999 | n/a |
| 02 | 〃 | v4 (Optuna 25, early-stopped) | 0.7810 | 0.6011 | 0.6988 | 0.9069 |
| 06 | SegFormer MiT-B3 drone | v1 | 0.7809 | 0.6001 | 0.6996 | 0.8822 |
| 10 | SegFormer-head ResNet34 ImageNet | v1 | 0.7801 | 0.5969 | 0.6950 | 0.8741 |
| 14 | DeepLabV3+ ResNet34 ImageNet | v2 | 0.7753 | 0.5999 | 0.7016 | 0.8824 |
| 09 | U-Net ResNet34 ImageNet | v1 | 0.7677 | 0.5694 | 0.6681 | 0.8705 |
| 12 | SegFormer MiT-B0 ImageNet | v2 | 0.7552 | 0.5521 | 0.6509 | 0.8725 |
| 16 | DeepLabV3+ ResNet50 ImageNet | v1 | 0.7533 | 0.5482 | 0.6470 | n/a |
| 11 | SegFormer-head ResNet34 raw | v2 | 0.6535 | 0.3779 | 0.4580 | 0.8274 |
| 08 | U-Net ResNet34 raw | v1 | 0.6494 | 0.3464 | 0.4427 | 0.8346 |
| 15 | DeepLabV3+ ResNet34 raw | v2 | 0.5867 | 0.2727 | 0.3562 | 0.8237 |
| 01 | SegFormer MiT-B3 raw | v1 | 0.4725 | 0.1404 | 0.1841 | 0.6958 |

v4-final extras: precision 0.7816, recall 0.8515, bg IoU 0.9715, best val mIoU 0.8344 (epoch 80/80).

## Table A — pretraining (SegFormer MiT-B3, fixed everything else)

| init | mIoU |
|---|---|
| raw (01) | 0.4725 |
| ImageNet cls (02 v1) | **0.8210** |
| aerial tree-cover (04) | 0.8140 |
| ADE20K seg (05) | 0.8077 |
| drone seg (06) | 0.7809 |

→ +0.35 from pretraining at all; no domain-specific init beats ImageNet.

## Table B — raw vs ImageNet across encoders/decoders

| | raw | ImageNet | Δ |
|---|---|---|---|
| SegFormer + MiT-B3 | 0.4725 | 0.8210 | +0.349 |
| SegFormer-head + ResNet34 | 0.6535 | 0.7801 | +0.127 |
| U-Net + ResNet34 | 0.6494 | 0.7677 | +0.118 |
| DeepLabV3+ + ResNet34 | 0.5867 | 0.7753 | +0.189 |

→ transformer encoder collapses from scratch on 1400 imgs (no locality inductive bias); CNNs degrade less.

## Table C — decoder × encoder (ImageNet)

| | U-Net | DeepLabV3+ | SegFormer All-MLP |
|---|---|---|---|
| MiT-B3 | 0.7918 (03) | 0.8092 (13) | **0.8210** (02) |
| ResNet34 | 0.7677 (09) | 0.7753 (14) | 0.7801 (10) |

→ SegFormer head wins on both encoders; MiT-B3 > ResNet34 for every decoder (~+0.02–0.04).

## Table D — encoder size

| SegFormer MiT | params | mIoU |
|---|---|---|
| B0 (12) | ~3.8 M | 0.7552 |
| B3 (02) | ~47 M | **0.8210** |
| B5 (07) | ~85 M | 0.8087 |

DeepLabV3+ ResNet: R34 0.7753, R50 0.7533, R101 0.7816 → no monotone gain with depth.

## Table E — improving run 02

| Version | Change | mIoU | Δ vs v1 |
|---|---|---|---|
| v1 | baseline 40 ep, patience 8, no sched | 0.8210 | — |
| v1-80ep | 80 ep, patience 8, no sched (stopped ep 33) | 0.8005 | −0.021 |
| v1-80ep-poly | 80 ep, no early stop, PolyLR, baseline hparams | 0.8258 | +0.005 |
| v3 | Optuna 12 trials | 0.8177 | −0.003 |
| v4 | Optuna 25 trials, final run early-stopped at ep 16 | 0.7810 | −0.040 |
| **v4-final** | v4 trial-15 hparams, 80 ep, no early stop, PolyLR | **0.8320** | **+0.011** |
| clean-stage1 | 94 noisy photos removed | 0.8087 @301 / 0.8162 @290 | −0.012 / −0.009 (vs 0.8250 @290) |
| curriculum A | clean→all at ep 21, seed 42 | 0.8169 | −0.004 (tie) |
| curriculum B | same, seed 43 | 0.8048 | −0.016 (worse) |

Key decomposition: schedule + 80 ep alone (v1-80ep-poly) = +0.005; tuned hparams on top (v4-final) = another +0.006.

Paired bootstrap (10 000 resamples, 95% CI, from README — **not reproducible from repo files**, see gotchas):
v4-final − v1 = +0.011 (+0.002 to +0.019); A − v1 = −0.004 (−0.010 to +0.001); B − v1 = −0.016 (−0.024 to −0.010).
Seed noise ≈ ±0.01 (A vs B differ by 0.012) → project treats |Δ| < 0.02 as a tie.

## Table F — XAI faithfulness (v4-final, `xai/02-segformer-mitb3-imagenet/v4/xai_summary.json`)

| | value |
|---|---|
| Images tested (GT>0 & pred>0) | 219 |
| Plastic prediction kept after deleting **hottest** 50% | **20.3%** |
| … after deleting **coldest** 50% | 65.0% |
| Images where hot-delete hurts more | 204 / 219 (93.2%) |
| Reproduced mIoU in XAI notebook | 0.832 (matches) |

Per-image fg IoU / gt% / pred% in `xai/.../v4/per_image.csv` (best/worst grids: `v4-final_best.png`, `v4-final_worst.png`).

## Archived pre-grid experiments (different split/metric — use only as history)

U-Net++ IoU 0.56, U-Net IoU 0.67, SegFormer-B3 mIoU 0.81, EoMT-DINOv3-L (ADE) mIoU 0.7916 (fg IoU 0.615),
CosNet from scratch fg IoU 0.437 / mIoU 0.694.

## Figures available

- `results/02.../v4-final/overlays.png` (README hero), `samples.png`, `curves.png`
- `results/02.../v3|v4/hpo_history.png`, `hpo_importance.png`, `hpo_slice.png`
- `results/<run>/<ver>/samples.png` for every run
- `xai/02.../v4/v4-final_samples.png`, `_best.png`, `_worst.png`
- `data/clean/audit/*.jpg` (label-audit examples), `eda/overlay/samples/*.png`
- `deployment/server/docs/architecture.png` (onion diagram)
