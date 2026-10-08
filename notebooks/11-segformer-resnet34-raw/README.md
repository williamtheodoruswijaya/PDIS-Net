# SegFormer decoder + ResNet34 encoder, raw init

| | |
|---|---|
| **Model** | `smp.Segformer("resnet34", decoder_segmentation_channels=768)` |
| **Encoder** | ResNet34, random init (`encoder_weights=None`), same as run 08's encoder |
| **Decoder** | SegFormer All-MLP head, width 768, same as run 10 |
| **LR** | encoder trains at `lr_decoder` (3e-4) because `init == "raw"`, same rule as runs 01 and 08 |

Set in `CFG` as `arch="segformer-smp"`, `backbone="resnet34"`, `init="raw"`.

**Why this one:** it fills the last empty cell of the raw column.

| | raw | imagenet |
|---|---|---|
| **UNet + ResNet34** | 08: 0.649 | 09: 0.768 |
| **SegFormer + ResNet34** | **11: ?** | 10: 0.780 |
| **SegFormer + MiT-B3** | 01: 0.472 | 02: 0.821 |

- 11 vs 01: same decoder, both from scratch. Only the encoder type changes (CNN vs transformer).
- 11 vs 08: same encoder, both from scratch. Only the decoder changes.
- If 11 lands near 08 (~0.65), the collapse of 01 comes from the **transformer encoder**,
  not the SegFormer decoder. A CNN assumes nearby pixels belong together; a transformer
  has to learn that, and 1400 images aren't enough.

**Caveats:** same as run 10. smp's decoder also reads ResNet's 1/2-resolution stem
(5 inputs vs MiT's 4), and the LRs were set for MiT, not tuned for this run.

Identical to `10-segformer-resnet34-imagenet/v1.ipynb` except `CFG["init"]`. Outputs cleared.
