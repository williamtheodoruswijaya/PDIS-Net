# DeepLabV3+ decoder + MiT-B3 encoder, ImageNet init

| | |
|---|---|
| **Model** | `smp.DeepLabV3Plus("mit_b3", encoder_weights="imagenet")` |
| **Encoder** | MiT-B3, smp `imagenet` weights (smp's copy of the official SegFormer ImageNet-1k release, same as run 03) |
| **Decoder** | ASPP (dilation rates 12/24/36) + one 1/4-resolution skip |
| **Params** | 45.2M (vs 47.2M SegFormer-B3 in run 02) |

Set in `CFG` as `arch="deeplab"`, `backbone="mit_b3"`, `init="imagenet"`.

**Why this one:** it is the only DeepLab run with a real chance at 02's 0.821, and it
holds the encoder fixed so only the decoder changes:

| MiT-B3 ImageNet encoder | test mIoU |
|---|---|
| SegFormer All-MLP (02) | 0.821 |
| UNet (03) | 0.792 |
| **DeepLabV3+ (13)** | **?** |

**Caveat:** DeepLab needs the last stage at 1/16 resolution, not 1/32. smp does this by
turning stage 4's stride-2 patch embedding into stride 1 with dilation 2. The pretrained
stage-4 weights were never trained that way, so this encoder is slightly modified compared
with 02/03. Mention it in Bab 3 if this row is reported.

Identical to `notebooks/v2.ipynb` except `arch`, `init`, `backbone` and `run_version = "v2"` (named after the v2 template, like runs 11/12) in `CFG`. Outputs cleared.
