# SegFormer-B0, ImageNet init: `nvidia/mit-b0`

| | |
|---|---|
| **HF source** | https://huggingface.co/nvidia/mit-b0 |
| **Trained on** | ImageNet-1k (same data as run 02) |
| **Encoder** | MiT-B0: depths `[2,2,2,2]`, widths `[32,64,160,256]` (B3: `[3,4,18,3]`, `[64,128,320,512]`) |
| **Decoder** | width 256 from the official B0 config (B3 uses 768) |
| **Params** | ~3.8M vs ~47M for B3 (~12× smaller) |

Set in `CFG` as `arch="segformer"`, `backbone="mit_b0"`, `init="imagenet"`.

**Why this one:** it's the bottom rung of a size ladder.

| | params | test mIoU |
|---|---|---|
| **B0** | ~3.8M | **12: ?** |
| B3 | ~47M | 02: 0.821 |
| B5 | ~85M | 07: 0.809 |

B5 already showed that bigger doesn't help. B0 shows whether smaller hurts. If it's
within 0.02 of B3, a 12× smaller model is enough, which suits ZeroGPU deployment and
the edge-device angle of the FloPWD paper. If it loses by more than 0.02, run B2 next
to find where shrinking starts to hurt.

**Caveat:** this is the official B0 as a whole. The decoder also shrinks (256 vs 768),
so the comparison is "whole model size", not "encoder only". That is how the SegFormer
paper defines B0–B5 too.

Identical to `notebooks/v2.ipynb` except `CFG["backbone"]`. Outputs cleared.
