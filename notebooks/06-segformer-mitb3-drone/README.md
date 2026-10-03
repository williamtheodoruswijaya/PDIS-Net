# Drone init — `pablojrios/segformer-b3-finetuned-drones`

| | |
|---|---|
| **HF source** | https://huggingface.co/pablojrios/segformer-b3-finetuned-drones |
| **Trained on** | Semantic Drone Dataset (TU Graz) — low-altitude nadir drone photos, 24 classes incl. `water` |
| **Task** | semantic segmentation, 24 classes |
| **Backbone** | MiT-B3 (same as raw / imagenet / aerial / ade runs) |
| **Started from** | `nvidia/mit-b3` (config `_name_or_path`) — the same weights as the imagenet run |
| **License** | not stated (no model card) |

Loaded in `build_model()` as `init="drone"`.

**Why this one:** closest public MiT-B3 to FloPWD's viewpoint — low drone, looking
straight down, water in frame. Because it started from `nvidia/mit-b3`, the
`imagenet` vs `drone` comparison isolates exactly one extra step: drone-photo
segmentation fine-tuning. The decoder transfers too; only the 24-wide classifier
is re-initialised by `ignore_mismatched_sizes`.

**Not** `chribark/segformer-b3-finetuned-ade-512-512-finetuned-UAVid` — real UAVid
labels, but its own model card reports val mIoU 0.0093 and it ships TensorFlow
weights only.

**Caveat:** no model card, so its own training quality is undocumented.

Identical to `05-segformer-mitb3-ade/v1.ipynb` except `CFG["init"]` and the
extra `"drone"` entry in the `src` dict.
