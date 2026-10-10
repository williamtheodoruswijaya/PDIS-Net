# DeepLabV3+ decoder + ResNet34 encoder, ImageNet init

| | |
|---|---|
| **Model** | `smp.DeepLabV3Plus("resnet34", encoder_weights="imagenet")` |
| **Encoder** | ResNet34, smp `imagenet` weights, byte-identical start to runs 09 and 10 |
| **Params** | 22.4M (vs 24.4M UNet-ResNet34, 25.0M SegFormer-head-ResNet34) |

Set in `CFG` as `arch="deeplab"`, `backbone="resnet34"`, `init="imagenet"`.

**Why this one:** it completes the ResNet34 row, so all three decoders share one CNN encoder:

| ResNet34 ImageNet encoder | test mIoU |
|---|---|
| UNet (09) | 0.768 |
| SegFormer All-MLP head (10) | 0.780 |
| **DeepLabV3+ (14)** | **?** |

Together with run 13 this gives a 2 encoders x 3 decoders table.
Learning rates are the MiT-tuned ones from v2, like runs 09/10, so the comparison stays fair.
