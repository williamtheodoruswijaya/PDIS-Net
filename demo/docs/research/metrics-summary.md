# Metrics Summary

This file summarizes available metric artifacts. Always check the source files for exact values.

## SegFormer

Source:

```text
results/segformer/flopwd_test_metrics (2).json
```

Reported fields include:

- loss
- IoU
- foreground IoU
- background IoU
- mIoU
- Dice
- precision
- recall

The mIoU naming in the model folder is:

```text
model/20261205 - Segformer (mIoU=0.81)
```

## DINOv3/EoMT

Sources:

```text
results/dinov3/flopwd_eomt_dinov3_test_metrics.json
results/dinov3/flopwd_eomt_dinov3_training_history.csv
model/20261305 - DinoV3 (mIoU=0.7916)/training_metadata.json
```

Training metadata includes:

```text
best_threshold: 0.9
num_classes: 2
labels: background, plastic
```

## Metric Meaning

IoU:

```text
intersection / union
```

Dice:

```text
2 * overlap / total area
```

Precision:

```text
predicted plastic pixels that were correct
```

Recall:

```text
actual plastic pixels found by the model
```

## Deployment Warning

Good notebook metrics do not automatically mean good drone performance. Field conditions add motion blur, reflections, altitude changes, and camera angle issues.

