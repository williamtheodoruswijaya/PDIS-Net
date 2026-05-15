# Model Inference Architecture

## Model Adapter Pattern

All model-specific logic is isolated in:

```text
droidcam-prototype/src/drone_phone_demo/models.py
```

The rest of the application expects each model adapter to return:

- probability map
- binary mask
- plastic percentage
- inference time

## SegFormer

SegFormer is the current default model.

Model folder:

```text
model/20261205 - Segformer (mIoU=0.81)
```

Runtime behavior:

1. Convert BGR frame to RGB.
2. Run SegFormer image processor.
3. Run model.
4. Upsample logits to original frame size.
5. Apply softmax.
6. Use class `1` as plastic.
7. Threshold to binary mask.

## DINOv3/EoMT

DINOv3/EoMT model folder:

```text
model/20261305 - DinoV3 (mIoU=0.7916)
```

Expected runtime behavior:

1. Convert BGR frame to RGB.
2. Run EoMT image processor.
3. Run model.
4. Read class query logits and mask query logits.
5. Softmax class queries.
6. Sigmoid mask queries.
7. Combine into semantic probabilities.
8. Upsample to original frame size.
9. Use class `1` as plastic.

## Thresholds

Current practical defaults:

| Model | Threshold |
| --- | --- |
| SegFormer | `0.8` |
| DINOv3/EoMT | `0.9` from training metadata |

Thresholds can be changed:

```powershell
py run_phone_demo.py --model segformer --source 0 --threshold 0.5
```

Lower thresholds increase recall but may increase false positives.

## Percentage Calculation

```text
plastic_percentage = binary_mask.mean() * 100
```

This is image-area percentage, not real-world square meters.

