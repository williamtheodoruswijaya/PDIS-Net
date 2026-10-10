# DeepLabV3+ decoder + ResNet34 encoder, random init (raw)

| | |
|---|---|
| **Model** | `smp.DeepLabV3Plus("resnet34", encoder_weights=None)` |
| **Encoder** | ResNet34, random init, encoder lr = decoder lr (3e-4) as in v2 |
| **Params** | 22.4M |

Set in `CFG` as `arch="deeplab"`, `backbone="resnet34"`, `init="raw"`.

**Why this one:** it completes the raw ResNet34 row:

| ResNet34 random encoder | test mIoU |
|---|---|
| UNet (08) | 0.649 |
| SegFormer All-MLP head (11) | 0.654 |
| **DeepLabV3+ (15)** | **?** |

Raw UNet and raw SegFormer-head land within 0.01 of each other, and both sit about 0.12
below their ImageNet versions. If DeepLab does the same, the thesis can say that the
**initialisation matters more than the decoder** on 1,400 training images.

Identical to `notebooks/v2.ipynb` except `arch`, `init`, `backbone` and `run_version = "v2"` (named after the v2 template, like runs 11/12) in `CFG`. Outputs cleared.
