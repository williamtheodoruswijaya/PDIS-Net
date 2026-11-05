# Methods (Bab 3 material) — exact, from the notebooks

Source of truth: `notebooks/v2.ipynb` (train template), `notebooks/v3.ipynb` / `v4.ipynb` (Optuna),
`notebooks/02-segformer-mitb3-imagenet/v4-final.ipynb` (best model). Cell numbers below refer to v2.

## 1. Data pipeline

- Read both CSVs, rename to `image_name`, `presence`, `fg_pct`; inner-merge; `has_plastic = presence == "yes"`.
- Mask binarised `> 127`. Image BGR→RGB (cv2).
- Split: see `project.md` (1400/301/301, seed 42, stratified on `has_plastic`).
- Resize 1280×720 → **512×512** (aspect ratio NOT kept). ImageNet mean/std normalisation.
- **Train augmentation** (albumentations): HorizontalFlip 0.5, VerticalFlip 0.5, RandomRotate90 0.5,
  ShiftScaleRotate(shift 0.1, scale 0.2, rotate 30°, p 0.5), ColorJitter(0.2, 0.2, 0.2, hue 0.1, p 0.4).
  Eval: resize + normalise only.
- DataLoader: batch 4, shuffle train, `drop_last=True` on train.

## 2. Models (one-variable-at-a-time grid)

Three variables: **architecture/decoder**, **encoder (backbone)**, **pretraining init**.

| arch key | Implementation | Notes |
|---|---|---|
| `segformer` | HF `SegformerForSemanticSegmentation`, `num_labels=2`, `ignore_mismatched_sizes=True` | logits at 1/4 res → bilinear upsample to 512 |
| `segformer-smp` | `smp.Segformer(encoder, decoder_segmentation_channels=768)` | used to put the SegFormer All-MLP head on ResNet34 (runs 10, 11) |
| `unet` | `smp.Unet` | |
| `deeplab` | `smp.DeepLabV3Plus` (ASPP rates 12/24/36 + 1/4 skip) | MiT-B3 version needs stage-4 stride→dilation (caveat) |

Init options (`build_model`):

| init | Source checkpoint | What transfers |
|---|---|---|
| `raw` | random (`SegformerConfig` / `encoder_weights=None`) | nothing; encoder LR = decoder LR |
| `imagenet` | `nvidia/mit-b3` (or b0/b5) / smp imagenet | **encoder only** (decode head random) |
| `aerial` | `restor/tcd-segformer-mit-b3` (OAM-TCD tree cover, 10 cm/px, 1024 px) | encoder + full decoder (head already 2-class) |
| `ade` | `nvidia/segformer-b3-finetuned-ade-512-512` (ADE20K 150 cls) | encoder + decoder MLPs; classifier re-init |
| `drone` | `pablojrios/segformer-b3-finetuned-drones` (Semantic Drone Dataset, 24 cls, from nvidia/mit-b3) | encoder + decoder; classifier re-init |

Model size: SegFormer-MiT-B3 = **47.22 M params**, 42.75 GMACs @512 (`results/02.../v4-final/model_summary.txt`).
MiT-B0 ~3.8 M (decoder width 256), MiT-B5 ~85 M, UNet-R34 24.4 M, SegFormer-head-R34 25.0 M,
DeepLabV3+-R34 22.4 M, DeepLabV3+-MiT-B3 45.2 M.

## 3. Loss

- `pos_weight = neg/pos` pixel ratio estimated on 200 random train masks; CE class weights `[1, min(pos_weight, 50)]`.
- `L = w_dice · Dice(softmax[:,1], y) + w_ce · WeightedCE`, Dice smooth = 1.
- Default `w_dice=0.7, w_ce=0.3`.

## 4. Optimisation

- AdamW, two param groups: encoder `lr_encoder=1e-5`, decoder `lr_decoder=3e-4`, `weight_decay=1e-4`
  (raw init → encoder uses decoder LR).
- AMP (`torch.amp.autocast` + `GradScaler`). Seed 42 (`random`, `numpy`, `torch`, `cuda`).
- 40 epochs, early stopping patience 8 on **val mIoU**; best epoch checkpoint (`best.pth`) used for test.
- No LR scheduler in v1/v2 template. `v1-80ep-poly`, v4 and v4-final use `PolynomialLR(power=1.0)` = linear decay to 0.

## 5. Metrics (per-image, then averaged)

For each test image at threshold 0.5 on softmax[:,1]: TP/FP/FN/TN → 
fg IoU = TP/(TP+FP+FN), bg IoU = TN/(TN+FP+FN), **mIoU = (fg+bg)/2**, Dice = 2TP/(2TP+FP+FN),
precision, recall (= fg pixel acc), bg acc, **mPA = (recall + bg_acc)/2**. eps = 1e-7 in num and denom
(so an empty-GT image predicted empty scores IoU = 1). Reported number = mean over the 301 test images.
⚠️ v4.ipynb computed a **dataset-level** (pooled-pixel) version instead → re-scored per-image (`per_image_t05`).

## 6. Hyperparameter optimisation (Optuna)

| | v3 | v4 |
|---|---|---|
| Trials | 12 | 30 planned, 25 recorded (19 complete, 5 pruned, 1 fail) |
| Epochs / trial | 12 | 12 |
| Search: lr_encoder | 1e-6–1e-4 log | 1e-6–1e-4 log |
| lr_decoder | 1e-4–3e-3 log | **3e-5**–3e-3 log |
| weight_decay | 1e-5–1e-2 log | 1e-5–**5e-2** log |
| dice_weight (ce = 1−dice) | 0.3–0.9 | 0.3–0.9 |
| Objective | best val mIoU in 12 ep | **mean of last 3 epochs'** val mIoU (with PolyLR over 12 ep) |
| Sampler / pruner | TPE(seed 42) / Median | TPE(seed 42) / Median(startup 10, warmup 5) |
| Trial 0 | enqueued baseline params | enqueued baseline params |
| Final train | 40 ep, patience 8 | 40 ep, patience 8 + PolyLR; then threshold tuned on val (0.30–0.90) |

v4 best = **trial 15**: lr_enc 2.679e-5, lr_dec 3.383e-5, wd 1.645e-3, dice 0.7564 (val objective 0.8136).
**v4-final** = those params, **80 epochs, patience 80 (no early stop), PolyLR over 80 ep, threshold 0.5.**
Best val mIoU 0.8344 at epoch 80 (still rising).

## 7. Label cleaning + curriculum learning

- **Phase 1 (`v2-clean-stage1`):** train on 1335 clean photos only (see `project.md` label audit).
- **Phase 2 (curriculum, `curriculum-learnings/v2-curriculum.ipynb`):** epochs 1–20 on the 1335 clean train photos,
  epochs 21–40 on all 1400. Early stop disabled before the switch; patience counter reset at epoch 21.
  Val/test identical to v1. Runs A (seed 42), B (seed 43); C (baseline seed 43) pending.
- `leakage_check.py` verifies no photo moved splits (0 moved, 0 shared for all runs).

## 8. Explainability — Seg-Eigen-CAM

- `pytorch-grad-cam`'s `SegEigenCAM`, subclassed (`SegEigenCAMLite`): CAM = first principal component (SVD) of
  `|grad| ⊙ activation`, sign-flipped so the dominant lobe is positive.
- Target layer: `decode_head.batch_norm` (fused 768-ch decoder feature, 1/4 res). Target = predicted plastic mask.
- **Faithfulness (deletion) test:** on 219 test photos with GT>0 and prediction>0, zero out (= mean colour after
  normalisation) the hottest 50% vs coldest 50% of predicted-plastic pixels by CAM, re-predict, measure share of
  the original plastic prediction that survives.

## 9. Deployment

- `deployment/server`: FastAPI + Gradio `/ui`, onion architecture (entities → domain → application → infrastructure → api),
  hosted as HF Space (port 7860). Weights from HF Hub `adamantix/pdisnet-weights` (or local `model/`).
- Endpoints: `GET /health`, `GET /models` (16 combos), `POST /predict` (file + arch/backbone/init) →
  mask (base64 PNG), coverage %, category, recommendation. Default model `segformer-mit_b3-imagenet` = v4-final.
- Coverage → category: 0 → none; <1.1% → low; <4.5% → moderate; ≥4.5% → high (constants in `core/domain/constants.py`).
- `deployment/web`: Next.js client (`src/app/page.tsx`, `components/ResultView.tsx`, typed API client).
- Old Streamlit client + server in `.archive/deployment/`.
