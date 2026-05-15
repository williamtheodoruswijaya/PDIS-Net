# Dataset And Models

## Dataset

The repository ignores `data/` because datasets are large and may not be suitable for version control.

Training notebooks reference the FloPWD 2025 plastic waste dataset.

## Model Artifacts

Current model folders:

```text
model/20260105 - Unet (IOU=0.67)
model/20261104 - Unet++ (IOU=0.56)
model/20261205 - Segformer (mIoU=0.81)
model/20261305 - DinoV3 (mIoU=0.7916)
```

## Default Runtime Model

Use:

```text
model/20261205 - Segformer (mIoU=0.81)
```

Why:

- strong metrics
- compatible with current local environment
- practical for the phone demo

## DINOv3 Model

Use for:

- research comparison
- future high-quality inference path
- ground-station experiments

Compatibility note:

- requires a Transformers version with EoMT-DINOv3 support

## Model Manifest

The demo tracks model paths in:

```text
droidcam-prototype/models/model_manifest.json
```

Update this file if model names, paths, or thresholds change.

