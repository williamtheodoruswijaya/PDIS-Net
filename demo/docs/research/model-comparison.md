# Model Comparison

## Current Models

| Model | Folder | Role |
| --- | --- | --- |
| U-Net | `model/20260105 - Unet (IOU=0.67)` | older baseline |
| U-Net++ | `model/20261104 - Unet++ (IOU=0.56)` | older baseline |
| SegFormer | `model/20261205 - Segformer (mIoU=0.81)` | default phone demo model |
| DINOv3/EoMT | `model/20261305 - DinoV3 (mIoU=0.7916)` | advanced comparison model |

## SegFormer

Strengths:

- strong segmentation metrics
- already supported by current local environment
- practical default for demo

Weaknesses:

- still may be heavy for small onboard drone hardware
- inference speed depends on device

## DINOv3/EoMT

Strengths:

- modern foundation-model-style segmentation
- strong comparison model
- useful for research framing

Weaknesses:

- much heavier
- needs newer Transformers support
- likely better for ground station/server than small drone hardware

## Practical Thesis Framing

Use SegFormer for the live prototype. Present DINOv3/EoMT as a stronger modern comparison and future high-compute option.

