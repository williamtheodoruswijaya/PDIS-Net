# Aerial init — `restor/tcd-segformer-mit-b3`

| | |
|---|---|
| **HF source** | https://huggingface.co/restor/tcd-segformer-mit-b3 |
| **Trained on** | [`restor/tcd`](https://huggingface.co/datasets/restor/tcd) (OAM-TCD) — global aerial imagery @ 10 cm/px |
| **Task** | binary tree / no-tree, 2 classes |
| **Backbone** | MiT-B3 (same as the raw + imagenet runs) |
| **By** | Restor / ETH Zurich |
| **License** | code Apache-2; NVIDIA SegFormer research license; imagery mostly CC BY 4.0 |

Loaded in `build_model()` as `init="aerial"`.

**Why this one:** MiT-B3 keeps the backbone constant across the grid, and its head is
already `[2, 768, 1, 1]` — so `ignore_mismatched_sizes` drops nothing and the
**decoder transfers too**, not just the encoder.

**Not** `chribark/segformer-b3-finetuned-UAVid` — that repo's weights carry a
150-class ADE20K head, not UAVid's 8. Mislabelled.

**Caveat:** trained at 1024 px / 10 cm/px, we run 512 px. Uses ImageNet
normalisation, same as our `eval_tf`.
